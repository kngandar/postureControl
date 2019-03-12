import threading
import serial
import sys
import datetime

#from postureCases import *
from postureCases4Laptop import *

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
    samplingTime = 1    # seconds
    time2evaluate = 15
    newTime2evaluate = 0

    global seat_refForce
    global seat_tolForce
    global seat_tolPercent
    seat_refForce = [0.0, 0.0, 0.0, 0.0]
    seat_tolForce = [2, 2, 2, 2]            # dummy values
    seat_tolPercent = [0.10, 0.05, 0.15, 0.15]

    global back_refForce
    global back_tolForce
    global back_tolPercent
    back_refForce = [0.0, 0.0, 0.0, 0.0]
    back_tolForce = [0.5, 0.5, 0.5, 0.5]    # dummy values
    back_tolPercent = [0.5, 0.5, 0.3, 0.3]

    global numOfVars2Average
    numOfVars2Average = 5

    global recalibrate
    recalibrate = False

    global snooze
    snooze = False

    # ttg: [ Setup ]
    global arduino
    #arduino = serial.Serial('/dev/ttyACM0', 9600)
    arduino = serial.Serial('COM3', 9600)
    time.sleep(3)

    #  > Running main function now...

    wait = threading.Thread(name='userInput', target=waitUserInput)
    read = threading.Thread(name='readSensor', target=readSensorData)

    wait.start()
    read.start()

    # ttg: Check if program is running every second, and spawn new userInput thread whenever one has already completed
    while programRunning:
        if not wait.isAlive():
            wait = threading.Thread(name='userInput', target=waitUserInput)
            wait.start()
        time.sleep(1)


def waitUserInput():
    # ttg: Waits for user input, if there's one set flag
    global cmd
    global userInput

    # > Thread Starting...
    cmd = input()

    if cmd is not '':
        # > Got user input!
        userInput = True
        handleUserInput()

    # > Thread Exiting...


def readSensorData():
    global samplingTime
    global snooze
    global arduino
    global newTime2evaluate
    global time2evaluate
    global numOfVars2Average

    global recalibrate
    global seat_refForce
    global seat_tolForce
    global seat_tolPercent

    global back_refForce
    global back_tolForce
    global back_tolPercent

    seat_averageForce = [0.0, 0.0, 0.0, 0.0]
    back_averageForce = [0.0, 0.0, 0.0, 0.0]
    counter = 0
    evalResult = ''

    prev_sensorVal = []

    # > Thread Starting...

    # ttg: Create text file to log data for the day
    now = datetime.datetime.now()
    filename = [now.strftime('%Y-%m-%d_%H-%M') + '.txt']
    file = open(''.join(filename), 'w')     # converts it into a string (?)

    # ttg: Read data while program is running, and not snoozing
    while programRunning:
        if not snooze:
            counter = counter + 1

            # ttg: String manipulation - strips data to numbers, removes commas, convert string into floats
            arduino.write("5".encode())
            data = arduino.readline().decode().strip('\r\n')
            data = data.split(', ')

            try:
                sensorVal = [float(i) for i in data]   # float version of data
            except:
                # > CONVERSION ERROR DUE TO BAD SERIAL COMMUNICATION
                sensorVal = prev_sensorVal


            # ttg: Recalibrate reference value
            if recalibrate:
                # Set reference forces
                seat_refForce = [(sensorVal[i]) for i in range(0, 4)]
                back_refForce = [(sensorVal[i]) for i in range(4, 8)]

                # Record change
                file.write(' > seat_refForce is set to: ' + str(seat_refForce))
                file.write(' > back_refForce is set to: ' + str(back_refForce))

                # Calculate tolerance forces
                for i in range(len(seat_refForce)):
                    seat_tolForce[i] = seat_tolPercent[i] * seat_refForce[i]
                for i in range(len(back_refForce)):
                    back_tolForce[i] = back_tolPercent[i] * back_refForce[i]

                # Forces the headrest tolerance to be a fixed value
                back_tolForce[0] = 0.5
                back_tolForce[1] = 0.5

                recalibrate = False

                # Sends to web app recalibrate is done
                print('Done')


            # ttg: Evaluate by taking average last 5 points in each eval period
            if counter == time2evaluate:

                counter = 0
                seat_averageForce = [seat_averageForce[i] + sensorVal[i] for i in range(0,4)]
                back_averageForce = [back_averageForce[i-4] + sensorVal[i] for i in range(4,8)]

                seat_averageForce = [val/numOfVars2Average for val in seat_averageForce]   # actually averages the force
                back_averageForce = [val/numOfVars2Average for val in back_averageForce]  # actually averages the force

                evalResult = evaluatePosture(seat_averageForce, back_averageForce)
                seat_averageForce = [0.0, 0.0, 0.0, 0.0]
                back_averageForce = [0.0, 0.0, 0.0, 0.0]

                if newTime2evaluate is not 0:
                    time2evaluate = newTime2evaluate
                    newTime2evaluate = 0

                    # > Changed new eval period

                    # Sends to web app that evaluate period is changed
                    print('Done')


            elif counter > (time2evaluate - numOfVars2Average):
                # Note 1: Average force should be reset by evaluatePosture btw
                # Note 2: This should be an array not just a data

                # _averageForce here actually just accumulates data (total force)

                seat_averageForce = [seat_averageForce[i] + sensorVal[i] for i in range(0, 4)]
                back_averageForce = [back_averageForce[i-4] + sensorVal[i] for i in range(4, 8)]


            # ttg: Write data and evalResult to text given that it is not empty
            # TODO: Write to text file for an ARRAY
            # 1 text file per day for now
            if evalResult is not '':
                file.write(str(data) + '\n')
                for i in range(len(evalResult)):
                    file.write(evalResult[i] + '\n')
                evalResult = ''
            else:
                file.write(str(data) + '\n')

            prev_sensorVal = sensorVal
            time.sleep(samplingTime)

        # ttg: Checks every 1 second if we got out of snooze
        else:
            # > Snoozing...
            time.sleep(1)

            # ttg: Reset counter and seat_averageForce values when user ask to snooze program
            counter = 0
            seat_averageForce = [0.0, 0.0, 0.0, 0.0]
            back_averageForce = [0.0, 0.0, 0.0, 0.0]

            # ttg: In the event, user does: change eval_time, snooze, snooze, ...
            # ttg: New eval_time will be updated once unsnoozed; otherwise, the change will delayed by snooze(s)
            if newTime2evaluate is not 0:
                time2evaluate = newTime2evaluate
                newTime2evaluate = 0

                # > Changed new eval period

                # Sends to web app that evaluate period is changed
                print('Done')

    file.close()
    # > Thread Exiting...


def evaluatePosture(seat_averageForce, back_averageForce):
    # ttg: Evaluate if need to vibrate motors
    global seat_refForce
    global seat_tolForce

    global back_refForce
    global back_tolForce

    # > Evaluating Posture...

    goodSensors = [0, 0, 0, 0, 0, 0, 0, 0]
    logdata = []

    # Convert sensors to relative values
    seat_relative = [seat_averageForce[i] - seat_refForce[i] for i in range(len(seat_refForce))]
    back_relative = [back_averageForce[i] - back_refForce[i] for i in range(len(back_refForce))]

    # Check each sensor to corresponding tolerance values
    for i in range(0, 4):
        if abs(seat_relative[i]) > seat_tolForce[i]:
            # Value is bad; out of range
            goodSensors[i] = 0

        else:
            # Value is good; within range
            goodSensors[i] = 1

    # Different check procedure for headrest
    for i in range(0, 2):
        if back_averageForce[i] > back_tolForce[i]:
            # Value is good for headrest; applying enough pressure
            goodSensors[i+4] = 1

        else:
            # Value is bad; out of range
            goodSensors[i+4] = 0


    for i in range(2, 4):
        if abs(back_relative[i]) > back_tolForce[i]:
            # Value is bad; out of range
            goodSensors[i+4] = 0

        else:
            # Value is good; within range
            goodSensors[i+4] = 1

    logdata.append(' Good sensors: ' + str(goodSensors))

    # Send to web app sensor results
    print(str(goodSensors))

    # TODO: Utilise postureCases functions - see code from test_postureCases.py
    # ttg: Only sends numbers above or below 0 to indicate out of bound values
    FR = seat_relative[0] if goodSensors[0] == 0 else 0
    FL = seat_relative[1] if goodSensors[1] == 0 else 0
    BR = seat_relative[2] if goodSensors[2] == 0 else 0
    BL = seat_relative[3] if goodSensors[3] == 0 else 0

    UL = back_relative[0] if goodSensors[4] == 0 else 0
    UR = back_relative[1] if goodSensors[5] == 0 else 0
    LL = back_relative[2] if goodSensors[6] == 0 else 0
    LR = back_relative[3] if goodSensors[7] == 0 else 0

    logdata.append(' FR: ' + str(FR) + ', FL: ' + str(FL) + ', BR: ' + str(BR) + ', BL: ' + str(BL))
    logdata.append( 'UL: ' + str(UL) + ', UR: ' + str(UR) + ', LL: ' + str(LL) + ', LR: ' + str(LR))

    logdata.append(' seat_tolForce is set to: ' + str(seat_tolForce))
    logdata.append(' back_tolForce is set to: ' + str(back_tolForce))

    if correctUpright(FR, FL, BR, BL, UL, UR, LL, LR): evalResult = 'Correct upright'
    elif leanForward(FR, FL, BR, BL, UL, UR, LL, LR): evalResult = 'Lean forwards'
    elif leanBackward(FR, FL, BR, BL, UL, UR, LL, LR): evalResult = 'Lean backwards'
    elif leanLeft(FR, FL, BR, BL, UL, UR, LL, LR): evalResult = 'Lean left'
    elif leanRight(FR, FL, BR, BL, UL, UR, LL, LR): evalResult = 'Lean right'
    elif sitForwards(FR, FL, BR, BL, UL, UR, LL, LR): evalResult = 'Sitting Forward'
    else: evalResult = 'Posture not characterized'

    logdata.append(' Current posture: ' + evalResult)

    return logdata


def handleUserInput():
    # ttg: Handles the different user inputs
    global cmd
    global programRunning
    global snooze

    global recalibrate

    option = cmd[0]

    if option is '1':
        # ttg: Do shutdown sequence

        # > Shutting down...
        print(str([2, 2, 2, 2, 2, 2, 2, 2]))

        programRunning = False
        time.sleep(2)   # waits 2 seconds, before shutting down RPi
        sys.exit()      # exits off program, for now,,,

    elif option is '2':
        # ttg: Do recalibrate
        recalibrate = True


    elif option is '4':
        # ttg: Snooze program
        print(str([2, 2, 2, 2, 2, 2, 2, 2]))

        snooze = True
        value = int(cmd[1:])

        time.sleep(value)
        snooze = False

        # Sends to web app that snooze is done
        print('Done')


    elif option is '5':
        # ttg: Set evaluate period
        global newTime2evaluate

        value = int(cmd[1:])
        newTime2evaluate = value


if __name__ == '__main__':
    main()



