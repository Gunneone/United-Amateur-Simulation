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
	esc1 = team.Team("ESC 1",0,10,20,12,36)
	esc2 = team.Team("ESC 2",0,0,24,16,48)
	esc3 = team.Team("ESC 3",0,10,25,32,11)
	#esc4 = team.Team("ESC 4",0,0,37,15,45)
	# esc5 = team.Team("16-10-30",0,0,16,10,30)
	# esc6 = team.Team("20-9-27",0,0,20,9,27)
	# esc7 = team.Team("27-20-9",0,0,27,20,9)
	# esc8 = team.Team("ESC",0,0,31,14,11)
	# esc9 = team.Team("14-11-31",0,0,14,11,31)
	handSelectedTeams = [esc1,esc2,esc3]

	if config.tournamentMode:
		for i in range(config.tournaments):
			teamList = handSelectedTeams
			for j in range(config.teamAmount-len(handSelectedTeams)):
				generatedTeam = team.Team.squares(config.amateur, combs)
				teamList.append(generatedTeam)
			
	else:
		teamList = handSelectedTeams
		logging.info("Generating teams...")
		print("Generating teams...")
		
		print("\nTEAMS:")
		logging.info("\nTEAMS:")
		for i in range(0,config.teamAmount):
			#generatedTeam = team.Team.good(config.amateur,combs)
			generatedTeam = team.Team.square(config.amateur,combs)
			teamList.append(generatedTeam)
			#generatedTeam.log()

		logging.info(str(len(teamList))+" teams in the race.")
		print(str(len(teamList))+" teams in the race.")

		if config.singleTeam == True:
			print("Simulating games...")
			logging.info("Simulating games...")
			esc.allMatches(teamList)
			if config.pointSystem:
				print("\nTeam "+str(esc.name)+" scored "+str(esc.wins)+" after "+str(esc.games)+"games.")
				print("That is an average of "+str(round(esc.wins/(esc.games),2))+"points per game.")
				logging.info("\nTeam "+str(esc.name)+" scored "+str(esc.wins)+" after "+str(esc.games)+"games.")
				logging.info("That is an average of "+str(round(esc.wins/(esc.games),2))+"points per game.")
			else:
				print("\nWins: "+str(esc.wins))
				print("Games: "+str(esc.games))
				print("\nTeam "+str(esc.name)+" had a win rate of "+str(round(100*esc.wins/(esc.games),2))+"%.")
				logging.info("\nWins: "+str(esc.wins))
				logging.info("Games: "+str(esc.games))
				logging.info("\nTeam "+str(esc.name)+" had a win rate of "+str(round(100*esc.wins/(esc.games),2))+"%.")
			print("Top-Scorers against "+esc.name+":")
			teamList.sort(key=team.rate)
			for t in teamList:
				if config.pointSystem:          
					if t.wins > config.games*config.displayThreshhold*3:
						print("Team "+str(t.name)+": "+str(t.wins)+" points after "+str(t.games)+" games")
						logging.info("Team "+str(t.name)+": "+str(t.wins)+" points after "+str(t.games)+" games")
					if t.wins > config.singleTeamGames*0.7*3:
						t.flagged = True
				else:
					if t.wins > config.games*config.displayThreshhold:
						print("Team "+str(t.name)+": "+str(t.wins)+" of "+str(t.games)+" games")
						logging.info("Team "+str(t.name)+": "+str(t.wins)+" of "+str(t.games)+" games")
					if t.wins > config.singleTeamGames*0.7:
						t.flagged = True
					t.wins=0
					t.games=0
			
			config.singleTeam = False
			
			dominatingTeams=[]
			print('\nDominating Teams:')
			for t in teamList:
				if t.flagged:
					t.log()
					print(str(t.wins)+' Points')
					dominatingTeams.append(t)

			for t in dominatingTeams:
				t.allMatches(dominatingTeams)
			print('\n')

			dominatingTeams.sort(key=team.rate)
			
			for t in dominatingTeams:
				print("\nTeam "+str(t.name)+" had a win rate of "+str(round(100*t.wins/(t.games),2))+"% win rate after "+str(t.games)+" games.")
				logging.info("Team "+str(t.name)+" had a win rate of "+str(round(100*t.wins/(t.games),2))+"% win rate after "+str(t.games)+" games.")

			config.singleTeam = True
		
		

		if config.singleTeam == False:
			if config.vampireMode:
				teamNames = Counter([t.name for t in teamList])
				print('------------ teamNames ------------')
				logging.info('------------ teamNames ------------')
				print('Unique teams: ' + str(len(teamNames)))
				logging.info('Unique teams: ' + str(len(teamNames)))
				if config.verbose:
					print(teamNames)
					logging.info(teamNames)

				topTeams = teamNames.most_common(20)
				print('------------ Top Teams ------------')
				logging.info('------------ Top Teams ------------')
				for t in topTeams:
					print(t[0]+': '+str(t[1]))
					logging.info(t[0]+': '+str(t[1]))

				allTimeTopTeams = teamNames
				print('')
				print('------------ All Time Top Teams ------------')
				for t in allTimeTopTeams.most_common(20):
					print(t[0]+': '+str(t[1]))

				iteration=0
				while len(teamNames) != 1 and iteration < config.phases:
					print('')
					print('--------------------------------------')
					print('Iteration: '+str(iteration))
					print('--------------------------------------')
					print('')
					logging.info('--------------------------------------')
					logging.info('Iteration: '+str(iteration))
					logging.info('--------------------------------------')
					logging.info('')
					iteration+=1
					random.shuffle(teamList)
					if config.verbose:
						print('Teams after shuffle:')
						print([t.name for t in teamList])
					for t in range(math.floor(len(teamList)/2)):
						teamList[t].playAgainst(teamList[-1-t])
						if teamList[t].name != teamList[-1-t].name:
							if config.verbose:
								print('Due to a tie, both teams are replaced by a good team.')
								logging.info('Due to a tie, both teams are replaced by a good team.')
							teamList[t]=team.Team.good(config.amateur, combs)
							teamList[-1-t]=team.Team.good(config.amateur, combs)
						if config.verbose:
							print('--------------------------------------')
					teamNames = Counter([t.name for t in teamList])
					# Sort teamNames by number of occurences descending
					topTeams = teamNames.most_common(10)
					print('------------ Top Teams ------------')
					logging.info('------------ Top Teams ------------')
					for t in topTeams:
						print(t[0]+': '+str(t[1]))
						logging.info(t[0]+': '+str(t[1]))
						if t[0] in allTimeTopTeams:
							if t[1] > allTimeTopTeams[t[0]]:
								allTimeTopTeams[t[0]] = t[1]
						else:
							allTimeTopTeams[t[0]] = t[1]
					print('------------ All Time Top Teams ------------')
					logging.info('------------ All Time Top Teams ------------')
					for t in allTimeTopTeams.most_common(5):
						print(str(t[0])+': '+str(t[1]))
						logging.info(str(t[0])+': '+str(t[1]))
					print('Remaining teams: ' + str(len(teamNames)))
					logging.info('Remaining teams: ' + str(len(teamNames)))
				print('------------ All Time Top Teams ------------')
				logging.info('------------ All Time Top Teams ------------')
				for t in allTimeTopTeams.most_common(20):
					print(str(t[0])+': '+str(t[1]))
					logging.info(str(t[0])+': '+str(t[1]))
			else:
				for i in range(1,config.phases+1):
					print("PHASE "+str(i))
					logging.info("\nPHASE "+str(i))
					print("Simulating games...")
					logging.info("Simulating games...")
					for t in range(len(teamList)):
						teamList[t].allMatches(teamList)
						sys.stdout.write('\r'+str(t+1) + ' of '+ str(len(teamList)) +' teams simulated.')
						sys.stdout.flush()

					print("\n"+str(config.games*(len(teamList))*(len(teamList)-1))+" games were simulated. (Phase "+str(i)+")\n")
					logging.info(""+str(config.games*(len(teamList))*(len(teamList)-1))+" games were simulated. (Phase "+str(i)+")\n")
					teamList.sort(key=team.rate)

					if i < config.phases:
						survivors = []

						if config.pointSystem:
							for t in teamList:
								if t.wins/t.games < config.killThreshhold*3:
									print("\nTeam "+t.name+" scored "+str(round(t.wins/(t.games),2))+" points per game after "+str(t.games)+" games and was killed.")
									logging.info("\nTeam "+t.name+" scored "+str(round(t.wins/(t.games),2))+" points per game after "+str(t.games)+" games and was killed.")
								else:
									print("\nTeam "+t.name+" scored "+str(round(t.wins/(t.games),2))+" points per game after "+str(t.games)+" games.")
									logging.info("\nTeam "+t.name+" scored "+str(round(t.wins/(t.games),2))+" points per game after "+str(t.games)+" games.")
									t.wins=0
									t.games=0
									survivors.append(t)
						else:
							for t in teamList:
								if t.wins/t.games < config.killThreshhold:
									print("\nTeam "+t.name+" had a win rate of "+str(round(100*t.wins/(t.games),2))+"% and was killed.")
									logging.info("Team "+t.name+" had a win rate of "+str(round(100*t.wins/(t.games),2))+"% and was killed.")
								else:
									print("\nTeam "+str(t.name)+" had a win rate of "+str(round(100*t.wins/(t.games),2))+"%.")
									logging.info("Team "+str(t.name)+" had a win rate of "+str(round(100*t.wins/(t.games),2))+"%.")
									t.wins=0
									t.games=0
									survivors.append(t)


						print(str(len(survivors))+" of "+str(len(teamList))+" teams have survived.")
						logging.info(str(len(survivors))+" of "+str(len(teamList))+" teams have survived.")

						teamList = survivors
						if len(teamList)<2:
							print("\nWe have a winner!\n")
							logging.info("\nWe have a winner!\n")
							break

		if len(teamList)>1 and config.singleTeam == False and config.vampireMode == False:
			for t in teamList:
				if t.wins/t.games >= config.displayThreshhold:
					if config.pointSystem:
						print("\nTeam "+str(t.name)+" scored "+str(round(t.wins/(t.games),2))+" points per game after "+str(t.games)+" games.")
						logging.info("\nTeam "+str(t.name)+" scored "+str(round(t.wins/(t.games),2))+" points per game after "+str(t.games)+" games.")          
					else:
						print("\nTeam "+str(t.name)+" had a win rate of "+str(round(100*t.wins/(t.games),2))+"% win rate after "+str(t.games)+" games.")
						logging.info("Team "+str(t.name)+" had a win rate of "+str(round(100*t.wins/(t.games),2))+"% win rate after "+str(t.games)+" games.")
