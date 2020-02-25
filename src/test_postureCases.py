from postureCases import *

# Test file
# If successful, this means the postures are independent from each other,
# and that importing postureCases can vibrate motor

FR = 0
FL = 0
BR = 0
BL = 0

if correctUpright(FR, FL, BR, BL):
    print("Correct posture")

elif leanForward(FR, FL, BR, BL):
    print("Lean forwards")

elif leanBackward(FR, FL, BR, BL):
    print("Lean backwards")

elif leanLeft(FR, FL, BR, BL):
    print("Lean left")

elif leanRight(FR, FL, BR, BL):
    print("Lean right")

elif twistLeft(FR, FL, BR, BL):
    print("Twisted left")

elif twistRight(FR, FL, BR, BL):
    print("Twisted right")

elif slouching(FR, FL, BR, BL):
    print("Slouching")


print("Done testing")
