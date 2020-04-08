import random
import math
import config

print(config.amateur)

class Team():
    def __init__(self,name,t,a,v,m,s):
        self.name=name
        self.t=t
        self.a=a
        self.v=v
        self.m=m
        self.s=s
        self.wins=0
        self.defeats=0
        self.games=0
        #self.results=[]
        if t*2+a*2+v+m+s != config.amateur:
            print("Team "+str(self.name)+" does not have the right amount of WP!")
        if v>3*m or v>3*s or m>3*v or m>3*s or s>3*v or s>3*m:
            print("3:1 REDUKTION!")

    @classmethod
    def random(cls,wp,comb):
        # Constraints:
            # 3:1 Regel
            # T,A <=10
            # randomize row order
        t=0
        a=0
        v=0
        m=0
        s=0

        rand = random.randint(0,comb[0][10])
        t=0
        while comb[0][t] < rand:
            t=t+1


        rand = random.randint(0,comb[t][10])
        a=0
        while comb[t][a] < rand:
            a=a+1


        vms = wp-t*2-a*2

        first = random.randint(math.ceil(vms/7),vms-2*math.ceil(vms/5))
        
        vms = vms - first

        low = max(math.ceil(first/3),math.ceil(vms/4),math.ceil(vms-first*3))
        high = min(first*3,math.floor(vms*0.75),math.floor(vms-first/3))

        second = random.randint(low,high)
        third = vms-second

        rnd = random.randint(1,6)
        if rnd==1:
            v = first
            m = second
            s = third
        elif rnd==2:
            v = first
            m = third
            s = second
        elif rnd==3:
            v = second
            m = first
            s = third
        elif rnd==4:
            v = second
            m = third
            s = first
        elif rnd==5:
            v = third
            m = first
            s = second
        elif rnd==6:
            v = third
            m = second
            s = first

        name = str(t)+"-"+str(a)+"-"+str(v)+"-"+str(m)+"-"+str(s)
        print(name)

        return cls (name, t, a, v, m, s)

    def win_rate(self):
        return self.wins/self.games

    def log(self):
        print(str(self.t)+"-"+str(self.a)+"-"+str(self.v)+"-"+str(self.m)+"-"+str(self.s))

    def playAgainst(self,opp):
        if config.verbose:
	        print("Team "+str(self.name)+" vs. Team "+str(opp.name))

        ownChances = 0
        oppChances = 0

        if self.s>opp.a+opp.v:
            ownChances+=(self.s-opp.a-opp.v)
        elif opp.v>self.s:
            oppChances+=round((opp.v-self.s)/4)
        if self.m>opp.m:
            ownChances+=round((self.m-opp.m)/2)
        else:
            oppChances+=round((opp.m-self.m)/2)
        if opp.s>self.v+self.a:
            oppChances+=(opp.s-self.v-self.a)
        elif self.v>opp.s:
            ownChances+=round((self.v-opp.s)/4)
        
        if config.verbose:
            print("Chances: "+str(ownChances) + " - " + str(oppChances))


        tieOwnChances = 0
        tieOppChances = 0
        
        if self.s>opp.a+opp.v:
            tieOwnChances+=round((self.s-opp.a-opp.v)/3)
        elif opp.v>self.s:
            tieOppChances+=round((opp.v-self.s)/4/3)
        if self.m>opp.m:
            tieOwnChances+=round((self.m-opp.m)/2/3)
        else:
            tieOppChances+=round((opp.m-self.m)/2/3)
        if opp.s>self.v+self.a:
            tieOppChances+=round((opp.s-self.v-self.a)/3)
        elif self.v>opp.s:
            tieOwnChances+=round((self.v-opp.s)/4/3)    

        i = 0
        ownWins = 0
        oppWins = 0
        ties = 0
        for i in range(config.games):
            self.games+=1
            opp.games+=1
            if config.verbose:
                print("")
                print("Game "+str(i))

            ownGoals = 0
            oppGoals = 0

            #print(str(random.randrange(1,15)))

            #random.randrange(1,15)>opp.a &
            # random.randrange(1,15)>self.a &

            for o in range(ownChances):
                if random.randint(1,14)>=opp.t and random.randint(1,15)>=opp.a:
                    ownGoals += 1
            for o in range(oppChances):
                if random.randint(1,14)>=self.t and random.randint(1,15)>=self.a:
                    oppGoals += 1

            if config.verbose:
                print(str(ownGoals)+" - "+str(oppGoals))

            if ownGoals == oppGoals:
                # Unentschieden nach 90 Minuten
                
                if config.verbose:
                    print("Unentschieden nach 90 Minuten")

                for o in range(tieOwnChances):
                    if random.randrange(1,14)>opp.t and random.randrange(1,15)>opp.a:
                        ownGoals += 1
                for o in range(tieOppChances):
                    if random.randrange(1,14)>self.t and random.randrange(1,15)>self.a:
                        oppGoals += 1

                if config.verbose:
                    print(str(ownGoals)+" - "+str(oppGoals))
                
                if ownGoals == oppGoals:
                    if config.verbose:
                        print("Unentschieden nach Verlängerung")
                    if self.t == 0 and opp.t == 0:
                        while ownGoals == oppGoals:
                            for p in range(5):
                                if random.randrange(1,14)>10:
                                    ownGoals += 1
                                if random.randrange(1,14)>10:
                                    oppGoals += 1
                    else: 
                        while ownGoals == oppGoals:
                            for p in range(5):
                                if random.randrange(1,14)>opp.t:
                                    ownGoals += 1
                                if random.randrange(1,14)>self.t:
                                    oppGoals += 1
                    
                    if config.verbose:
                        print(str(ownGoals)+" - "+str(oppGoals))         
            if ownGoals > oppGoals:
                ownWins += 1
                if config.verbose:
                    print("Win!")
            elif oppGoals > ownGoals:
                oppWins += 1
                if config.verbose:
                    print("Loose!")
            else:
                print("THIS CODE SHOULD BE UNREACHABLE!!!")

        #print("Team "+str(self.name)+" has won "+str(ownWins)+" of "+str(games)+" games against Team "+str(opp.name))

        self.wins += ownWins
        opp.defeats += ownWins
        self.defeats += oppWins
        opp.wins += oppWins
        #self.results.append(str(round(100*ownWins/games,digits))+"\\%")

    def allMatches(self,teams):
        print("Simulating for Team "+str(self.name))
        for opp in teams:
            if opp.name != self.name:
                self.playAgainst(opp)
            #else:
            #    self.results.append("-")