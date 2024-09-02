import config
import math
import team
import logging
import sys
import random
from datetime import datetime
from collections import Counter

if __name__ == '__main__':


    logging.basicConfig(filename="../logs/"+str(config.amateur)+"WP__"+str(datetime.now().strftime('%Y-%m-%d %H-%M'))+".txt",filemode='a',format="",level=logging.INFO)
    logging.info("CONFIGURATION")
    logging.info("Number of games per match: "+str(config.games))
    logging.info("Verbose mode: "+str(config.verbose))
    logging.info("Decimal places for win rates: "+str(config.digits))
    logging.info("WP per team: "+str(config.amateur))
    logging.info("Number of randomized teams: "+str(config.teamAmount))
    logging.info("Display Threshhold: "+str(config.displayThreshhold))
    logging.info("Kill Threshhold: "+str(config.killThreshhold))
    logging.info("Number of simulated phases: "+str(config.phases))
    logging.info("Simulate single Team: "+str(config.singleTeam))
    logging.info("Use Point System instead of KO: "+str(config.pointSystem))
    logging.info("")

    combs = []

    combinations = 0
    if config.excludeKeeper:
        maxKeeper=0
    else:
        maxKeeper=10
    if config.excludeAusputzer:
        maxAusputzer=0
    else:
        maxAusputzer=5
    for i in range(min(maxKeeper,math.floor((config.amateur-3)/2))+1):
        if config.verbose and False:
            print("i: "+str(i))
            logging.info("i: "+str(i))
        combsX = []
        combsY = 0
        for j in range(min(maxAusputzer,math.floor((config.amateur-3)/2)-i)+1):
            if config.verbose and False:
                print("j: "+str(j))
                logging.info("j: "+str(j))
            vms = config.amateur - 2*i-2*j
            minWP = math.ceil(max(0,(vms)/7))
            maxWP = math.floor(3 / 5 * vms)
            for k in range(minWP,maxWP+1,1):
                ms = vms - k
                minWP = max(math.ceil(k/4),math.ceil(ms/4))
                maxWP = min(k*3,math.floor(3 / 4 * ms))
                combinations+=maxWP-minWP+1
                combsY+=maxWP-minWP+1
                if config.verbose and False:
                    print("k: "+str(k))
                    print("MinWP: "+str(minWP))
                    print("MaxWP: "+str(maxWP))
                    print("MS Combinations: "+str(maxWP-minWP+1))
                    print("Cumulated Combinations: "+str(combinations))
            combsX.append(combsY)
            if config.verbose and False:
                print("VMS Combinations:" + str(combsY))
        combs.append(combsX)

    
    print(combs)

    print("For " + str(config.amateur) + " wp there are " + str(combinations) + " different combinations.")
    logging.info("For " + str(config.amateur) + " wp there are " + str(combinations) + " different combinations.")

    #esc = team.Team("ESC",10,10,35,35,13)
    esc1 = team.Team("ESC 1",0,0,10,8,24)
    esc2 = team.Team("ESC 2",0,0,14,21,7)
    esc3 = team.Team("ESC 3",0,0,18,6,18)
    esc4 = team.Team("ESC 4",0,0,24,10,8)
    esc5 = team.Team("ESC 5",0,0,18,18,6)
    # esc6 = team.Team("20-9-27",0,0,20,9,27)
    # esc7 = team.Team("27-20-9",0,0,27,20,9)
    # esc8 = team.Team("ESC",0,0,31,14,11)
    # esc9 = team.Team("14-11-31",0,0,14,11,31)
    handSelectedTeams = [esc1, esc2, esc3, esc4, esc5]
    handSelectedTeams = []

    if config.tournamentMode:
        stats = {team.name: {'points': [], 'places':[]} for team in handSelectedTeams}
        winning_teams = []

        for i in range(config.tournaments):
            print('\rSimulating tournament ' + str(i), end='', flush=True)
            teamList = handSelectedTeams.copy()
            for j in range(config.teamAmount-len(handSelectedTeams)):
                generatedTeam = team.Team.good(config.amateur, combs)
                teamList.append(generatedTeam)

            for current_team in teamList:
                current_team.allMatches(teamList)

            # Order teams by number of points
            teamList.sort(key=team.rate, reverse=True)

            winning_teams.append(teamList[0].name)

            # Display tournaments table
            if config.verbose:
                print('\nTournament '+str(i)+' Results:')
                print('Place  Team Name    Points')
                for place, selected_team in enumerate(teamList, start=1):
                    print(f'{place:<6}{selected_team.name:<12}{selected_team.wins}')

            # For all teams in handSelectedTeams append team.wins to their respective points list.
            for selected_team in handSelectedTeams:
                stats[selected_team.name]['points'].append(selected_team.wins)

            # For all teams in handSelectedTeams append their place in the ordered list to their respective places list.
                stats[selected_team.name]['places'].append(teamList.index(selected_team) + 1)

            # Reset the team.wins and team.games stats to 0
                selected_team.wins = 0
                selected_team.games = 0

        for team in handSelectedTeams:
            print(f'\n{team.name} Results:')
            first_places = stats[team.name]['places'].count(1)
            total_tournaments = len(stats[team.name]['places'])
            
            # Calculate percentage of first places
            percentage_first_places = (first_places / total_tournaments) * 100
            print('First places: {:.2f}%'.format(percentage_first_places))

                        # Calculate percentage of second places
            second_places = stats[team.name]['places'].count(2)
            percentage_second_places = (second_places / total_tournaments) * 100
            print('Second places: {:.2f}%'.format(percentage_second_places))

            # Calculate percentage of third places
            third_places = stats[team.name]['places'].count(3)
            percentage_third_places = (third_places / total_tournaments) * 100
            print('Third places: {:.2f}%'.format(percentage_third_places))
            
            # Calculate average points per tournament
            average_points = sum(stats[team.name]['points']) / total_tournaments
            print('Average points per tournament: {:.2f}'.format(average_points))

        team_mentions = Counter(winning_teams)
        top_teams = team_mentions.most_common(10)

        print('\nTop 10 Notable Teams:')
        print('Team Name\tMentions')
        for team_name, mentions in top_teams:
            print(f'{team_name}\t\t{mentions}')

        print(top_teams)
