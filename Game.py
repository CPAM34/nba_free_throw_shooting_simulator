import random

from main import log


class Game:
    def __init__(self, player_name, ft_pct, nba_stats_id):
        self.player_name = player_name
        self.ft_pct = ft_pct
        self.nba_stats_id = nba_stats_id
        self.ft_made = 0
        self.ft_attempts = 0
        self.done = False

    def im_done(self):
        self.done = True

    def shoot_ft(self):
        accuracy = random.radint(1,100)
        if accuracy < self.ft_pct:
            log("SWISH!", color="Green", figlet=True)
            self.ft_made += 1
            self.ft_attempts += 1
            log("Currently {}/{} from the line", color="Green")
        else:
            log("CLANK!", color="Red", figlet=True)
            self.ft_attempts += 1
            log("Currently {}/{} from the line", color="Red")
