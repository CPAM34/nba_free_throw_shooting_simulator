from Game import Game
from Log import log

import os
import re

import statistics

from datetime import datetime
from nba_api.stats.static import players
from nba_api.stats.endpoints import (playercareerstats, commonplayerinfo)

from PyInquirer import (Token, ValidationError, Validator, prompt,
                        style_from_dict)


style = style_from_dict({
    Token.QuestionMark: '#fac731 bold',
    Token.Answer: '#4688f1 bold',
    Token.Instruction: '',  # default
    Token.Separator: '#cc5454',
    Token.Selected: '#0abf5b',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Question: '',
})


class PlayerValidator(Validator):

    def validate(self, name):
        """
        Checks to see if the player input is of an actual player's name

        :param name: the player's inputted name
        """
        if len(name.text):
            try:
                # Find NBA player matching the input name, raise an error if not found
                nba_players = players.get_players()
                player_match = [player for player in nba_players if player['full_name'] == name.text][0]
                return True
            except:
                raise ValidationError(
                    message="That is not an NBA player",
                    cursor_position=len(name.text))
        else:
            # Raise an error if field left blank
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
            'message': 'There are {} players with that name. Please chose one:'.format(len(matches)),
            'choices': []
        }
    ]
    for match in matches:
        # Populate choices with specific player characteristics when a name is associated with multiple players
        player = commonplayerinfo.CommonPlayerInfo(player_id=match['id']).get_data_frames()[0]
        birthdate = datetime.strptime(player.BIRTHDATE.values[0], '%Y-%m-%dT%H:%M:%S').strftime("%B %-d, %Y")
        question[0]['choices'].append({
            'name': "{} {} - {} - Born {}".format(player.FIRST_NAME.values[0], player.LAST_NAME.values[0],
                                                  player.POSITION.values[0], birthdate),
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
            'type': 'list',
            'name': 'choice',
            'message': 'What would you like to do?',
            'choices': ['Take a shot', 'I\'m done, let\'s end this']
        }
    ]
    answer = prompt(question, style=style)
    return answer


def main():
    # Welcomes the user and prepares the retrieves the list of players to reference the user's input to
    log("NBA Free Throw Shooting Simulator", color="red", figlet=True)
    log("Welcome to the NBA Free Throw Simulator command line tool", color="green")
    log("Populating NBA Players...", color="blue")
    nba_players = players.get_players()
    log("Populated!", color="blue")
    # Check for match within between input and list of players after user makes prompted input
    player = ask_for_player()
    matches = [nba_player for nba_player in nba_players if nba_player['full_name'] == player['player_name']]
    player_id = matches[0]['id']
    if len(matches) > 1:
        # If there are multiple players matching a name, prompt user for follow-up choice
        player_id = clarify_player(matches)['exact_player']
    # Retrieve stats for selected player, get player's career FT%
    log("Retrieving stats for {}...".format(player['player_name']), color="blue")
    stats = playercareerstats.PlayerCareerStats(player_id=player_id).get_data_frames()[0]
    ft_pct = statistics.mean(stats.FT_PCT.values) * 100
    log("Stats retrieved!", color="blue")
    # Initialize game
    game = Game(player_name=player['player_name'], ft_pct=ft_pct, nba_stats_id=player_id)
    while not game.done:
        # Keep asking the user whethe rhe'd like to shoot/not till user elects not to shoot
        take_shot = ask_if_done()
        if take_shot['choice'] == "Take a shot":
            game.shoot_ft()
        else:
            game.im_done()
    log("Thank you so much for playing my game!", color="blue", figlet=True)


def get_stats(game):
    # TODO: Implement a charting solution where player can chart simulator results with real life results
    return game


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
