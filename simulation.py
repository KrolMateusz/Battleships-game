import random
import string
import itertools
import time
from battleship_game import Player


class Ai(Player):

    def generate_random_coords(self, vertical_or_horizontal):
        ship_size = list(self.ships_to_place.keys())[0]
        if vertical_or_horizontal == 'horizontal':
            row = random.choice(string.ascii_uppercase[:10])
            ship_start_number = random.randint(1, 11 - ship_size)
            ship_end_number = ship_start_number + ship_size - 1
            start_pos = row + str(ship_start_number)
            end_pos = row + str(ship_end_number)
        else:
            col = random.randint(0, 10)
            ship_start_letter = random.choice(string.ascii_uppercase[:11 - ship_size])
            ship_start_letter_index = string.ascii_uppercase.index(ship_start_letter)
            ship_end_letter = string.ascii_uppercase[ship_start_letter_index + ship_size - 1]
            start_pos = ship_start_letter + str(col)
            end_pos = ship_end_letter + str(col)
        return start_pos, end_pos

    def place_ships(self):
        while self.ships_to_place:
            ship_size = list(self.ships_to_place.keys())[0]
            ships_placed = 0
            while ships_placed < self.ships_to_place[ship_size]:
                vertical_or_horizontal = random.choice(['horizontal', 'vertical'])
                start_pos, end_pos = self.generate_random_coords(vertical_or_horizontal)
                coords = self.get_coords(start_pos, end_pos, vertical_or_horizontal)
                if self.check_ship_location(coords, vertical_or_horizontal):
                    self.put_ship_on_map(coords)
                    self.ship_list[tuple(coords)] = []
                    for _ in range(ship_size):
                        self.ship_list[tuple(coords)].append('.')
                    ships_placed += 1
            self.ships_to_place.pop(ship_size)

    def shoot(self):
        if self.coords_to_shoot:
            shot_tuple = random.choice(self.coords_to_shoot)
            self.shot = shot_tuple[0] + str(shot_tuple[1])
            self.coords_to_shoot.remove(shot_tuple)

    def __init__(self):
        super().__init__()
        self.coords_to_shoot = list(itertools.product(string.ascii_uppercase[:10], range(1, 11)))


def main():
    player_1 = Ai()
    player_2 = Ai()
    # Gracz 1 ustawia statki
    player_1.place_ships()
    # Gracz 2 ustawia statki
    player_2.place_ships()
    # Gra się toczy, dopóki wszystki statki jednego z graczy nie zostaną zatopione
    while True:
        # Gracz 1 oddaje strzał
        player_1.shoot()
        player_1.update_map(player_2.ship_grid, player_2.ship_list)
        if player_2.end_game() or not player_1.coords_to_shoot:
            print('Gracz 1 wygrywa!')
            player_1.update_map(player_2.ship_grid, player_2.ship_list)
            player_2.print_map(player_2.ship_grid)
            print(player_2.ship_list)
            break
        # Gracz drugi oddaje strzał
        player_2.shoot()
        player_2.update_map(player_1.ship_grid, player_1.ship_list)
        if player_1.end_game() or not player_2.coords_to_shoot:
            print('Gracz 2 wygrywa!')
            player_2.update_map(player_1.ship_grid, player_1.ship_list)
            player_1.print_map(player_1.ship_grid)
            print(player_1.ship_list)
            break


def play_games(number_of_games):
    for _ in range(number_of_games):
        main()


if __name__ == "__main__":
    start = time.time()
    play_games(1000)
    print(f'Czas wykonywania programu to {time.time() - start} s')
