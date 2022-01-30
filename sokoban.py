import enum


class Direction(enum.IntEnum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4


class Entity(str, enum.Enum):
    PLAYER = '@'
    WALL = '#'
    FLOOR = ' '
    DOCK = '.'
    BOX = '$'


class GameManager:
    def __init__(self, level):
        self.level = level
        self.player_pos = [0, 0]
        self.memory = []

        dock_count = 0
        for i in range(len(level)):
            for j in range(len(level[i])):
                if Entity.PLAYER in level[i][j]:
                    self.player_pos = [j, i]

                if Entity.DOCK in level[i][j]:
                    dock_count += 1

        self.total_docks = dock_count
        self.docks_left = dock_count
        self.__output_game_state()

    def __output_game_state(self):
        for i in range(len(self.level)):
            for j in range(len(self.level[i])):
                print(self.level[i][j][-1], end='')
            print('')

    def __check_obstacle(self, pos):
        entities = self.level[pos[1]][pos[0]]
        if Entity.WALL in entities or Entity.BOX in entities:
            return entities
        return []

    def __check_dock(self, pos):
        if self.level[pos[1]][pos[0]] == Entity.DOCK:
            return True
        return False

    def __move_entity(self, old_pos, new_pos, entity):
        self.level[new_pos[1]][new_pos[0]].append(entity.value)
        self.level[old_pos[1]][old_pos[0]].remove(entity.value)
        self.memory[-1].append((old_pos, new_pos, entity.value))

        if Entity.PLAYER is entity:
            self.player_pos = new_pos

    def move(self, direction: Direction):
        index = None
        increment = None
        self.memory.append([])

        if direction == Direction.NORTH:
            index = 1
            increment = -1
        elif direction == Direction.EAST:
            index = 0
            increment = 1
        elif direction == Direction.SOUTH:
            index = 1
            increment = 1
        elif direction == Direction.WEST:
            index = 0
            increment = -1
        else:
            return False

        new_player_pos = self.player_pos.copy()
        new_player_pos[index] += increment
        if Entity.WALL in self.__check_obstacle(new_player_pos):
            return False

        if Entity.BOX in self.__check_obstacle(new_player_pos):
            box_pos = new_player_pos.copy()
            new_box_pos = box_pos.copy()
            new_box_pos[index] += increment
            if self.__check_obstacle(new_box_pos):
                return False

            if self.__check_dock(new_box_pos):
                self.docks_left -= 1

            if self.__check_dock(box_pos):
                self.docks_left += 1

            self.__move_entity(box_pos, new_box_pos, Entity.BOX)
        self.__move_entity(self.player_pos, new_player_pos, Entity.PLAYER)

        self.__output_game_state()


__all__ = ["Direction", "Entity", "GameManager"]
