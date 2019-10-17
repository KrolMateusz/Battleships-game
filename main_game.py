import string


def generate_empty_map(size):
    battlefield = {}
    for letter in 'ABCDEFGHIJ':
        battlefield[letter] = ["." for _ in range(size)]
    return battlefield


def print_map(player_battlefield):
    print(end='  ')
    for number in range(len(player_battlefield)):
        print(number + 1, end='  ')
        if number + 1 == len(player_battlefield):
            print()
    for row in player_battlefield:
        print(row, end=' ')
        for col in range(len(player_battlefield)):
            print(player_battlefield[row][col], end='  ')
        print()


def generate_ships():
    player_ships = {
        5: 1,
        4: 1,
        3: 2,
        2: 1,
    }
    return player_ships


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
                if (player_battlefield[previous_row][col] == 's' or
                        player_battlefield[next_row][col] == 's'):
                    return False
                # Sprawdzanie góra-środek-dół na początku statku
                if 0 < col < 9 and coord == ship_coords[0]:
                    if (player_battlefield[previous_row][col - 1] == 's' or
                            player_battlefield[row][col - 1] == 's' or
                            player_battlefield[next_row][col - 1] == 's'):
                        return False
                # Sprawdzanie góra-środek-dół na końcu statku
                if 0 < col < 9 and coord == ship_coords[-1]:
                    if (player_battlefield[previous_row][col + 1] == 's' or
                            player_battlefield[row][col + 1] == 's' or
                            player_battlefield[next_row][col + 1] == 's'):
                        return False
            # Sprawdzanie, gdy statek jest przy górnej krawędzi planszy
            if row == 'A' and col != 0 and coord == ship_coords[0]:
                if (player_battlefield[row][col - 1] == 's' or
                        player_battlefield[next_row][col - 1] == 's'):
                    return False
            if row == 'A' and col != 9 and coord == ship_coords[-1]:
                if (player_battlefield[row][col + 1] == 's' or
                        player_battlefield[next_row][col + 1] == 's'):
                    return False
            if row == 'A':
                if player_battlefield[next_row][col] == 's':
                    return False
            # Sprawdzanie, gdy statek jest przy dolnej krawędzi planszy
            if row == 'J' and col != 0 and coord == ship_coords[0]:
                if (player_battlefield[row][col - 1] == 's' or
                        player_battlefield[previous_row][col - 1] == 's'):
                    return False
            if row == 'J' and col != 9 and coord == ship_coords[-1]:
                if (player_battlefield[row][col + 1] == 's' or
                        player_battlefield[previous_row][col + 1] == 's'):
                    return False
            if row == 'J':
                if player_battlefield[previous_row][col] == 's':
                    return False
        # Sprawdzanie statku w pionie
        else:
            # Sprawdzanie prawo-lewo w pionie
            if 0 < col < 9:
                if (player_battlefield[row][col - 1] == 's' or
                        player_battlefield[row][col + 1] == 's'):
                    return False
                # Sprawdzania góra-środek-dół na początku statku
                if 'A' < row < 'J' and coord == ship_coords[0]:
                    if (player_battlefield[previous_row][col - 1] == 's' or
                            player_battlefield[previous_row][col] == 's' or
                            player_battlefield[previous_row][col + 1] == 's'):
                        return False
                # Sprawdzania góra-środek-dół na końcu statku
                elif 'A' < row < 'J' and coord == ship_coords[-1]:
                    if (player_battlefield[next_row][col - 1] == 's' or
                            player_battlefield[next_row][col] == 's' or
                            player_battlefield[next_row][col + 1] == 's'):
                        return False
            # Sprawdzanie, gdy statek jest przy lewej krawędzi planszy
            if col == 0 and row != 'A' and coord == ship_coords[0]:
                if (player_battlefield[previous_row][col + 1] == 's' or
                        player_battlefield[previous_row][col] == 's'):
                    return False
            if col == 0 and row != 'J' and coord == ship_coords[-1]:
                if (player_battlefield[next_row][col + 1] == 's' or
                        player_battlefield[next_row][col] == 's'):
                    return False
            if col == 0:
                if player_battlefield[row][col + 1] == 's':
                    return False
            # Sprawdzanie, gdy statek jest przy prawej krawędzi planszy
            if col == 9 and row != 'A' and coord == ship_coords[0]:
                if (player_battlefield[previous_row][col] == 's' or
                        player_battlefield[previous_row][col - 1] == 's'):
                    return False
            if col == 9 and row != 'J' and coord == ship_coords[-1]:
                if (player_battlefield[next_row][col] == 's' or
                        player_battlefield[next_row][col - 1] == 's'):
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
    ship_list = {}
    while ships_to_place:
        ship_size = list(ships_to_place.keys())[0]
        ships_placed = 0
        while ships_placed < ships_to_place[ship_size]:
            start_pos, end_pos = get_ship_pos(ship_size)
            vertical_or_horizontal = check_ship_level(start_pos, end_pos, ship_size)
            if vertical_or_horizontal:
                coords = get_coords(start_pos, end_pos, vertical_or_horizontal)
                if check_ship_location(coords, player_battlefield, vertical_or_horizontal):
                    player_battlefield = put_ship_on_map(coords, player_battlefield)
                    ship_list[tuple(coords)] = []
                    for _ in range(ship_size):
                        ship_list[tuple(coords)].append('.')
                    ships_placed += 1
                print_map(player_battlefield)
        ships_to_place.pop(ship_size)
    return player_battlefield, ship_list


def shoot():
    coord = input('Podaj miejsce, w które chcesz oddać strzał: ')
    return coord.upper()


def check_shot(shot, player_battlefield):
    shot_letter, shot_number = shot[0], int(shot[1:]) - 1
    if player_battlefield[shot_letter][shot_number] == 's':
        return True
    return False


def update_player_sunk_ships(player_ships):
    for ship, ship_fragments in player_ships.items():
        if all([fragment == 'x' for fragment in ship_fragments]):
            player_ships[ship] = ['#' for _ in ship_fragments]


def update_map(shot, oponent_battlefield, oponent_ships, player_ocean_battlefield):
    hit = check_shot(shot, oponent_battlefield)
    shot_letter, shot_number = shot[0], int(shot[1:]) - 1
    shot = shot_letter + str(shot_number)
    if oponent_battlefield[shot_letter][shot_number] == '#':
        return None
    if hit:
        player_ocean_battlefield[shot_letter][shot_number] = 'x'
        oponent_battlefield[shot_letter][shot_number] = 'x'
        for ship, ship_fragments in oponent_ships.items():
            if shot in ship:
                ship_fragments[ship.index(shot)] = 'x'
    else:
        player_ocean_battlefield[shot_letter][shot_number] = 'o'
        oponent_battlefield[shot_letter][shot_number] = 'o'
    update_player_sunk_ships(oponent_ships)
    for ship, ship_fragments in oponent_ships.items():
        if all([shot == '#' for shot in ship_fragments]):
            for row, col in ship:
                player_ocean_battlefield[row][int(col)] = '#'
                oponent_battlefield[row][int(col)] = '#'


def end_game(player_ships):
    ships_sunk = []
    for _, ship_fragments in player_ships.items():
        if all([shot == '#' for shot in ship_fragments]):
            ships_sunk.append(True)
        else:
            ships_sunk.append(False)
    if all(ships_sunk):
        return True
    return False


def main():
    ship_board_1 = generate_empty_map(10)
    shot_board_1 = generate_empty_map(10)
    ship_board_2 = generate_empty_map(10)
    shot_board_2 = generate_empty_map(10)
    # Gracz 1 ustawia statki
    print('Gracz 1 wykonuje ruch')
    print_map(ship_board_1)
    ship_board_1, ships_1 = place_ships(generate_ships(), ship_board_1)
    # Gracz 2 ustawia statki
    print('Gracz 2 wykonuje ruch')
    print_map(ship_board_2)
    ship_board_2, ships_2 = place_ships(generate_ships(), ship_board_2)
    # Gra się toczy, dopóki wszystki statki jednego z graczy nie zostaną zatopione
    while True:
        # Gracz 1 oddaje strzał
        print('Gracz 1 wykonuje ruch')
        shot_coord_1 = shoot()
        update_map(shot_coord_1, ship_board_2, ships_2, shot_board_1)
        print_map(ship_board_1)
        print_map(shot_board_1)
        if end_game(ships_2):
            print('Gracz 1 wygrywa!')
            break
        # Gracz drugi oddaje strzał
        print('Gracz 2 wykonuje ruch')
        shot_coord_2 = shoot()
        update_map(shot_coord_2, ship_board_1, ships_1, shot_board_2)
        print_map(ship_board_2)
        print_map(shot_board_2)
        if end_game(ships_1):
            print('Gracz 2 wygrywa!')
            break


if __name__ == "__main__":
    # print_map(generate_empty_map(10))
    main()
