import string

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
        3: 3,
        2: 2,
    }
    return ships


def check_ship_level(ship_start, ship_end, ship_len):
    alphabet = string.ascii_uppercase
    ship_start_letter, ship_start_number = ship_start[0], ship_start[1:]
    ship_start_letter_index = alphabet.index(ship_start_letter)
    ship_end_letter, ship_end_number = ship_end[0], ship_end[1:]
    ship_end_letter_index = alphabet.index(ship_end_letter)
    # Walidacja pionowa
    if ship_start_number == ship_end_number:
        if (ship_start_letter_index - ship_end_letter_index == ship_len - 1 or
                ship_start_letter_index - ship_end_letter_index == -ship_len + 1):
            return 'vertical'
    # Walidacja pozioma
    if ship_start_letter == ship_end_letter:
        if (int(ship_start_number) - int(ship_end_number) == ship_len - 1 or
                int(ship_start_number) - int(ship_end_number) == -ship_len + 1):
            return 'horizontal'
    return False


def get_coords(ship_start, ship_end, level):
    alphabet = string.ascii_uppercase
    ship_start_letter, ship_start_number = ship_start[0], ship_start[1:]
    ship_start_letter_index = alphabet.index(ship_start_letter)
    ship_end_letter, ship_end_number = ship_end[0], ship_end[1:]
    ship_end_letter_index = alphabet.index(ship_end_letter)
    ship_coords = []
    if level == 'horizontal':
        for coord in range(int(ship_start_number), int(ship_end_number) + 1):
            ship_coords.append(ship_start_letter + str(coord))
    else:
        for coord in range(ship_start_letter_index, ship_end_letter_index + 1):
            ship_coords.append(alphabet[coord] + str(ship_start_number))
    return ship_coords


def check_ship_location(ship_coords, battlefield, level):
    alphabet = string.ascii_uppercase
    # Sprawdzanie, czy w tym miejscu nie ma już innego statku
    for coord in ship_coords:
        row, col = coord[0], int(coord[1:])
        if battlefield[row][col] != '.':
            return False
    # Sprawdzanie, czy w sąsiedztwie nie ma innego statku
    for coord in ship_coords:
        previous_row = alphabet[alphabet.index(row) - 1]
        next_row = alphabet[alphabet.index(row) + 1]
        # Sprawdzanie w poziomie
        if level == 'horizontal':
            # Sprawdzanie góra-dół w poziomie
            if 'A' < row < 'J':
                if battlefield[previous_row][col] == 's' or battlefield[next_row][col] == 's':
                    return False
                # Sprawdzanie góra-środek-dół na początku statku
                if 1 < col < 10 and coord == ship_coords[0]:
                    if (battlefield[previous_row][col - 1] == 's'
                            or battlefield[row][col - 1] == 's'
                            or battlefield[next_row][col - 1] == 's'):
                        return False
                # Sprawdzanie góra-środek-dół na końcu statku
                if 1 < col < 10 and coord == ship_coords[-1]:
                    if (battlefield[previous_row][col + 1] == 's'
                            or battlefield[row][col + 1] == 's'
                            or battlefield[next_row][col + 1] == 's'):
                        return False
            # Sprawdzanie, gdy statek jest przy lewej krawędzi planszy
            if row == 'A':
                if battlefield[next_row][col] == 's':
                    return False
            # Sprawdzanie, gdy statek jest przy prawej krawędzi planszy
            if row == 'J':
                if battlefield[previous_row][col] == 's':
                    return False
        else:
            # Sprawdzanie prawo-lewo w pionie
            if 1 < col < 10:
                if battlefield[row][col - 1] == 's' or battlefield[row][col + 1] == 's':
                    return False
                # Sprawdzania góra-środek-dół na początku statku
                if 'A' < row < 'J' and coord == ship_coords[0]:
                    if (battlefield[previous_row][col - 1] == 's'
                            or battlefield[previous_row][col] == 's'
                            or battlefield[previous_row][col + 1] == 's'):
                        return False
                # Sprawdzania góra-środek-dół na końcu statku
                elif 'A' < row < 'J' and coord == ship_coords[-1]:
                    if (battlefield[next_row][col - 1] == 's'
                            or battlefield[next_row][col] == 's'
                            or battlefield[next_row][col + 1] == 's'):
                        return False
            # Sprawdzanie, gdy statek jest przy górnej krawędzi planszy
            if col == 1:
                if battlefield[row][col + 1] == 's':
                    return False
            # Sprawdzanie, gdy statek jest przy dolnej krawędzi planszy
            if col == 10:
                if battlefield[row][col - 1] == 's':
                    return False
    return True


def put_ship_on_board(ship_coords, battlefield):
    for coord in ship_coords:
        row, col = coord[0], int(coord[1:])
        battlefield[row][col] = 's'
    return battlefield


def place_ships(ships_to_place, battlefield):
    while ships_to_place:
        ship_size = list(ships_to_place.keys())[0]
        ships_placed = 0
        while ships_placed < ships_to_place[ship_size]:
            print('Podaj pozycję statku o rozmiarze ', ship_size)
            start_pos, end_pos = input('Podaj pozycję początkową oraz końcową: ').upper().split()
            vertical_or_horizontal = check_ship_level(start_pos, end_pos, ship_size)
            if vertical_or_horizontal:
                print(start_pos, end_pos, vertical_or_horizontal)
                coords = get_coords(start_pos, end_pos, vertical_or_horizontal)
                print(check_ship_location(coords, battlefield, vertical_or_horizontal))
                if check_ship_location(coords, battlefield, vertical_or_horizontal):
                    battlefield = put_ship_on_board(coords, battlefield)
                    ships_placed += 1
                print_map(battlefield)
        ships_to_place.pop(ship_size)


if __name__ == "__main__":
    ship_board = generate_empty_map(10)
    print_map(ship_board)
    place_ships(generate_ships(), ship_board)
