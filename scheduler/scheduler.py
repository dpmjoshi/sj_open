# A Python program to find out all combinations of players to play matches
# Length is 2 for "Singles Tennis Match"
# We will then choose a random number between 1 to 15 and that 
import sys
import datetime
import calendar
import random
import time
import colorama
from colorama import Fore, Back, Style, Cursor
from itertools import combinations

from tournament_config import tournament_config
from file_handler import file_handler

sj_open = tournament_config("config/config_2021.yaml")
sj_open.generate_players_dict()

sj_open_files = file_handler()


# Now let's figure out groups for the tournament
# logic used here is 
# New players will be equally distributed to different groups randomly.
# Which means each group will have same number of new players
# Now we will just go through old_players and divide them randomly in two groups.
# finally prev year's finalists will go into different group using same randomness.

numNewPlayers = sj_open.get_num_new_players()
newPlayers = sj_open.new_players
#numOlfPlayers = sj_open.get_num_old_players()


scheduledMatches = 0
matches = []

group_a = []
group_b = []


def draw(playersList, group_a, group_b):
    numGroupA = 0
    numGroupB = 0    
    numPlayersPicked = 0
    numPlayers = len(playersList)
    playerMap = [0] * (numPlayers)    
    while (numPlayersPicked < numPlayers):
        # choose for group A
        index = random.randrange(0, numPlayers, 1)
        if playerMap[index] == 0 and numGroupA < numPlayers/2:
            playerMap[index] = 1
            group_a.append(playersList[index])   
            numPlayersPicked +=1
            numGroupA +=1

        index = random.randrange(0, numPlayers, 1)
        if playerMap[index] == 0 and numGroupB < numPlayers/2:
            playerMap[index] = 1
            group_b.append(playersList[index])
            numPlayersPicked +=1
            numGroupB +=1
print("")
print(Fore.GREEN + "Draw for {} \n".format(sj_open.name))
print(Style.RESET_ALL)
draw(sj_open.new_players, group_a, group_b)
draw(sj_open.old_players, group_a, group_b)
draw(sj_open.prev_finalist, group_a, group_b)

print("---------------------------------")
print("|  Group A      |      Group B  |")
print("---------------------------------")
for player_a, player_b in zip(group_a, group_b):
    time.sleep(1)
    print("      {}".format(player_a), end =" ")
    sys.stdout.flush()
    time.sleep(0.5)
    print("       |      ", end =" ")
    sys.stdout.flush()
    time.sleep(2)
    print("{}".format(player_b))
    sys.stdout.flush()
    time.sleep(1)

# write groups to the file
sj_open_files.write_groups(group_a, group_b)


# Start date for tournament (YYYY,MM,DD)
practiceStartDate = sj_open.practice_date.date()
startDate = sj_open.start_date.date()

weekDelta = datetime.timedelta(days=7)
oneDay = datetime.timedelta(days=1)

def match_scheduler(numPlayers, players, startDate):
    global hashMap
    global weekDelta 
    scheduledMatches = 0
    matchDate = startDate
    numMatches = 0
    matches = list(combinations(players, 2))

    # Print the obtained combinations 
    for match in list(matches):
        #print match    
        numMatches+= 1
    
    #print "Number of matches {}".format(numMatches)
    hashMap = [0] * (numMatches)
    consecutiveMatchesMap = [0] * (numPlayers)
    prevMatch = ["yy", "zz"]
    matchOrder = []

    while (scheduledMatches < numMatches):
        matchNum = random.randrange(0, numMatches, 1)
        #print "Checking matchNum : {}".format(matchNum)
        if (hashMap[matchNum] == 0):
            #if ((scheduledMatches < (numMatches / 2) - 1) and (prevMatch[0] in matches[matchNum]) or (prevMatch[1] in matches[matchNum])):
                #continue            
            matchDate = startDate + (scheduledMatches * weekDelta)
            matchWeekday = calendar.day_name[matchDate.weekday()]
            matchWeekday = matchWeekday.ljust(8, ' ')
            hashMap[matchNum] = 1
            #consecutiveMatchesMap[
            scheduledMatches+= 1
            prevMatch = matches[matchNum]
            #print "{} |  {}  |  {} Vs {}".format(matchDate, matchWeekday, matches[matchNum][0], matches[matchNum][1])
            matchOrder.append(matches[matchNum])
    return matchOrder        

practice_order = match_scheduler(len(group_a), group_a+group_b, practiceStartDate)
grp_a_order = match_scheduler(len(group_a), group_a, startDate)
grp_b_order = match_scheduler(len(group_b), group_b, startDate + oneDay)

# Practice Schedule
# Practice start date and number of practice matches per player comes from config file
# Groups doesn't apply to practice matches, your opponent will be randomly chosen.

scheduledPracticeMatches = 0
matchesPerDay = 0
practiceDate = practiceStartDate
prevMatch = ["zz", "yy"]
consecutiveHash = [0] * len(practice_order)
numPractMatchesPerPlayerMap = [0] * sj_open.num_players

print ("")
print(Fore.GREEN + "Practice Schedule for {}".format(sj_open.name))
print(Style.RESET_ALL)
print ("")

for match in practice_order:
    if ((prevMatch[0] in match) or (prevMatch[1] in match)):
       continue

    player1 = match[0]
    player2 = match[1]
    if ((numPractMatchesPerPlayerMap[sj_open.playersDict[player1]] >= sj_open.max_pract_match_per_player) or
        (numPractMatchesPerPlayerMap[sj_open.playersDict[player2]] >= sj_open.max_pract_match_per_player)):
        continue

    if ((scheduledPracticeMatches % 2) == 0):
        practiceDate = practiceStartDate + ((scheduledPracticeMatches / 2) * weekDelta)
    matchWeekday = calendar.day_name[practiceDate.weekday()]
    matchWeekday = matchWeekday.ljust(8, ' ')
    scheduledPracticeMatches+= 1
    if (practiceDate >= startDate):
        break

    pract_schedule = "{} |  {}  |  {} Vs {} ".format(practiceDate, matchWeekday, match[0], match[1])
    print (pract_schedule)
    sj_open_files.write_pract_schedule(pract_schedule)

    matchesPerDay+=1
    prevMatch = match

    # to keep track of number of practice matches each player plays
    numPractMatchesPerPlayerMap[sj_open.playersDict[prevMatch[0]]] += 1
    numPractMatchesPerPlayerMap[sj_open.playersDict[prevMatch[1]]] += 1

    if (matchesPerDay == 1):
        matchesPerDay = 0
        practiceDate += oneDay

sj_open_files.finalize_pract_schedule()

print ("")
print ("")
print (Fore.GREEN + "Tournament Schedule for {}".format(sj_open.name))
print (Style.RESET_ALL)

tournament_schedule_header = "   Group   |    Date    |     Day    |    Match    |   Referees"
print ("")
print (tournament_schedule_header)
print ("------------------------------------------------------------------")
sj_open_files.write_tournament_schedule(tournament_schedule_header)

lastMatchDate = startDate
for (match_a, match_b) in zip(grp_a_order, grp_b_order):
    matchDate = startDate + (scheduledMatches * weekDelta)
    matchWeekday = calendar.day_name[matchDate.weekday()]
    matchWeekday = matchWeekday.ljust(8, ' ')
    scheduledMatches+= 1

    # match_a schedule
    match_a_schedule = " Group A   | {} |  {}  |  {} Vs {}   |  Refs. {} and {} ".format(matchDate, matchWeekday, match_a[0], match_a[1], match_b[0], match_b[1])
    print (match_a_schedule)
    sj_open_files.write_tournament_schedule(match_a_schedule)

    matchDate += oneDay
    matchWeekday = calendar.day_name[matchDate.weekday()]
    matchWeekday = matchWeekday.ljust(8, ' ')    

    # match_b schedule
    match_b_schedule = " Group B   | {} |  {}  |  {} Vs {}   |  Refs. {} and {} ".format(matchDate, matchWeekday, match_b[0], match_b[1], match_a[0], match_a[1])

    # print match b schedule on console
    print (match_b_schedule)
    print ("")

    # Write match b schedule to csv file
    sj_open_files.write_tournament_schedule(match_b_schedule)

    lastMatchDate = matchDate
    time.sleep(0.75)

# Print semi's and final's date for visibility 

semiFinalStartDate = lastMatchDate + weekDelta
print(Fore.YELLOW + "1st Semi Final | A1 vs B2  | {}   ---> Winner ----".format(semiFinalStartDate))
print("\t\t\t\t\t\t\t |")
print(Fore.RED + "\t\t\t\t\t\t\t ------------ Final | {} ".format(semiFinalStartDate + weekDelta))
print("\t\t\t\t\t\t\t |")
print(Fore.YELLOW + "2nd Semi Final | B1 vs A2  | {}   ---> Winner ----".format(semiFinalStartDate + oneDay))
print("")


sj_open_files.write_tournament_schedule("1st Semi Final | {} |  A1 vs B2 ".format(semiFinalStartDate))
sj_open_files.write_tournament_schedule("2nd Semi Final | {} |  B1 vs A2 ".format(semiFinalStartDate + oneDay))
sj_open_files.write_tournament_schedule("Final Match | {}".format(semiFinalStartDate + weekDelta))


sj_open_files.finalize_tournament_schedule()
