import string

def generate_empty_map(size):
    battlefield = {}
    for letter in 'ABCDEFGHIJ':
        battlefield.setdefault(letter, ["." for _ in range(size)])
    return battlefield


def print_map(player_battlefield):
    print(end='  ')
    for number in range(len(player_battlefield)):
        print(number  + 1, end='  ')
        if number + 1 == len(player_battlefield):
            print()
    for row in player_battlefield:
        print(row, end=' ')
        for col in range(len(player_battlefield)):
            print(player_battlefield[row][col], end='  ')
        print()


def generate_ships():
    ships = {
        5: 1,
        4: 1,
        3: 2,
        2: 1,
    }
    return ships

def get_ship_pos(ship_len):
    print('Podaj pozycję statku o rozmiarze ', ship_len)
    start_pos, end_pos = input('Podaj pozycję początkową oraz końcową: ').upper().split()
    if end_pos[0] < start_pos[0]:
        start_pos, end_pos = end_pos, start_pos
    elif int(end_pos[1:]) < int(start_pos[1:]):
        start_pos, end_pos = end_pos, start_pos
    return start_pos, end_pos


def check_ship_level(ship_start, ship_end, ship_len):
    alphabet = string.ascii_uppercase
    ship_start_letter, ship_start_number = ship_start[0], int(ship_start[1:]) -1
    ship_start_letter_index = alphabet.index(ship_start_letter)
    ship_end_letter, ship_end_number = ship_end[0], int(ship_end[1:]) - 1
    ship_end_letter_index = alphabet.index(ship_end_letter)
    # Sprawdzanie, czy statek jest ustawiony pionowo
    if ship_start_number == ship_end_number:
        if (ship_start_letter_index - ship_end_letter_index == ship_len - 1 or
                ship_start_letter_index - ship_end_letter_index == -ship_len + 1):
            return 'vertical'
    # Sprawdzanie, czy statek jest ustawiony poziomo
    if ship_start_letter == ship_end_letter:
        if (ship_start_number - ship_end_number == ship_len - 1 or
                ship_start_number - ship_end_number == - ship_len + 1):
            return 'horizontal'
    return False


def get_coords(ship_start, ship_end, level):
    alphabet = string.ascii_uppercase
    ship_start_letter, ship_start_number = ship_start[0], int(ship_start[1:]) - 1
    ship_start_letter_index = alphabet.index(ship_start_letter)
    ship_end_letter, ship_end_number = ship_end[0], int(ship_end[1:]) - 1
    ship_end_letter_index = alphabet.index(ship_end_letter)
    ship_coords = []
    if level == 'horizontal':
        for coord in range(ship_start_number, ship_end_number + 1):
            ship_coords.append(ship_start_letter + str(coord))
    else:
        for coord in range(ship_start_letter_index, ship_end_letter_index + 1):
            ship_coords.append(alphabet[coord] + str(ship_start_number))
    return ship_coords


def check_ship_location(ship_coords, player_battlefield, level):
    alphabet = string.ascii_uppercase
    # Sprawdzanie, czy w tym miejscu nie ma już innego statku
    for coord in ship_coords:
        row, col = coord[0], int(coord[1:])
        if player_battlefield[row][col] != '.':
            return False
    # Sprawdzanie, czy w sąsiedztwie nie ma innego statku
    for coord in ship_coords:
        row, col = coord[0], int(coord[1:])
        previous_row = alphabet[alphabet.index(row) - 1]
        next_row = alphabet[alphabet.index(row) + 1]
        # Sprawdzanie w poziomie
        if level == 'horizontal':
            # Sprawdzanie góra-dół w poziomie
            if 'A' < row < 'J':
                if player_battlefield[previous_row][col] == 's' or player_battlefield[next_row][col] == 's':
                    return False
                # Sprawdzanie góra-środek-dół na początku statku
                if 0 < col < 9 and coord == ship_coords[0]:
                    if (player_battlefield[previous_row][col - 1] == 's'
                            or player_battlefield[row][col - 1] == 's'
                            or player_battlefield[next_row][col - 1] == 's'):
                        return False
                # Sprawdzanie góra-środek-dół na końcu statku
                if 0 < col < 9 and coord == ship_coords[-1]:
                    if (player_battlefield[previous_row][col + 1] == 's'
                            or player_battlefield[row][col + 1] == 's'
                            or player_battlefield[next_row][col + 1] == 's'):
                        return False
            # Sprawdzanie, gdy statek jest przy górnej krawędzi planszy
            if row == 'A' and col != 0 and coord == ship_coords[0]:
                if (player_battlefield[row][col - 1] == 's'
                        or player_battlefield[next_row][col - 1] == 's'):
                    return False
            if row == 'A' and col != 9 and coord == ship_coords[-1]:
                if (player_battlefield[row][col + 1] == 's'
                        or player_battlefield[next_row][col + 1] == 's'):
                    return False
            if row == 'A':
                if player_battlefield[next_row][col] == 's':
                    return False
            # Sprawdzanie, gdy statek jest przy dolnej krawędzi planszy
            if row == 'J' and col != 0 and coord == ship_coords[0]:
                if (player_battlefield[row][col - 1] == 's'
                        or player_battlefield[previous_row][col - 1] == 's'):
                    return False
            if row == 'J' and col != 9 and coord == ship_coords[-1]:
                if (player_battlefield[row][col + 1] == 's'
                        or player_battlefield[previous_row][col + 1] == 's'):
                    return False
            if row == 'J':
                if player_battlefield[previous_row][col] == 's':
                    return False
        # Sprawdzanie statku w pionie
        else:
            # Sprawdzanie prawo-lewo w pionie
            if 0 < col < 9:
                if (player_battlefield[row][col - 1] == 's'
                        or player_battlefield[row][col + 1] == 's'):
                    return False
                # Sprawdzania góra-środek-dół na początku statku
                if 'A' < row < 'J' and coord == ship_coords[0]:
                    if (player_battlefield[previous_row][col - 1] == 's'
                            or player_battlefield[previous_row][col] == 's'
                            or player_battlefield[previous_row][col + 1] == 's'):
                        return False
                # Sprawdzania góra-środek-dół na końcu statku
                elif 'A' < row < 'J' and coord == ship_coords[-1]:
                    if (player_battlefield[next_row][col - 1] == 's'
                            or player_battlefield[next_row][col] == 's'
                            or player_battlefield[next_row][col + 1] == 's'):
                        return False
            # Sprawdzanie, gdy statek jest przy lewej krawędzi planszy
            if col == 0 and row != 'A' and coord == ship_coords[0]:
                if (player_battlefield[previous_row][col + 1] == 's'
                        or player_battlefield[previous_row][col] == 's'):
                    return False
            if col == 0 and row != 'J' and coord == ship_coords[-1]:
                if (player_battlefield[next_row][col + 1] == 's'
                        or player_battlefield[next_row][col] == 's'):
                    return False
            if col == 0:
                if player_battlefield[row][col + 1] == 's':
                    return False
            # Sprawdzanie, gdy statek jest przy prawej krawędzi planszy
            if col == 9 and row != 'A' and coord == ship_coords[0]:
                if (player_battlefield[previous_row][col] == 's'
                        or player_battlefield[previous_row][col - 1] == 's'):
                    return False
            if col == 9 and row != 'J' and coord == ship_coords[-1]:
                if (player_battlefield[next_row][col] == 's'
                        or player_battlefield[next_row][col - 1] == 's'):
                    return False
            if col == 9:
                if player_battlefield[row][col - 1] == 's':
                    return False
    return True


def put_ship_on_map(ship_coords, player_battlefield):
    for coord in ship_coords:
        row, col = coord[0], int(coord[1:])
        player_battlefield[row][col] = 's'
    return player_battlefield


def place_ships(ships_to_place, player_battlefield):
    while ships_to_place:
        ship_size = list(ships_to_place.keys())[0]
        ships_placed = 0
        while ships_placed < ships_to_place[ship_size]:
            start_pos, end_pos = get_ship_pos(ship_size)
            vertical_or_horizontal = check_ship_level(start_pos, end_pos, ship_size)
            if vertical_or_horizontal:
                print(start_pos, end_pos, vertical_or_horizontal)
                coords = get_coords(start_pos, end_pos, vertical_or_horizontal)
                print(check_ship_location(coords, player_battlefield, vertical_or_horizontal))
                if check_ship_location(coords, player_battlefield, vertical_or_horizontal):
                    player_battlefield = put_ship_on_map(coords, player_battlefield)
                    ships_placed += 1
                print_map(player_battlefield)
        ships_to_place.pop(ship_size)
    return player_battlefield


def shoot():
    coord = input('Podaj miejsce, w które chcesz oddać strzał: ')
    return coord


def check_shot(shot, player_battlefield):
    shot_letter, shot_number = shot[0], int(shot[1:])
    if player_battlefield[shot_letter][shot_number] == 's':
        return True
    return False


def update_map(shot, player_battlefield, ocean_battlefield):
    hit = check_shot(shot, player_battlefield)
    shot_letter, shot_number = shot[0], int(shot[1:])
    if hit:
        ocean_battlefield[shot_letter][shot_number] = 'x'
        player_battlefield[shot_letter][shot_number] = 'x'
    else:
        ocean_battlefield[shot_letter][shot_number] = 'o'
        player_battlefield[shot_letter][shot_number] = 'o'

if __name__ == "__main__":
    ship_board = generate_empty_map(10)
    print_map(ship_board)
    print_map(place_ships(generate_ships(), ship_board))
