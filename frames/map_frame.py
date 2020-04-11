DATA = 'GM|+379;1;22;-3;79,48;-3;1560^105,1569^105;8,14;-1,-1,-1;0,0,0,0;-1,-1,-1;0,0,0,0;|+268;3;33;-1;59,47,47,31,31,103;-3;1565^100,1001^90,1001^90,1563^100,1563^110,1020^95;5,23,23,4,6,14;-1,-1,-1;0,0,0,0;-1,-1,-1;0,0,0,0;-1,-1,-1;0,0,0,0;-1,-1,-1;0,0,0,0;-1,-1,-1;0,0,0,0;-1,-1,-1;0,0,0,0;|+453;1;0;-2;31,47,47;-3;1563^90,1001^90,1001^90;2,23,23;-1,-1,-1;0,0,0,0;-1,-1,-1;0,0,0,0;-1,-1,-1;0,0,0,0;'


class Entity:
    def __init__(self, type, **kwargs):
        self.type = type
        self.__dict__.update(kwargs)

    def __str__(self):
        return '<{}}> {}'.format(self.type, self.__dict__)


# GM
class MapFrame:
    def __init__(self, raw_data, game_state):
        self.entities = []
        self.game_state = game_state
        self.parse_data(raw_data)
        self.game_state.update_entities(self.entities)

    def __repr__(self):
        return 'Entities\n{}'.format('\n'.join(map(str, self.entities))) if self.entities else 'No entities'

    def parse_data(self, data):
        instances = data[3:].split('|')
        for instance in instances:
            if len(instance) < 1:
                continue
            if instance[0] == '+':
                infos = instance[1:].split(';')
                cell = int(infos[0])
                id = int(infos[3])
                template = infos[4]
                type = int(infos[5]) if ',' not in infos[5] else int(infos[5].split(',')[0])

                # SWITCH
                if type == -1:  # creature
                    pass
                elif type == -2:  # mob
                    if not self.game_state.isFighting:
                       return
                    # monster_team = infos[15] if len(infos) <= 18 else infos[22]
                    self.entities.append(Entity('Mob', cell=cell, id=id, pa=infos[12], health=infos[13], pm=infos[14]))
                elif type == -3:  # group of mob
                    templates = list(map(int, template.split(',')))
                    levels = list(map(int, infos[7].split(',')))
                    self.entities.append(Entity('GroupMob', cell=cell, id=id, templates=templates, levels=levels))
                elif type == -4:  # NPC
                    pass  # mapa.entidades.TryAdd(id, new Npc(id, int.Parse(nombre_template), celda))
                elif type == -5:  # Merchants
                    pass  # mapa.entidades.TryAdd(id, new Mercantes(id, celda))
                elif type == -6:  # resources
                    pass
                else:  # players
                    self.entities.append(Entity('Player', cell=cell, id=id, name=infos[4], guild=infos[16]))


if __name__ == '__main__':
    m = MapFrame(DATA)
    print(m)