# sj_open

repository to version control sj open scheduler script and other potential upcoming software components

scheduler:

a python script that consumes yaml based config file, extracts all configs and does following key tasks.
   1. Generates two groups based on new_players, old_players and previous finalists. Script puts them in two different groups
      randomly, each time user runs this scheduler these groups will be different.
   2. Generates a practice match scheduler based on practice match date and maximum practice matches per player.
   3. Finally it generates a tournament schedule based on groups generated in step1 and other configs from yaml file.

config_2021.yaml:

There should be a config file per tournament.
     
    - start_date: start date of tournament
    
    - practice_date: practice start date
    
    - max_pract_match_per_player: defines number of practice matches each player will play
    
    - prev_finalist: list of finalist from previous tournament

    - new_players: Players those are new to the tournament or haven't won a match in previous tournament.

    - old_players: list of players who have played tournament previously and have won at least one match.

Testing:
   tested on python3.7
   
   requires colorama to be installed "pip3 install colorama"

How to run:
   run from command line, so that you can see colourful output.
   
   $ python3 scheduler.py
