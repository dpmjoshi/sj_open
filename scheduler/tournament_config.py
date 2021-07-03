import yaml
from datetime import datetime

class tournament_config:
    def __init__(self, config_file):
        with open(config_file, "r") as yamlfile:
            cfg = yaml.load(yamlfile, Loader=yaml.FullLoader)
            self.num_players = cfg["general"]["num_players"]
            self.prev_finalist = list(cfg["general"]["prev_finalist"])
            self.new_players = list(cfg["general"]["new_players"])
            self.old_players = list(cfg["general"]["old_players"])
            self.name = str(cfg["general"]["name"])
            self.start_date = datetime.strptime(cfg["general"]["start_date"], '%m/%d/%Y')
            self.practice_date = datetime.strptime(cfg["general"]["practice_date"], '%m/%d/%Y')
            self.max_pract_match_per_player = cfg["general"]["max_pract_match_per_player"]

    def get_num_new_players(self):
        return len(self.new_players)

    def generate_players_dict(self):
        self.playersDict = dict()
        playerNum = 0
        for player in self.new_players:
            self.playersDict[player] = playerNum
            playerNum += 1
        for player in self.old_players:
            self.playersDict[player] = playerNum
            playerNum += 1
        for player in self.prev_finalist:
            self.playersDict[player] = playerNum
            playerNum += 1