import string
import requests

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


alphabet = []
for i in string.ascii_lowercase:
    alphabet.append(i)

def get_secret_word_and_clue():
    word_response = requests.get("https://random-word-api.herokuapp.com/word")
    base_word = word_response.json()[0]
    clue = None
    return base_word, clue


def play():

    used_letters = []
    for i in range(27):
        used_letters.append(0)

    print("Welcome to hangman!")
    print("Your task is to guess the given secret word")

    secret, clue = get_secret_word_and_clue()


    arr_secret = []
    for i in secret:
        arr_secret.append(i)

    player_secret = ""

    for i in range(len(secret)):
        if secret[i] != " ":
            player_secret += "_"
        else:
            player_secret += " "

    number_of_mistakes = 0

    def lose():
        print("YOU LOST!!!!!")
        play()

    while True:
        if number_of_mistakes == 8:
            lose()

        print(player_secret)
        print(clue)
        used = ""
        for i in range(len(used_letters)):
            if used_letters[i] == 1:
                used += chr(i + 97)

        print(f'Used characters: {used}')
        given_char = get_chr(used_letters)

        if given_char in arr_secret:
            for i in range(len(secret)):
                if secret[i] == given_char:
                    player_secret = player_secret[:i] + given_char + player_secret[i+1:]
            if "_" not in player_secret:
                print("YOU WON!!!")
                print(f'The secret word was "{secret}" ')
                play()
        else:
            number_of_mistakes +=1
            print(f'You have {8-number_of_mistakes} lives left')

if __name__ == "__main__":
    play()
    # print(get_secret_word_and_clue())
