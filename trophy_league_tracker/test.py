from function.calculate_trophy_league_stat import calculate_trophy_league_stat
from utility.constants import TROPHY_CONDITIONS
import json

ctlsi = None # calculate_trophy_league_stat_input
with open('./input/calculate_trophy_league_stat.json') as f:
    ctlsi = json.load(f)

def test_calculate_trophy_league_stat(input, trophy_conditions, real_ttl, real_tspr, real_btl):
    tls = calculate_trophy_league_stat(input, trophy_conditions) # trophy_league_stat
    ttl = tls[0] # total_trophy_lost
    tspr = tls[1] # total_star_point_reward
    btl = tls[2] # brawler_trophy_lost

    is_true_ttl = ttl == real_ttl
    is_true_tspr = tspr == real_tspr
    is_true_btl = btl == real_btl

    if is_true_ttl and is_true_tspr and is_true_btl:
        return True
    return False

real_ttl = 185
real_tspr = 2760
real_btl = [
    [1,"NANI",561,12],[2,"SHELLY",635,11],[3,"BO",560,11],[4,"BEA",610,11],
    [5,"BARLEY",534,10],[6,"COLT",558,9],[7,"TARA",683,9],[8,"DARRYL",633,9],
    [9,"TICK",558,9],[10,"POCO",557,8],[11,"PAM",582,8],[12,"FRANK",532,8],
    [13,"GENE",607,8],[14,"NITA",580,6],[15,"MR. P",530,6],[16,"JESSIE",554,5],
    [17,"DYNAMIKE",629,5],[18,"EL PRIMO",554,5],[19,"GALE",604,5],[20,"SPROUT",554,5],
    [21,"RICO",578,4],[22,"ROSA",628,4],[23,"PENNY",627,3],[24,"CARL",551,2],
    [25,"JACKY",601,2],[26,"SURGE",576,2],[27,"COLETTE",551,2],[28,"BULL",650,1],
    [29,"BROCK",600,1],[30,"PIPER",750,1],[31,"BIBI",575,1],[32,"EMZ",650,1],
    [33,"EDGAR",550,1]
]

is_test_past = test_calculate_trophy_league_stat(
    ctlsi, TROPHY_CONDITIONS, real_ttl, real_tspr, real_btl
)
    
if is_test_past:
    print("test_calculate_trophy_league_stat pass !!")
else:
    print("test_calculate_trophy_league_stat not pass !!")