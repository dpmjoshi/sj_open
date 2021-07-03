# SJ_Open

Repository to version control sj open scheduler script and other potential upcoming software projects.

# Scheduler Project:

a python script that consumes yaml based config file, extracts all configs and does following key tasks.
   1. Generates two groups based on `new_players`, `old_players` and `prev_finalist`. Script puts them in two different groups
      randomly, each time user runs this scheduler these groups will be different.
   2. Generates a practice match scheduler based on `practice_date` and `max_pract_match_per_player`.
   3. Finally it generates a tournament schedule based on groups generated in step1 and other configs from yaml file.

## config_2021.yaml:

There should be a config file per tournament.

Here are few configs with the description
     
   `start_date:` start date of tournament
    
   `practice_date:` practice start date
    
   `max_pract_match_per_player:` defines number of practice matches each player will play
    
   `prev_finalist:` list of finalist from previous tournament

   `new_players:` Players those are new to the tournament or haven't won a match in previous tournament.

   `old_players:` list of players who have played tournament previously and have won at least one match.
   
 Checkout this config file for reference [config_2021.yaml](https://github.com/dpmjoshi/sj_open/blob/mainline/scheduler/config/config_2021.yaml)

## Testing:

tested on **Python 3.9.4**
   
   requires colorama to be installed 
  
     $ pip3 install colorama

## How to run:

run from command line, so that you can see colourful output.
   
     $ python3 scheduler.py
