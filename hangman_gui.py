import string
import requests
import tkinter as tk
from tkinter import messagebox

class HangmanGame:
    def __init__(self):
        self.alphabet = list(string.ascii_lowercase)
        self.reset_game()

    def reset_game(self):
        self.used_letters = [0] * 26
        self.secret_word = self.get_secret_word()
        self.clue = self.get_word_definition(self.secret_word)
        self.player_secret = "".join(['_' if char != ' ' else ' ' for char in self.secret_word])
        self.number_of_mistakes = 0
        self.game_over = False
        self.won = False

    def get_secret_word(self):
        word_response = requests.get("https://random-word-api.vercel.app/api?words=1")
        return word_response.json()[0]

    def get_word_definition(self, base_word):
        url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{base_word}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            try:
                return data[0]['meanings'][0]['definitions'][0]['definition']
            except (KeyError, IndexError):
                return "Definition not found in response"
        else:
            return f"API error: {response.status_code}"

    def get_character(self):
        while True:
            given_char = input("Input a character: ").lower()

            if len(given_char) != 1:
                print("Please enter exactly one character!")
                continue

            if given_char not in self.alphabet:
                print("You need to input a letter from the alphabet!")
                continue

            if self.used_letters[ord(given_char) - 97] == 1:
                print("You already used that letter!")
                continue

            self.used_letters[ord(given_char) - 97] = 1
            return given_char

    def process_guess(self, char):
        if char in self.secret_word:
            new_player_secret = list(self.player_secret)
            for i, secret_char in enumerate(self.secret_word):
                if secret_char == char:
                    new_player_secret[i] = char
            self.player_secret = "".join(new_player_secret)

            if "_" not in self.player_secret:
                self.game_over = True
                self.won = True
        else:
            self.number_of_mistakes += 1
            if self.number_of_mistakes == 8:
                self.game_over = True
                self.won = False

    def display_game_state(self):
        print("\n" + "="*50)
        print(f"Word: {self.player_secret}")
        print(f"Clue: {self.clue}")

        used_chars = [chr(i + 97) for i, used in enumerate(self.used_letters) if used == 1]
        print(f"Used letters: {', '.join(used_chars)}")
        print(f"Mistakes: {self.number_of_mistakes}/8 - Lives left: {8 - self.number_of_mistakes}")

    def play_again(self):
        restart = input("\nPlay again? (y/n): ").lower()
        if restart == 'y':
            self.reset_game()
            self.play()
        elif restart != "n" and restart != "y":
            print("You need to input y or n")
            self.play_again()
        else:
            print("Thanks for playing!")


    def play(self):
        print("Welcome to Hangman!")
        print("Your task is to guess the secret word")

        while not self.game_over:
            self.display_game_state()
            char = self.get_character()
            self.process_guess(char)

        self.display_game_state()
        if self.won:
            print("\nYOU WON!!!")
        else:
            print("\nYOU LOST!!!")
        print(f"The secret word was: '{self.secret_word}'")
        self.play_again()



if __name__ == "__main__":
    game = HangmanGame()
    game.play()