import sys
sys.path.append('NBA-Stats/')
from PlayerStats.stats import write_stats_for_season as write_season

START_YEAR = 1997
STOP_YEAR = 2017
DATA_DIR = 'data/'

def main():
    for year in range(START_YEAR, STOP_YEAR):
        write_season(year, data_dir=DATA_DIR)


main()
