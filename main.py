# This is a sample Python script.
import Game

import os
import re

import PyInquirer
import clint
import requests
import statistics
import six

from PyInquirer import (Token, ValidationError, Validator, print_json, prompt,
                        style_from_dict)

from pyfiglet import figlet_format

from nba_api.stats.static import players
from nba_api.stats.endpoints import (playercareerstats, commonplayerinfo)

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
        """
        Checks to see if the player input is of an actual player's name

        :param name: the player's inputted name
        """
        if len(name.text):
            player_match = [player for player in nba_players if player['full_name'] == name][0]
            if player_match == name.text:
                return True
            else:
                raise ValidationError(
                    message="That is not an NBA player",
                    cursor_position=len(name.text))
        else:
            raise ValidationError(
                message="You can't leave this blank",
                cursor_position=len(name.text))


def ask_for_player():
    """
    Asks user to input an NBA player's name

    :return: The player's name
    """
    question = [
        {
            'type': 'input',
            'name': 'player_name',
            'message': 'Enter the player\'s name',
            'validate': PlayerValidator,
        }
    ]
    answer = prompt(question, style=style)
    return answer


def clarify_player(matches):
    """
    Asks user to clarify a specific player in case of multiple players with the same name

    :param matches: A list of possible players that are a match for the name provided earlier
    :return: Returns the ID of the selected player
    """
    question = [
        {
            'type': 'list',
            'name': 'exact_player',
            'message': 'There are ' + len(matches) + ' players with that name. Please chose one:',
            'choices': []
        }
    ]
    for match in matches:
        player = commonplayerinfo(player_id=match['id'])
        question[0].choices.add({
            'name': "{} {} {} - Born {}".format(player['position'], player['first_name'],
                                                            player['last_name'], player['birthdate']),
            'value': match['id']
        })

    answer = prompt(question, style=style)
    return answer


def ask_if_done():
    """
    Asks user to choose whether to shoot or end the game

    :return: The user's choice
    """
    question = [
        {
            'type': 'input',
            'name': 'player_name',
            'message': 'What would you like to do?',
            'choices': ['Take a shot', 'I\'m done, let\'s end this']
        }
    ]
    answer = prompt(question, style=style)
    return answer


def main():
    """
    A Python CLI designed to simulate an NBA player's ability to shoot free throws
    """
    log("NBA Free Throw Shooting Simulator", color="red", figlet=True)
    log("Welcome to the NBA Free Throw Simulator command line tool", color="green")
    player = ask_for_player()
    matches = [player for player in nba_players if player['full_name'] == player.text]
    player_id = matches[0]['id']
    if len(matches) > 1:
        player_id = clarify_player(matches)
    stats = playercareerstats.PlayerCareerStats(player_id=player_id).get_data_frames()[0]
    game = Game(player_name=player['name'], ft_pct=statistics.mean(stats['ft_pct']), nba_stats_id=player_id)
    while not game.done:
        take_shot = ask_if_done()
        if take_shot:
            good = game.shoot_ft()
        else:
            game.im_done()
    log("Thank you so much for playing my game!", color="Blue", figlet=True)


def get_stats(name):
    pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
