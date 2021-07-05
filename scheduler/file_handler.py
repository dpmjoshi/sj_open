import os
import datetime

class file_handler:
    def __init__(self):
        # Open .csv files for draw, practice schedule and tournament schedule 
        now = datetime.datetime.now() 
        curDateTime = "{}_{}_{}__{}{}".format(now.month, now.day, now.year, now.hour, now.minute)
        self.outputDirPath = "{}/output/{}".format(os.getcwd(), curDateTime)
        os.mkdir(self.outputDirPath)
        
        self.groupsFilePath = "output/{}/groups.csv".format(curDateTime)
        self.practScheduleFile = open("output/{}/practice_schedule.csv".format(curDateTime), "wt")
        self.tournamentScheduleFile = open("output/{}/tournament_schedule.csv".format(curDateTime), "wt")
        
    def write_groups(self, group_a, group_b):
        self.groupsFile = open(self.groupsFilePath, "wt")
        self.groupsFile.writelines("Group A, Group B\n")
        for player_a, player_b in zip(group_a, group_b):
            self.groupsFile.writelines("{}, {}\n".format(player_a, player_b))
        self.groupsFile.close()
        
    def write_tournament_schedule(self, schedule):
        self.tournamentScheduleFile.write(schedule.replace("|", ","))
        self.tournamentScheduleFile.write("\n")
        
    def finalize_tournament_schedule(self):
        self.tournamentScheduleFile.close()
        
    def write_pract_schedule(self, schedule):
        self.practScheduleFile.write(schedule.replace("|", ","))
        self.practScheduleFile.write("\n")
        
    def finalize_pract_schedule(self):
        self.practScheduleFile.close()    