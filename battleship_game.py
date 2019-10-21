import string


class Player:

    ship_list = {}

    @staticmethod
    def generate_empty_map(size):
        player_battlefield = {}
        for letter in 'ABCDEFGHIJ':
            player_battlefield[letter] = ["." for _ in range(size)]
        return player_battlefield

    @staticmethod
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

    @staticmethod
    def generate_ships():
        player_ships = {
            5: 1,
            4: 1,
            3: 2,
            2: 1,
        }
        return player_ships

    @staticmethod
    def get_ship_pos(ship_len):
        print('Podaj pozycję statku o rozmiarze ', ship_len)
        start_pos, end_pos = input('Podaj pozycję początkową oraz końcową: ').upper().split()
        if end_pos[0] < start_pos[0]:
            start_pos, end_pos = end_pos, start_pos
        elif int(end_pos[1:]) < int(start_pos[1:]):
            start_pos, end_pos = end_pos, start_pos
        return start_pos, end_pos

    @staticmethod
    def check_ship_level(ship_start, ship_end, ship_len):
        alphabet = string.ascii_uppercase
        ship_start_letter, ship_start_number = ship_start[0], int(ship_start[1:]) - 1
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

    @staticmethod
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

    def check_ship_location(self, ship_coords, level):
        alphabet = string.ascii_uppercase
        # Sprawdzanie, czy w tym miejscu nie ma już innego statku
        for coord in ship_coords:
            row, col = coord[0], int(coord[1:])
            if self.ship_grid[row][col] != '.':
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
                    if (self.ship_grid[previous_row][col] == 's' or
                            self.ship_grid[next_row][col] == 's'):
                        return False
                    # Sprawdzanie góra-środek-dół na początku statku
                    if 0 < col < 9 and coord == ship_coords[0]:
                        if (self.ship_grid[previous_row][col - 1] == 's' or
                                self.ship_grid[row][col - 1] == 's' or
                                self.ship_grid[next_row][col - 1] == 's'):
                            return False
                    # Sprawdzanie góra-środek-dół na końcu statku
                    if 0 < col < 9 and coord == ship_coords[-1]:
                        if (self.ship_grid[previous_row][col + 1] == 's' or
                                self.ship_grid[row][col + 1] == 's' or
                                self.ship_grid[next_row][col + 1] == 's'):
                            return False
                # Sprawdzanie, gdy statek jest przy górnej krawędzi planszy
                if row == 'A' and col != 0 and coord == ship_coords[0]:
                    if (self.ship_grid[row][col - 1] == 's' or
                            self.ship_grid[next_row][col - 1] == 's'):
                        return False
                if row == 'A' and col != 9 and coord == ship_coords[-1]:
                    if (self.ship_grid[row][col + 1] == 's' or
                            self.ship_grid[next_row][col + 1] == 's'):
                        return False
                if row == 'A':
                    if self.ship_grid[next_row][col] == 's':
                        return False
                # Sprawdzanie, gdy statek jest przy dolnej krawędzi planszy
                if row == 'J' and col != 0 and coord == ship_coords[0]:
                    if (self.ship_grid[row][col - 1] == 's' or
                            self.ship_grid[previous_row][col - 1] == 's'):
                        return False
                if row == 'J' and col != 9 and coord == ship_coords[-1]:
                    if (self.ship_grid[row][col + 1] == 's' or
                            self.ship_grid[previous_row][col + 1] == 's'):
                        return False
                if row == 'J':
                    if self.ship_grid[previous_row][col] == 's':
                        return False
            # Sprawdzanie statku w pionie
            else:
                # Sprawdzanie prawo-lewo w pionie
                if 0 < col < 9:
                    if (self.ship_grid[row][col - 1] == 's' or
                            self.ship_grid[row][col + 1] == 's'):
                        return False
                    # Sprawdzania góra-środek-dół na początku statku
                    if 'A' < row < 'J' and coord == ship_coords[0]:
                        if (self.ship_grid[previous_row][col - 1] == 's' or
                                self.ship_grid[previous_row][col] == 's' or
                                self.ship_grid[previous_row][col + 1] == 's'):
                            return False
                    # Sprawdzania góra-środek-dół na końcu statku
                    elif 'A' < row < 'J' and coord == ship_coords[-1]:
                        if (self.ship_grid[next_row][col - 1] == 's' or
                                self.ship_grid[next_row][col] == 's' or
                                self.ship_grid[next_row][col + 1] == 's'):
                            return False
                # Sprawdzanie, gdy statek jest przy lewej krawędzi planszy
                if col == 0 and row != 'A' and coord == ship_coords[0]:
                    if (self.ship_grid[previous_row][col + 1] == 's' or
                            self.ship_grid[previous_row][col] == 's'):
                        return False
                if col == 0 and row != 'J' and coord == ship_coords[-1]:
                    if (self.ship_grid[next_row][col + 1] == 's' or
                            self.ship_grid[next_row][col] == 's'):
                        return False
                if col == 0:
                    if self.ship_grid[row][col + 1] == 's':
                        return False
                # Sprawdzanie, gdy statek jest przy prawej krawędzi planszy
                if col == 9 and row != 'A' and coord == ship_coords[0]:
                    if (self.ship_grid[previous_row][col] == 's' or
                            self.ship_grid[previous_row][col - 1] == 's'):
                        return False
                if col == 9 and row != 'J' and coord == ship_coords[-1]:
                    if (self.ship_grid[next_row][col] == 's' or
                            self.ship_grid[next_row][col - 1] == 's'):
                        return False
                if col == 9:
                    if self.ship_grid[row][col - 1] == 's':
                        return False
        return True

    def put_ship_on_map(self, ship_coords):
        for coord in ship_coords:
            row, col = coord[0], int(coord[1:])
            self.ship_grid[row][col] = 's'

    def place_ships(self):
        while self.ships_to_place:
            ship_size = list(self.ships_to_place.keys())[0]
            ships_placed = 0
            while ships_placed < self.ships_to_place[ship_size]:
                start_pos, end_pos = self.get_ship_pos(ship_size)
                vertical_or_horizontal = self.check_ship_level(start_pos, end_pos, ship_size)
                if vertical_or_horizontal:
                    coords = self.get_coords(start_pos, end_pos, vertical_or_horizontal)
                    if self.check_ship_location(coords, vertical_or_horizontal):
                        self.put_ship_on_map(coords)
                        self.ship_list[tuple(coords)] = []
                        for _ in range(ship_size):
                            self.ship_list[tuple(coords)].append('.')
                        ships_placed += 1
                    self.print_map(self.ship_grid)
            self.ships_to_place.pop(ship_size)

    def shoot(self):
        self.shot = input('Podaj miejsce, w które chcesz oddać strzał: ').upper()

    def check_shot(self, oponent_grid):
        shot_letter, shot_number = self.shot[0], int(self.shot[1:]) - 1
        if oponent_grid[shot_letter][shot_number] == 's':
            return True
        return False

    @staticmethod
    def update_player_sunk_ships(oponent_ships):
        for ship, ship_fragments in oponent_ships.items():
            if all([fragment == 'x' for fragment in ship_fragments]):
                oponent_ships[ship] = ['#' for _ in ship_fragments]

    def update_map(self, oponent_grid, oponent_ships):
        hit = self.check_shot(oponent_grid)
        shot_letter, shot_number = self.shot[0], int(self.shot[1:]) - 1
        self.shot = shot_letter + str(shot_number)
        if oponent_grid[shot_letter][shot_number] == '#':
            return None
        if hit:
            self.shot_grid[shot_letter][shot_number] = 'x'
            oponent_grid[shot_letter][shot_number] = 'x'
            for ship, ship_fragments in oponent_ships.items():
                if self.shot in ship:
                    ship_fragments[ship.index(self.shot)] = 'x'
        else:
            self.shot_grid[shot_letter][shot_number] = 'o'
            oponent_grid[shot_letter][shot_number] = 'o'
        self.update_player_sunk_ships(oponent_ships)
        for ship, ship_fragments in oponent_ships.items():
            if all([shot == '#' for shot in ship_fragments]):
                for row, col in ship:
                    self.shot_grid[row][int(col)] = '#'
                    oponent_grid[row][int(col)] = '#'

    def end_game(self):
        ships_sunk = []
        for _, ship_fragments in self.ship_list.items():
            if all([shot == '#' for shot in ship_fragments]):
                ships_sunk.append(True)
            else:
                ships_sunk.append(False)
        if all(ships_sunk):
            return True
        return False

    def __init__(self):
        self.ship_grid = self.generate_empty_map(10)
        self.shot_grid = self.generate_empty_map(10)
        self.ships_to_place = self.generate_ships()
        self.ship_list = {}


def main():
    player_1 = Player()
    player_2 = Player()
    # Gracz 1 ustawia statki
    print('Gracz 1 wykonuje ruch')
    player_1.print_map(player_1.ship_grid)
    player_1.place_ships()
    # Gracz 2 ustawia statki
    print('Gracz 2 wykonuje ruch')
    player_2.print_map(player_2.ship_grid)
    player_2.place_ships()
    # Gra się toczy, dopóki wszystki statki jednego z graczy nie zostaną zatopione
    while True:
        # Gracz 1 oddaje strzał
        print('Gracz 1 wykonuje ruch')
        player_1.shoot()
        player_1.update_map(player_2.ship_grid, player_2.ship_list)
        player_1.print_map(player_1.ship_grid)
        player_1.print_map(player_1.shot_grid)
        if player_2.end_game():
            print('Gracz 1 wygrywa!')
            break
        # Gracz drugi oddaje strzał
        print('Gracz 2 wykonuje ruch')
        player_2.shoot()
        player_2.update_map(player_1.ship_grid, player_1.ship_list)
        player_2.print_map(player_2.ship_grid)
        player_2.print_map(player_2.shot_grid)
        if player_1.end_game():
            print('Gracz 2 wygrywa!')
            break


if __name__ == '__main__':
    main()
