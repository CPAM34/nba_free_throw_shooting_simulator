# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import os
import re

import six

import PyInquirer
import clint
import requests

from PyInquirer import (Token, ValidationError, Validator, print_json, prompt,
                        style_from_dict)

from pyfiglet import figlet_format

from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats

from PyInquirer import (Token, ValidationError, Validator, print_json, prompt,
                        style_from_dict)


try:
    import colorama
    colorama.init()
except ImportError:
    colorama = None

try:
    from termcolor import colored
except ImportError:
    colored = None

style = style_from_dict({
    Token.QuestionMark: '#fac731 bold',
    Token.Answer: '#4688f1 bold',
    Token.Instruction: '',  # default
    Token.Separator: '#cc5454',
    Token.Selected: '#0abf5b',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Question: '',
})

nba_players = players.get_players()


def log(string, color, font="slant", figlet=False):
    """
    Outputs a string

    :param string: The string you are looking to output
    :param color: The color in which you'd like the string to be outputted
    :param font: The font in which you'd like the string to be outputted. Defaults to "slant"
    :param figlet: If set to true, creates ASCII art
    """
    if colored:
        if not figlet:
            six.print_(colored(string, color))
        else:
            six.print_(colored(figlet_format(
                string, font=font), color))
    else:
        six.print_(string)


class PlayerValidator(Validator):

    def validate(self, name):
        if len(name.text):
            player_match = [player for player in nba_players if player['full_name'] == name][0]
            if player_match == name.text:
                return True
            else:
                raise ValidationError(
                    message="Invalid email",
                    cursor_position=len(name.text))
        else:
            raise ValidationError(
                message="You can't leave this blank",
                cursor_position=len(email.text))

def askPlayer():
    questions = [
        {
            'type': 'input',
            'name': 'player_name',
            'message': 'Enter the player\'s name',
            'validate': PlayerValidator,
        },
    ]
    answers = prompt(questions, style=style)
    return answers


def main():
    """
    A Python CLI designed to simulate an NBA player's ability to shoot free throws
    """
    log("NBA Free Throw Shooting Simulator", color="red", figlet=True)
    log("Welcome to the NBA Free Throw Simulator command line tool", "green")


def get_stats(name):
    pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
