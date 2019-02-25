import logging
import threading
import time
import serial
import sys
import datetime

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',)

def main():

    # ttg: [ Initialization ]
    global programRunning
    global userInput
    global cmd
    programRunning = True
    userInput = False
    cmd = ''

    global samplingTime
    global time2evaluate
    global newTime2evaluate
    samplingTime = 1  # seconds
    time2evaluate = 9  # every 30 seconds
    newTime2evaluate = 0

    global refForce
    global tolForce
    refForce = 0
    tolForce = 6

    global snooze
    snooze = False

    # ttg: [ Setup ]
    global arduino
    arduino = serial.Serial('/dev/ttyACM0', 9600)
    #arduino = serial.Serial('COM4', 9600)

    print('Running main function now...')

    wait = threading.Thread(name='userInput', target=waitUserInput)
    read = threading.Thread(name='readSensor', target=readSensorData)

    wait.start()
    read.start()

    while programRunning:
        if not wait.isAlive():
            print('Wait is: ' +  str(wait.isAlive()))
            wait = threading.Thread(name='userInput', target=waitUserInput)
            wait.start()
        time.sleep(1)    


def waitUserInput():
    # ttg: Waits for user input, if there's one set flag
    global cmd
    global userInput

    logging.debug('Starting')
    cmd = input()

    if cmd is not '':
        print('Got user input! ')
        userInput = True
        handleUserInput()

    logging.debug('Exiting')


def readSensorData():
    global samplingTime
    global snooze
    global arduino
    global newTime2evaluate
    global time2evaluate

    averageForce = 0
    counter = 0
    evalResult = ''

    logging.debug('Starting')


    # ttg: Create text file to log data for the day
    now = datetime.datetime.now()
    filename = [now.strftime('%Y-%m-%d') + '.txt']
    print('Text file name: ' + ''.join(filename))
    file = open(''.join(filename), 'w')


    # ttg: Read data while program is running, and not snoozing
    while programRunning:
        if not snooze:
            counter = counter + 1
            #print('Counter: ' +  str(counter))

            # TODO: String manipulation - Parse data for an ARRAY
            data = arduino.readline().decode().strip('\r\n')
            print('Data: ' + data)


            # ttg: Evaluate by taking average last 5 points in each eval period
            if counter == time2evaluate:
                counter = 0
                evalResult = evaluatePosture(averageForce)
                averageForce = 0

                print('Eval Result is: ' +  evalResult)

                if newTime2evaluate is not 0:
                    time2evaluate = newTime2evaluate
                    newTime2evaluate = 0

                    print('New eval period is now: ' + str(time2evaluate))

            elif counter == time2evaluate - 5:
                # Need to record first value of average force
                print('Counter: ' + str(counter))
                averageForce = int(data)

            elif counter > (time2evaluate - 5):
                # Note 1: Average force should be reset by evaluatePosture btw
                # Note 2: This should be an array not just a data
                print('Counter: ' + str(counter))
                averageForce = (averageForce + int(data)) / 2
                print ('Average Force: ' + str(averageForce))


            # ttg: Write data and evalResult to text given that it is not empty
            # TODO: Write to text file for an ARRAY
            # 1 text file per day for now
            if evalResult is not '':
                file.write(data + ' ' + evalResult + '\n')
                evalResult = ''
            else:
                file.write(data + '\n')

            time.sleep(samplingTime)

        # DEBUG CHUNK - Maybe delete later,,,
        else:
            print('Snoozing...')
            time.sleep(1)

            # ttg: Reset counter and averageForce values when user ask to snooze program
            counter = 0
            averageForce = 0


    logging.debug('Exiting')


def recalibrate():
    # ttg: Read reference force from current seating position
    global refForce

    # TODO: read refForce from EACH sensor
    print('Reading refForce...')
    refForce = int(arduino.readline().decode().strip('\r\n'))
    print('refForce is set to: ' + str(refForce))


def setTolerance(tolValue):
    # ttg: Set the tolerance to difference in acceptable and non-acceptable force
    global tolForce

    tolForce = tolValue
    print('Set tolerance value to: ' + str(tolForce))


def vibrateSeat():
    # ttg: Vibrate seat motors
    print('Vibrating seat motors...')


def vibrateBack():
    # ttg: Vibrate back motors
    print('Vibrating back motors...')


def evaluatePosture(averageForce):
    # ttg: Evaluate if need to vibrate motors
    global refForce
    global tolForce

    print('Evaluating Posture...')

    if abs(averageForce - refForce) > tolForce:
        # Bad posture
        evalResult = 'Bad'

        # TODO: Depending on which sensors were bad, call respective vibrate functions
        # For now, vibrate the seat motors
        vibrateSeat()
        vibrateBack()

    else:
        # Ok posture
        evalResult = 'Good'

    return evalResult


def handleUserInput():
    # ttg: Handles the different user inputs
    global cmd
    global programRunning
    global snooze

    print('Command:' + cmd)

    option = cmd[0]

    if int(cmd) > 5:
        # Need to parse cmd
        print('Need to parse command')
        value = int(cmd[1:])

    if option is '1':
        # ttg: Do shutdown sequence

        print('Shutting down...')

        programRunning = False
        time.sleep(2)   # waits 2 seconds, before shutting down RPi
        sys.exit()      # exits off program, for now,,,
        #call('sudo shutdown -h now', shell=True)

    elif option is '2':
        # ttg: Do recalibrate
        recalibrate()

    elif option is '3':
        # ttg: Sets force tolerance
        setTolerance(value)

    elif option is '4':
        # ttg: Snooze program

        snooze = True

        print('Snoozing for:' + str(value) + ' seconds')

        time.sleep(value)
        snooze = False
        # NOTE: Maybe log also snooze period (?)

    elif option is '5':
        # ttg: Set evaluate period
        global newTime2evaluate

        newTime2evaluate = value

        print('Will change eval time on next cycle...')

if __name__ == '__main__':
    main()



