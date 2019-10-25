import battleship_game
import random
import string
from battleship_game import Player


class Ai(Player):

    def generate_random_coords(self):
        while self.ships_to_place:
            ship_size = list(self.ships_to_place.keys())[0]
            ships_placed = 0
            while ships_placed < self.ships_to_place[ship_size]:
                horizontal_or_vertical = random.choice(['horizontal', 'vertical'])
                if horizontal_or_vertical == 'horizontal':
                    row = random.choice(string.ascii_uppercase[:10])
                    ship_start_number = random.randint(0, 11 - ship_size)
                    ship_end_number = ship_start_number + ship_size - 1
                    print(row, ship_start_number, ship_end_number)
                else:
                    col = random.randint(0, 10)
                    ship_start_letter = random.choice(string.ascii_uppercase[:11 - ship_size])
                    ship_start_letter_index = string.ascii_uppercase.index(ship_start_letter)
                    ship_end_letter = string.ascii_uppercase[ship_start_letter_index + ship_size - 1]
                    print(col, ship_start_letter, ship_end_letter)
                ships_placed += 1
            self.ships_to_place.pop(ship_size)


if __name__ == "__main__":
    print('Touchpad nie działa')
    Ai().generate_random_coords()
    print(Ai().ships_to_place)
