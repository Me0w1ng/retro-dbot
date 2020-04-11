from data.map import Map
import logging

# 1, -34
# DATA = 'GDM|1853|0706131721|4c2f4c4c7d204c71236065687966574a554e3d464841354820462930786b6f5f2f225f2f51632f7b78342f41206e7a2877377c61555a7378764d33553a622e5b57343a3d602422737c732447686a787538755d644660682d756864376e2a4b436c6b4f576c60263b703b2139766b44407326554c68327c5f39383031445d613d677369473b5877274262'
DATA = 'GDM|8482|0907100942|40472451204e504d712c3e253235334848235d7163347a5f7f6b504a5d4c446e6b7b7e604466457d3c4f223f6a314a425a5b6827605d74494544374078694652597b2a583e582a273a4127524d3f2e724e582a516a68564723596f6b3d70766c6379443c4b267f615a7c523e5c794d5a7429594d7d2e69412c702f476d5542746c644c7b5b5b22296b273f7963602532352f7f33353d622d39253242603633692e696e462f50787b2722553c27635f7f265334613564292e606972714a667a6645673e6972584a4449605143637e3632503b20'


# GDM
class MapChange:
    def __init__(self, raw, game_state=None):
        data = raw[4:].split('|')
        map_id = data[0]
        map_date = data[1]
        map_key = data[2]
        self.map = Map(map_id, map_date, map_key)
        if game_state:
            game_state.map_changed(self.map)


if __name__ == '__main__':
    m = MapChange(DATA)
    m.map.debug()