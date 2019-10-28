import random
import string
import itertools
import time
from battleship_game import Player


class Ai(Player):

    def generate_random_coords(self, vertical_or_horizontal):
        ship_size = list(self.ships_to_place.keys())[0]
        # Losowanie koordynatów, gdy statek jest ustawiony poziomo
        if vertical_or_horizontal == 'horizontal':
            row = random.choice(string.ascii_uppercase[:10])
            ship_start_number = random.randint(1, 11 - ship_size)
            ship_end_number = ship_start_number + ship_size - 1
            start_pos = row + str(ship_start_number)
            end_pos = row + str(ship_end_number)
        # Losowanie koordynatów, gdy statek jest ustawiony pionowo
        else:
            col = random.randint(1, 10)
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

    def random_shooting(self):
        if self.coords_to_shoot:
            shot_tuple = random.choice(self.coords_to_shoot)
            self.shot = shot_tuple[0] + str(shot_tuple[1])
            self.coords_to_shoot.remove(shot_tuple)

    def shot_top(self):
        shot_letter, shot_number = self.previous_hit[0], int(self.previous_hit[1:])
        shot_letter_index = string.ascii_uppercase.index(shot_letter)
        self.shot = string.ascii_uppercase[shot_letter_index - 1] + str(shot_number)

    def shot_right(self):
        shot_letter, shot_number = self.previous_hit[0], int(self.previous_hit[1:])
        self.shot = shot_letter + str(shot_number + 1)

    def shot_bot(self):
        shot_letter, shot_number = self.previous_hit[0], int(self.previous_hit[1:])
        shot_letter_index = string.ascii_uppercase.index(shot_letter)
        self.shot = string.ascii_uppercase[shot_letter_index + 1] + str(shot_number)

    def shot_left(self):
        shot_letter, shot_number = self.previous_hit[0], int(self.previous_hit[1:])
        self.shot = shot_letter + str(shot_number - 1)

    def check_top(self):
        shot_letter, shot_number = self.previous_hit[0], int(self.previous_hit[1:])
        if shot_letter == 'A':
            return False
        shot_letter_index = string.ascii_uppercase.index(shot_letter)
        previous_letter = string.ascii_uppercase[shot_letter_index - 1]
        if self.shot_grid[previous_letter][shot_number] == '.':
            return True
        return False

    def check_right(self):
        shot_letter, shot_number = self.previous_hit[0], int(self.previous_hit[1:])
        if shot_number == 9:
            return False
        if self.shot_grid[shot_letter][shot_number + 1] == '.':
            return True
        return False

    def check_bot(self):
        shot_letter, shot_number = self.previous_hit[0], int(self.previous_hit[1:])
        if shot_letter == 'J':
            return False
        shot_letter_index = string.ascii_uppercase.index(shot_letter)
        next_letter = string.ascii_uppercase[shot_letter_index + 1]
        if self.shot_grid[next_letter][shot_number] == '.':
            return True
        return False

    def check_left(self):
        shot_letter, shot_number = self.previous_hit[0], int(self.previous_hit[1:])
        if shot_number == 0:
            return False
        if self.shot_grid[shot_letter][shot_number - 1] == '.':
            return True
        return False

    def check_directions(self):
        self.directions = []
        if self.check_top():
            self.directions.append('top')
        if self.check_right():
            self.directions.append('right')
        if self.check_bot():
            self.directions.append('bot')
        if self.check_left():
            self.directions.append('left')

    def hunt(self):
        self.check_directions()
        direction = self.directions[0]
        if direction == 'top':
            self.shot_top()
        elif direction == 'right':
            self.shot_right()
        elif direction == 'bot':
            self.shot_bot()
        else:
            self.shot_left()
        self.update_shot()
        shot_tuple = (self.shot[0], int(self.shot[1:]))
        if shot_tuple in self.coords_to_shoot:
            self.coords_to_shoot.remove(shot_tuple)

    def update_shot(self):
        self.shot = self.shot[0] + str(int(self.shot[1:]) + 1)

    def __init__(self):
        super().__init__()
        self.coords_to_shoot = list(itertools.product(string.ascii_uppercase[:10], range(1, 11)))
        self.previous_hits = []
        self.previous_hit = ''
        self.previous_shot = ''
        self.directions = []


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
        if any([player_1.previous_shot in key for key in player_2.ship_list]):
            player_1.previous_hit = player_1.previous_shot
            player_1.previous_hits.append(player_1.previous_shot)
            player_1.hunt()
            print(player_2.ship_list)
            print(f'shot: {player_1.shot}, coords to shoot: {player_1.coords_to_shoot}\n')
            player_1.print_map(player_1.shot_grid)
            player_2.print_map(player_2.ship_grid)
            time.sleep(10)
        else:
            player_1.random_shooting()
        player_1.update_map(player_2.ship_grid, player_2.ship_list)
        player_1.previous_shot = player_1.shot
        if player_2.end_game():
            print('Gracz 1 wygrywa!')
            player_2.print_map(player_2.ship_grid)
            break
        # Gracz drugi oddaje strzał
        player_2.random_shooting()
        player_2.update_map(player_1.ship_grid, player_1.ship_list)
        if player_1.end_game():
            print('Gracz 2 wygrywa!')
            player_1.print_map(player_1.ship_grid)
            break


def play_games(number_of_games):
    for _ in range(number_of_games):
        main()


if __name__ == "__main__":
    start = time.time()
    play_games(1)
    print(f'Czas wykonywania programu: {time.time() - start} s')
