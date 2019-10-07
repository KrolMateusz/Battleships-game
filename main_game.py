def generate_empty_map(size):
    battlefield = {}
    for letter in 'ABCDEFGHIJ':
        battlefield.setdefault(letter, ["." for _ in range(size)])
    return battlefield


def print_map(battlefield):
    print(end=' ')
    for number in range(len(battlefield)):
        print(number  + 1, end=' ')
        if number + 1 == len(battlefield):
            print()
    for row in battlefield:
        print(row, end='')
        for col in range(len(battlefield)):
            print(battlefield[row][col], end=' ')
        print()


def generate_ships():
    ships = {
        5: 1,
        4: 1,
        3: 1,
        2: 1,
        1: 1,
    }
    return ships


def place_ships(ships_to_place):
    while ships_to_place:
        for ship_size in ships_to_place:
            ship_placed = 0
            while ship_placed < ships_to_place[ship_size]:
                for ship_frag in range(ship_size):
                    print(ship_frag)
                # Walidacja
                ship_placed += 1
        ships_to_place.pop(ship_size)


if __name__ == "__main__":
    print_map(generate_empty_map(10))
    place_ships(generate_ships())
