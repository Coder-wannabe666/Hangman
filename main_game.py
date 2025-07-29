import string

def get_chr(used_letters):
    given_char = input("Input a character: ")
    given_char = given_char.lower()
    while given_char not in alphabet:
        print("You need to input a letter from the alphabet!")
        given_char = get_chr(used_letters)
    if used_letters[ord(given_char) - 97] == 1:
        print("You need to input a letter from the alphabet that was not used before!")
        given_char = get_chr(used_letters)
    used_letters[ord(given_char) - 97] = 1
    return given_char

used_letters = []
alphabet = []
for i in string.ascii_lowercase:
    alphabet.append(i)

for i in range(27):
    used_letters.append(0)

print("Welcome to hangman!")
print("Your task is to guess the given clue")

clue = "picky eater"

arr_clue = []
for i in clue:
    arr_clue.append(i)

running = True
number_of_mistakes = 0

player_clue = ""

for i in range(len(clue)):
    if clue[i] != " ":
        player_clue += "_"
    else:
        player_clue += " "

while running == True:
    if number_of_mistakes == 8:
        print("YOU LOST!!!!!")
        running = False

    print(player_clue)

    given_char = get_chr(used_letters)

    if given_char in arr_clue:
        for i in range(len(clue)):
            if clue[i] == given_char:
                player_clue = player_clue[:i] + given_char + player_clue[i+1:]
        if "_" not in player_clue:
            print("YOU WON!!!")
            print(f'The clue was "{clue}" ')
            running = False
    else:
        number_of_mistakes +=1
        print(f'You have {7-number_of_mistakes} lives left')

