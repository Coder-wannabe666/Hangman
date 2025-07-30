import string
import requests
import time

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

def get_secret_word():
    word_response = requests.get("https://random-word-api.vercel.app/api?words=1")
    base_word = word_response.json()[0]
    # base_word = "apple"
    return base_word

def get_word_definition(base_word):
    url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{base_word}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        try:
            first_definition = data[0]['meanings'][0]['definitions'][0]['definition']
            return first_definition
        except (KeyError, IndexError):
            return "Definition not found in response"
    else:
        return f"API error: {response.status_code}"


def play():

    used_letters = []
    for i in range(27):
        used_letters.append(0)

    print("Welcome to hangman!")
    print("Your task is to guess the given secret word")

    secret= get_secret_word()
    clue = get_word_definition(secret)

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
        print(f'The secret word was "{secret}"')
        time.sleep(5)
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
    # base_word = get_secret_word()
    # print(get_secret_word())
    # print(get_word_definition(base_word))
