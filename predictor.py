import requests
from getpass import getpass
from NBA import Player

############
## CONFIG ##
############
VERBOSE ="""This tool gathers data from https://www.mysportsfeeds.com and predicts the NBA
MVP. Currently, there is only support for seasons after 2015. When MySportsFeeds
adds more data, I will come back and tweak the prediciton algorithm to
be more accurate. If you want to try the tool out, you just need to make a mysportsfeeds
account.
"""

BASE_URL = "https://www.mysportsfeeds.com/api/feed/pull/nba/2015-2016-regular/"
TEAM_URL = "overall_team_standings.json?teamstats=W"
PLAYER_URL = "cumulative_player_stats.json?playerstats=PTS/G,REB/G,AST/G"
DEFAULTS = {
    'USERNAME': None,
    'PASSWORD': None
}
YEAR = "2016"

def get_credentials():
    if DEFAULTS['USERNAME']:
        print 'Username: %s' % DEFAULTS['USERNAME']
        username = DEFAULTS['USERNAME']
    else:
        username = raw_input("Username: ")

    if DEFAULTS['PASSWORD']:
        print "WARNING: Storing passwords in plain text is NOT recommend!"
        password = DEFAULTS['PASSWORD']
    else:
        password = getpass('Password: ')

    return (username, password)

def get_team_info(credentials):
    teams = {}
    query = BASE_URL + TEAM_URL
    data = requests.get(url=query, auth=credentials)
    team_data = data.json()['overallteamstandings']['teamstandingsentry']

    for i in team_data:
        name = i['team']['City'] + ' ' + i['team']['Name']
        wins = i['stats']['Wins']['#text']
        teams[name] = wins

    return teams

def get_player_info(credentials, teams):
    players = []
    query = BASE_URL + PLAYER_URL
    data = requests.get(url=query, auth=credentials)
    player_data = data.json()['cumulativeplayerstats']['playerstatsentry']

    for i in player_data:
        name = i['player']['FirstName'] + ' ' + i['player']['LastName']
        team = i['team']['City'] + ' ' + i['team']['Name']
        wins = teams[team]

        try:
            PPG = i['stats']['PtsPerGame']['#text']
            RPG = i['stats']['RebPerGame']['#text']
            APG = i['stats']['AstPerGame']['#text']
        except KeyError:
            PPG = 0
            RBP = 0
            APG = 0
        p = Player(name, team, wins, PPG, RPG, APG)
        players.append(p)
    return players

def find_mvp(players):
    max_score = players[0].score
    mvp = players[0]

    for p in players:
        if p.score > max_score:
            max_score = p.score
            mvp = p
    return mvp

def print_winner(player):
    print "The %s MVP is %s of the %s." % (YEAR, player.name, player.team)

def main():
    print VERBOSE
    credentials = get_credentials()
    teams = get_team_info(credentials)
    players = get_player_info(credentials, teams)
    mvp = find_mvp(players)
    print_winner(mvp)

if __name__ == '__main__':
    main()
