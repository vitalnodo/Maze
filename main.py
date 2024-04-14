from dataclasses import dataclass
from secrets import choice, randbelow


@dataclass(frozen=True)
class Vector:
    x: int
    y: int


@dataclass(frozen=True)
class Room:
    position: Vector
    height: int
    width: int


TILE_ROAD = "░"
TILE_EMPTY = " "
TILE_ENTRANCE = "I"
TILE_EXIT = "O"
TILE_TREASURE = "T"
ROOM_NUMBER = 10
width, height = tuple(
    int(x)
    for x in input("Enter world size like width,height (80,25): ").strip().split(",")
    if x.strip()
) or (80, 25)

WORLD_SIZE = Vector(width, height)

rooms = []
matrix = [[TILE_EMPTY for j in range(WORLD_SIZE.x)] for i in range(WORLD_SIZE.y)]
for i in range(ROOM_NUMBER):
    origin = Vector(0, 0)
    room_p = Vector(randbelow(13) + 3, randbelow(13) + 3)
    position = Vector(randbelow(WORLD_SIZE.x), randbelow(WORLD_SIZE.y))
    rooms.append(Room(position, room_p.x, room_p.y))

connected_rooms = []
for a in rooms:
    for b in rooms:
        x_overlap = (a.position.x <= b.position.x <= a.position.x + a.width) or (
            a.position.x <= b.position.x + b.width <= a.position.x + a.width
        )
        y_overlap = (a.position.y <= b.position.y <= a.position.y + a.height) or (
            a.position.y <= b.position.y + b.height <= a.position.y + a.height
        )
        if x_overlap and y_overlap:
            connected_rooms.append([a, b])

groups = []
for pair in connected_rooms:
    one = [z for z in groups if pair[0] in z or pair[1] in z]
    if len(one) == 0:
        groups.append(set(pair))
    else:
        one[0].add(pair[0])
        one[0].add(pair[1])

while len(groups) > 1:
    g_a, g_b = choice(groups), choice(groups)
    while g_a == g_b:
        g_a, g_b = choice(groups), choice(groups)
    a, b = next(iter(g_a)), next(iter(g_b))
    middle_a = Vector((a.position.x + (a.width // 2)), (a.position.y + (a.height // 2)))
    middle_b = Vector((b.position.x + (b.width // 2)), (b.position.y + (b.height // 2)))
    groups[groups.index(g_a)] = g_a | g_b
    groups.remove(g_b)
    from_ = min(middle_a.y, min(middle_b.y, WORLD_SIZE.y))
    to_ = min(WORLD_SIZE.y, max(middle_a.y, middle_b.y))
    for i in range(from_, to_):
        matrix[i][min(middle_a.x, WORLD_SIZE.x - 1)] = TILE_ROAD
    from_ = min(middle_a.x, min(middle_b.x, WORLD_SIZE.x))
    to_ = min(WORLD_SIZE.x, max(middle_a.x, middle_b.x))
    for i in range(from_, to_):
        matrix[min(middle_b.y, WORLD_SIZE.y - 1)][i] = TILE_ROAD

for room in rooms:
    for i in range(room.width):
        for j in range(room.height):
            if (
                room.position.x + i < WORLD_SIZE.x
                and room.position.y + j < WORLD_SIZE.y
            ):
                matrix[room.position.y + j][room.position.x + i] = TILE_ROAD


def is_wall(point: Vector):
    if point.x < 0 or point.y < 0:
        return True
    if point.x >= WORLD_SIZE.x or point.y >= WORLD_SIZE.y:
        return True
    return matrix[point.y][point.x] == TILE_EMPTY


while True:
    random_entrance = choice(rooms)
    left = Vector(random_entrance.position.x - 1, random_entrance.position.y)
    top = Vector(random_entrance.position.x, random_entrance.position.y - 1)
    if is_wall(left) and is_wall(top):
        matrix[random_entrance.position.y][random_entrance.position.x] = TILE_ENTRANCE
        break

while True:
    random_entrance = choice(rooms)
    right = Vector(
        random_entrance.position.x + random_entrance.width,
        random_entrance.position.y + random_entrance.height - 1,
    )
    bottom = Vector(
        random_entrance.position.x + random_entrance.width - 1,
        random_entrance.position.y + random_entrance.height,
    )
    if is_wall(right) and is_wall(bottom):
        matrix[
            min(
                random_entrance.position.y + random_entrance.height - 1,
                WORLD_SIZE.y - 1,
            )
        ][
            min(
                random_entrance.position.x + random_entrance.width - 1,
                WORLD_SIZE.x - 1,
            )
        ] = TILE_EXIT
        break

if randbelow(2):
    random_room = choice(rooms)
    matrix[random_room.position.y][random_room.position.x] = TILE_TREASURE

for i in range(len(matrix)):
    for j in range(len(matrix[i])):
        print(f"{matrix[i][j]}", end="")
    print()
