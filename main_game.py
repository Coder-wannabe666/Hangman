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

clue = "gduckling"

arr_clue = []
for i in clue:
    arr_clue.append(i)

running = True
number_of_mistakes = 0

while running == True:
    if number_of_mistakes == 8:
        running = False

    given_char = get_chr(used_letters)

    if given_char in arr_clue:
        print("test")
    else:
        number_of_mistakes +=1

