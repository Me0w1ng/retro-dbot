# Login
COORD_USERNAME = (108, 192)
COORD_PASSWORD = (108, 260)
COORD_SUBMIT_BT = (160, 320)
COORD_SERVER = (120, 304)
COORD_PLAYER_1 = (115, 323)
COORD_PLAY = (365, 438)

# Fight
COORD_READY = (688, 426)
COORD_PASS_TURN = (492, 552)
SPELL_1 = (530, 519)
SPELL_16 = (698, 548)

def spell_n(n) -> (int, int): # starts at 1
    gapx = int((SPELL_16[0] - SPELL_1[0]) / 8)
    x = SPELL_1[0] + ((n - 1) % 8) * gapx,
    y = SPELL_16[1] if n > 8 else SPELL_1[1]
    return x, y
