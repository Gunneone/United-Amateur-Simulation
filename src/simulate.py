import config
import math
import team
import logging
from datetime import datetime

if __name__ == '__main__':

	logging.basicConfig(filename="../logs/"+str(datetime.now())+".txt",filemode='a',format="",level=logging.INFO)
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
	logging.info("")

	combs = []

	combinations = 0
	for i in range(min(10,math.floor((config.amateur-3)/2))+1):
		if config.verbose:
			print("i: "+str(i))
			logging.info("i: "+str(i))
		combsX = []
		combsY = 0
		for j in range(min(10,math.floor((config.amateur-3)/2)-i)+1):
			if config.verbose:
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
				if config.verbose:
					print("k: "+str(k))
					print("MinWP: "+str(minWP))
					print("MaxWP: "+str(maxWP))
					print("MS Combinations: "+str(maxWP-minWP+1))
					print("Cumulated Combinations: "+str(combinations))
			combsX.append(combsY)
			if config.verbose:
				print("VMS Combinations:" + str(combsY))
		combs.append(combsX)

	if config.verbose:
		print(combs)

	print("For " + str(config.amateur) + " wp there are " + str(combinations) + " different combinations.")
	logging.info("For " + str(config.amateur) + " wp there are " + str(combinations) + " different combinations.")

	omph1 = team.Team("OMPH1",0,7,17,17,50)
	omph2 = team.Team("OMPH2",0,9,16,16,48)
	teamList = [omph1,omph2]
	
	print("\nTEAMS:")
	logging.info("\nTEAMS:")
	for i in range(0,config.teamAmount):
		teamList.append(team.Team.random(config.amateur,combs))

	if config.singleTeam == True:
		esc.allMatches(teamList)
		print("\nWins: "+str(esc.wins))
		print("Games: "+str(esc.games))
		print("\nTeam "+str(esc.name)+" had a win rate of "+str(round(100*esc.wins/(esc.games),2))+"%.")
		print("Teams, that have defeated ESC:")
		for t in teamList:
			if t.wins > 0:
				print("Team "+str(t.name)+": "+str(t.wins)+" of "+str(t.games)+" games")

	if config.singleTeam == False:
		for i in range(1,config.phases+1):			
			print("PHASE "+str(i))
			logging.info("\nPHASE "+str(i))
			print("Simulating games...")
			logging.info("Simulating games...")
			for t in teamList:
				t.allMatches(teamList)

			print("\n"+str(config.games*(len(teamList))*(len(teamList)-1))+" games were simulated. (Phase "+str(i)+")")
			logging.info(""+str(config.games*(len(teamList))*(len(teamList)-1))+" games were simulated. (Phase "+str(i)+")")
			teamList.sort(key=team.rate)

			if i < config.phases:
				survivors = []
				for t in teamList:
					if t.wins/t.games <= config.killThreshhold:
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




	for t in teamList:
		if t.wins/t.games >= config.displayThreshhold:
			print("\nTeam "+str(t.name)+" had a win rate of "+str(round(100*t.wins/(t.games),2))+"% win rate after "+str(t.games)+" games.")
			logging.info("Team "+str(t.name)+" had a win rate of "+str(round(100*t.wins/(t.games),2))+"% win rate after "+str(t.games)+" games.")

		#tex = "\\documentclass{article}\n\\usepackage[a4paper,left=0cm,right=0cm,top=1cm,bottom=4cm,bindingoffset=0mm]{geometry}\n\\begin{document}\n\\bgroup\\def\\arraystretch{2}\\setlength\\tabcolsep{0.75mm}\n\\begin{tabular}{|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|}\n\\hline\n"

		#for team in teamList:
		#		tex += " & " + str(team.name)

		#tex += "\\\\\n\\hline\n"

		#for y in teamList:
		#		 tex += str(y.name)

		#		 for idx, x in enumerate(teamList):
		#				 tex += " & " + y.results[idx]

		#		 tex += "\\\\\n\\hline\n"

		# tex += "\\end{tabular}\n\\end{document}"

		# print(tex)

		#print("\n"+str(games*(len(survivors))*(len(survivors)-1))+" games were simulated. (Phase 2)")

		#print("ESC Games: "+str(esc.games))
		#print("ESC Wins: "+str(esc.wins))
		#print("ESC Looses: "+str(esc.defeats))
		#esc.allMatches(teamList)
		#print("Team "+str(esc.name)+" "+str(round(100*esc.wins/(esc.wins+esc.defeats),2))+"% win rate")
		#print(str(esc.wins))