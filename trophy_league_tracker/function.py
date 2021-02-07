from utility.brawl_stars_constants import TROPHY_CONDITIONS

def calculate_trophy_league_stat(result):
    ttl = 0 # total_trophy_lost
    tspr = 0 # total_star_point_reward
    btl = [] # brawler_trophy_lost
    brawlers = result["brawlers"]
    for brawler in brawlers:
        brawler_name = brawler["name"]
        brawler_trophy = brawler["trophies"]
        if brawler_trophy > 500:
            for trophy_condition in TROPHY_CONDITIONS:
                ctra = trophy_condition["trophy_range"] # condition_trophy_range
                cspr = trophy_condition["star_point_reward"] # condition_star_point_reward
                ctre = trophy_condition["trophy_reset"] # condition_trophy_reset
                if brawler_trophy >= ctra[0] and brawler_trophy <= ctra[1]:
                    trophy_lost = brawler_trophy - ctre
                    ttl += trophy_lost
                    tspr += cspr
                    btl_elem = [
                        brawler_name,
                        brawler_trophy, 
                        trophy_lost
                    ]
                    btl.append(btl_elem)

    btl.sort(key=lambda x: x[2], reverse = True)
    for i in range(len(btl)):
        btl[i].insert(0, i+1)

    return [ttl, tspr, btl]