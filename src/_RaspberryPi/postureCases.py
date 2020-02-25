import RPi.GPIO as GPIO
import time

# Set numbering convention by pin number on the board itself
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Set GPIO as output
GPIO.setup(29,GPIO.OUT)     # Left
GPIO.setup(31,GPIO.OUT)     # Right
GPIO.setup(33,GPIO.OUT)     # Back
GPIO.setup(35,GPIO.OUT)     # Lumbar

vibrateTime = 2

def correctUpright(FR, FL, BR, BL, UL, UR, LL, LR):
    if FR == 0 and FL == 0 and BR == 0 and BL == 0 and \
            (UL == 0 or UR == 0) and LL == 0 and LR == 0:
        # No motor action done
        return True
    else:
        return False

def leanForward(FR, FL, BR, BL, UL, UR, LL, LR):
    if FR >= 0 and FL >= 0 and BR >= 0 and BL >= 0 and \
            (UL < 0 or UR < 0) and LL >= 0 and LR >= 0:
        # Lumbar on
        GPIO.output(35, GPIO.HIGH)
        time.sleep(vibrateTime)
        GPIO.output(35, GPIO.LOW)
        return True
    else:
        return False

def leanBackward(FR, FL, BR, BL, UL, UR, LL, LR):
    if FR < 0 and FL < 0 and BR >= 0 and BL >= 0 and \
            LL >= 0 and LR >= 0:
        # Back on
        GPIO.output(33, GPIO.HIGH)
        time.sleep(vibrateTime)
        GPIO.output(33, GPIO.LOW)
        return True
    else:
        return False

def leanLeft(FR, FL, BR, BL, UL, UR, LL, LR):
    if FR < 0 and FL >= 0 and BR < 0 and BL >= 0:
        # Left on
        GPIO.output(29, GPIO.HIGH)
        time.sleep(vibrateTime)
        GPIO.output(29, GPIO.LOW)
        return True
    else:
        return False

def leanRight(FR, FL, BR, BL, UL, UR, LL, LR):
    if FR >= 0 and FL < 0 and BR >= 0 and BL < 0:
        # Right on
        GPIO.output(31, GPIO.HIGH)
        time.sleep(vibrateTime)
        GPIO.output(31, GPIO.LOW)
        return True
    else:
        return False

def sitForwards(FR, FL, BR, BL, UL, UR, LL, LR):
    if FR >= 0 and FL >= 0 and BR <= 0 and BL <= 0 and \
            (UL < 0 or UR < 0) and LL < 0 and LR < 0:
        # Left + Right on
        GPIO.output(29, GPIO.HIGH)
        GPIO.output(31, GPIO.HIGH)
        time.sleep(vibrateTime)
        GPIO.output(29, GPIO.LOW)
        GPIO.output(31, GPIO.LOW)
        return True
    else:
        return False

