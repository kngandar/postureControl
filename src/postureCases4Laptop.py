import time

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
        print('Lumbar on')
        return True
    else:
        return False

#if FR >= 0 and FL >= 0 and BR <= 0 and BL <= 0 and \


def leanBackward(FR, FL, BR, BL, UL, UR, LL, LR):
    if FR < 0 and FL < 0 and BR >= 0 and BL >= 0 and \
         LL >= 0 and LR >= 0:
        # Back on
        print('Back on')
        return True
    else:
        return False


def leanLeft(FR, FL, BR, BL, UL, UR, LL, LR):
    if FR < 0 and FL >= 0 and BR < 0 and BL >= 0:
        # Left on
        print('Left on')
        return True
    else:
        return False


def leanRight(FR, FL, BR, BL, UL, UR, LL, LR):
    if FR >= 0 and FL < 0 and BR >= 0 and BL < 0:
        # Right on
        print('Right on')
        return True
    else:
        return False


def slouching(FR, FL, BR, BL, UL, UR, LL, LR):
    if FR >= 0 and FL >= 0 and BR <= 0 and BL <= 0 and \
        UL < 0 and UR < 0 and LL < 0 and LR < 0:
        # Lumbar on
        print('Left + Right on')
        return True
    else:
        return False


def sitForwards(FR, FL, BR, BL, UL, UR, LL, LR):
    if FR >= 0 and FL >= 0 and BR <= 0 and BL <= 0 and \
        (UL < 0 or UR < 0) and LL < 0 and LR < 0:
        # Lumbar on
        print('Left + Right on')
        return True
    else:
        return False
