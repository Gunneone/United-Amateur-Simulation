import config
import math
import team

if __name__ == '__main__':
    
    combs = []

    combinations = 0
    for i in range(11):
        combsX = []
        combsY = 0
        for j in range(11):
            vms = config.amateur - 2*i-2*j
            minWP = math.ceil(max(0,(vms)/7))
            maxWP = math.floor(3 / 5 * vms)
            for k in range(minWP,maxWP+1,1):
                ms = vms - 2*i-2*j
                minWP = max(math.ceil(k/4),math.ceil(ms/4))
                maxWP = min(k*3,math.floor(3 / 4 * ms))
                combinations+=maxWP-minWP
                combsY+=maxWP-minWP
            combsX.append(combsY)
        combs.append(combsX)

    #print(combs)


    print("For " + str(config.amateur) + " wp there are " + str(combinations) + " different combinations.")
   
    esc = team.Team("ESC",8,2,15,13,36)
    teamList = []

    for i in range(0,config.teamAmount):
        teamList.append(team.Team.random(config.amateur,combs))

    if config.singleTeam == True:
    	esc.allMatches(teamList)
    	print("\nWins: "+str(esc.wins))
    	print("Games: "+str(esc.games))
    	print("\nTeam "+str(esc.name)+" had a win rate of "+str(round(100*esc.wins/(esc.games),2))+"%.")
    	print("Teams, that have defeated ESC:")
    	for team in teamList:
    		if team.wins > 0:
    			print("Team "+str(team.name)+": "+str(team.wins)+" of "+str(team.games)+" games")
                    
    if config.singleTeam == False:
	    for i in range(1,config.phases+1):

	        for team in teamList:
	            team.allMatches(teamList)

	        print("\n"+str(config.games*(len(teamList))*(len(teamList)-1))+" games were simulated. (Phase "+str(i)+")")

	        teamList.sort(key=team.Team.win_rate)

	        if i < config.phases:
	            survivors = []
	            for team in teamList:
	                if team.wins/team.games <= config.killThreshhold:
	                    print("\nTeam "+team.name+" had a win rate of "+str(round(100*team.wins/(team.games),2))+"% and was killed.")
	                    #teamList.remove(team)
	                else:
	                    print("\nTeam "+str(team.name)+" had a win rate of "+str(round(100*team.wins/(team.games),2))+"%.")
	                    team.wins=0
	                    team.games=0
	                    survivors.append(team)

	            print(str(len(survivors))+" of "+str(len(teamList))+" teams have survived.")

	            teamList = survivors




	    for team in teamList:
	        if team.wins/team.games >= config.displayThreshhold:
	            print("\nTeam "+str(team.name)+" had a win rate of "+str(round(100*team.wins/(team.games),2))+"% win rate after "+str(team.games)+" games.")
    
    #tex = "\\documentclass{article}\n\\usepackage[a4paper,left=0cm,right=0cm,top=1cm,bottom=4cm,bindingoffset=0mm]{geometry}\n\\begin{document}\n\\bgroup\\def\\arraystretch{2}\\setlength\\tabcolsep{0.75mm}\n\\begin{tabular}{|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|}\n\\hline\n"

    #for team in teamList:
    #    tex += " & " + str(team.name)

    #tex += "\\\\\n\\hline\n"

    #for y in teamList:
    #     tex += str(y.name)

    #     for idx, x in enumerate(teamList):
    #         tex += " & " + y.results[idx]

    #     tex += "\\\\\n\\hline\n"

    # tex += "\\end{tabular}\n\\end{document}"

    # print(tex)

    #print("\n"+str(games*(len(survivors))*(len(survivors)-1))+" games were simulated. (Phase 2)")

    #print("ESC Games: "+str(esc.games))
    #print("ESC Wins: "+str(esc.wins))
    #print("ESC Looses: "+str(esc.defeats))
    #esc.allMatches(teamList)
    #print("Team "+str(esc.name)+" "+str(round(100*esc.wins/(esc.wins+esc.defeats),2))+"% win rate")
    #print(str(esc.wins))