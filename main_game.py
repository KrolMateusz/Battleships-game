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


def check_arrangement(ship_start, ship_end, ship_len):
    alphabet = string.ascii_uppercase
    ship_start_letter, ship_start_number = ship_start
    ship_start_letter_index = alphabet.index(ship_start_letter)
    ship_end_letter, ship_end_number = ship_end
    ship_end_letter_index = alphabet.index(ship_end_letter)
    # Walidacja pozioma
    if ship_start_number == ship_end_number:
        if (ship_start_letter_index - ship_end_letter_index == ship_len - 1 or 
                ship_start_letter_index - ship_end_letter_index == -ship_len + 1):
            return True
    # Walidacja pionowa
    if ship_start_letter == ship_end_letter:
        if (int(ship_start_number) - int(ship_end_number) == ship_len - 1 or
                int(ship_start_number) - int(ship_end_number) == -ship_len + 1):
            return True
    return False


def place_ships(ships_to_place):
    while ships_to_place:
        ship_size = list(ships_to_place.keys())[0]
        ship_placed = 0
        while ship_placed < ships_to_place[ship_size]:
            print('Podaj pozycję statku o rozmiarze ', ship_size)
            start_pos, end_pos = input('Podaj pozycję początkową oraz końcową: ').upper().split()
            if check_arrangement(start_pos, end_pos, ship_size):
                ship_placed += 1
                print(start_pos, end_pos)
        ships_to_place.pop(ship_size)


if __name__ == "__main__":
    print_map(generate_empty_map(10))
    place_ships(generate_ships())
