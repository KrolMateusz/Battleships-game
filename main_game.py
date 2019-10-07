def generate_map(size):
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


if __name__ == "__main__":
    print_map(generate_map(10))
