import requests
import datetime
import json
import csv
import sys
#########################
###      CONFIG      ###
#######################
### First available season would be 1999-00
MAX_RETRIES = 0
BASE_PARAMS = {
    #Check the README for all exceptable
    'DateFrom': "", #type: str; format month/day/year
    "DateTo": "", #str format month/day/year
    "GameScope": "", #Yesterday or Last 10
    "GameSegment": "",
    "LastNGames": 82,
    "LeagueID": "00", #00 for nba 20 for d-league
    "Location": "", #home or road
    "MeasureType": "Base", #(Base)|(Advanced)|(Misc)|(Four Factors)|(Scoring)|(Opponent)|(Usage)|(Defense)
    "Month": 0,
    "OpponentTeamID": "0",
    "Outcome": "",
    "PaceAdjust": "N", #Y or N
    "PerMode": "Totals",
    "Period": "0",
    "PlayerExperience": "",
    "PlayerPosition": "", #((F)|(C)|(G)|(C-F)|(F-C)|(F-G)|(G-F))
    "PlusMinus": "N", #Y or N
    "Rank": "Y", #Y or No
    #"Season": "%s", #format 2015-16
    "SeasonSegment": "",
    "SeasonType": "Regular Season", #(Regular Season)|(Pre Season)|(Playoffs)|(All Star)
    "StarterBench": "", #Starters or Bench
    "VsConference": "", #East or West
    "VsDivision": "" #((Atlantic)|(Central)|(Northwest)|(Pacific)|(Southeast)|(Southwest)|(East)|(West))
}

BASE_URL = "http://stats.nba.com/stats/leaguedashplayerstats"

def get_query_year(year):
    now = datetime.datetime.now()
    first_year = now.year - 1
    second_year = (now.year) % 1000

    #Stats are not available before 1946
    if year >= 1997 and year <= now.year - 1:
        first_year = str(year)
        second_year = (year + 1) % 1000

    if second_year < 10:
        #syntax should be 00 not 0
        second_year = '0' + str(second_year)
    return str(first_year) + "-" + str(second_year)

def get_data_for_season(year, retries=0):
    q_year = get_query_year(year)
    query = BASE_PARAMS
    query['Season'] = q_year
    data = requests.get(BASE_URL, params=query)
    try:
        data = data.json()['resultSets'][0]
    except ValueError:
        if retries >  MAX_RETRIES:
            print 'Query url: %s' % data.url
            print 'Failed to pull data from nba.com for %s' % year
            print "Try again later."
            sys.exit()
        retries += 1
        get_data_for_season(year, retries=retries)

    return data

def write_stats_for_season(year, filename=None, append=False):
    q_year = get_query_year(year)
    fname = filename if filename else '%s-Player-Stats.csv' % q_year

    data = get_data_for_season(year)
    headers = data['headers']
    player_data = data['rowSet']

    file_perm = 'ab' if append else 'wb'

    with open(fname, file_perm) as file_ouput:
        csv_writer = csv.writer(file_ouput)
        csv_writer.writerow(headers)
        csv_writer.writerows(player_data)
