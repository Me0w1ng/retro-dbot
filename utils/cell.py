HEX_CHARS = "0123456789ABCDEF"
ZKARRAY = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
SUN_MAGICS = [1030, 1029, 4088]


def unhash_cell(raw_cell):
    return [ZKARRAY.index(i) for i in raw_cell]


class Cell:
    def __init__(self, raw_data=None, index=-1):
        self.index = index
        self.entity = None
        self.color = 'black'
        self.dead = True
        self.text = ' '
        self.posIJ = []
        self.lineOfSight = False
        self.movement = 8
        self.initialized = False
        if raw_data:
            self.parse_data(raw_data)
            self.set_default_display()

    def parse_data(self, raw_data):
        cd = unhash_cell(raw_data)
        self.isActive = (cd[0] & 32 >> 5) == 1
        self.lineOfSight = (cd[0] & 1) == 1
        self.layerGroundRot = cd[1] & 48 >> 4
        self.groundLevel = cd[1] & 15
        self.movement = ((cd[2] & 56) >> 3)
        self.layerGroundNum = (cd[0] & 24 << 6) + (cd[2] & 7 << 6) + cd[3]
        self.layerObject1Num = ((cd[0] & 4) << 11) + ((cd[4] & 1) << 12) + (cd[5] << 6) + cd[6]
        self.layerObject2Num = ((cd[0]&2)<<12) + ((cd[7]&1)<<12) + (cd[8]<<6) + cd[9]
        self.isSun = self.layerObject1Num in SUN_MAGICS or self.layerObject2Num in SUN_MAGICS
        self.text = str(self.movement)
        self.initialized = True

    def is_obstacle(self):
        return self.lineOfSight and not self.entity

    def set_default_display(self):
        self.text = str(self.movement)
        if self.isSun:
            self.color = 'yellow'
            self.dead = False
        elif self.movement == 0 and self.lineOfSight:
            self.color = 'grey'
            self.dead = False
        elif self.lineOfSight:
            self.color = 'white'

    def set_entity(self, entity):
        if not entity:
            self.entity = None
            self.set_default_display()
        elif not entity.dead:
            self.entity = entity
            self.color = 'red'
            self.text = self.entity.type[0]

    def __repr__(self):
        return str(self.__dict__)

    def __str(self):
        return self.__repr__()