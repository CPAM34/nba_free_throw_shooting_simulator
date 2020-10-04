from Log import log
import random


class Game:
    def __init__(self, player_name, ft_pct, nba_stats_id):
        """
        Constructor for Game class

        :param player_name: The player's name
        :param ft_pct: The player's free throw percentage
        :param nba_stats_id: The player's NBA Stats API ID
        """
        self.player_name = player_name
        self.ft_pct = ft_pct
        self.nba_stats_id = nba_stats_id
        self.ft_made = 0
        self.ft_attempts = 0
        self.done = False

    def im_done(self):
        """
        Finish the game
        """
        self.done = True

    def shoot_ft(self):
        """
        Shoot a free throw
        """
        # Generate a random number to compare the player's percentage to
        accuracy = random.randint(1, 100)
        if accuracy < self.ft_pct:
            # Free throw good
            log("SWISH!", color="green", figlet=True)
            self.ft_made += 1
            self.ft_attempts += 1
            log("Currently {}/{} from the line".format(self.ft_made, self.ft_attempts), color="green")
        else:
            # Free throw miss
            log("BRICK!", color="red", figlet=True)
            self.ft_attempts += 1
            log("Currently {}/{} from the line".format(self.ft_made, self.ft_attempts), color="red")
