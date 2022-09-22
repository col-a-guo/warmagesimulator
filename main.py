# TO DO LIST (roughly in order of importance):
# character creation
# wondrous items (definitely wincon, quicken rod. Stat boosters?)
# feats
# skillcheck floors
# achievements
# chests
# buffs/debuffs
# other classes

import os
import random
import string

wizardmode = True

print ("WARMAGE SIMULATOR")
print()
print("Warmage simulator is based on the 3.5 SRD as well as the Warmage class (see https://dndtools.net/classes/warmage/, or google 'dndtools warmage'). \n This is probably some kind of copyright infringement, but y'know, whatever. \nIf you need to look anything up, this follows those rulesets. \nIn particular, go to the warmage class and click the appropriate spell level and then the appropriate spell name to check the details of a spell.")
print()

def question(text, *options): #creates a list of options and returns the one that's chosen. If no valid choices are inputed, print "command not recognized" and try again.
    print('')
    print (str(text))
    print ("Options:")
    for opt in options:
        print (str(opt))
    flag = False
    while flag == False:
        result = input()    
        for opt in options:
            if result == opt:
                flag = True
        if flag == False:
            print("command not recognized")
    return result
    print('')

class Creature(): #stat blobs, used alone for monsters and w/player class for player
    def __init__(self, name, hp, init, bab, ac, tac, ffac, fort, ref, will, dmg, dmgbonus, atktype, range1, ab2, dmg2, dmgb2, atkt2, range2, ab3, dmg3, dmgb3, atkt3, range3, speed, level, tag, group):
        self.name = name #reference name
        self.maxhp = hp #unused
        self.hp = hp 
        self.init = init #initiative, used to determine turn order
        self.bab = bab #chance to hit
        self.ac = ac #chance to dodge most physical attacks
        self.tac = tac #chance to dodge certain magical attacks
        self.ffac = ffac #reduction to AC if turn hasn't been taken this combat
        self.fort = fort #chance to resist afflictions
        self.ref = ref #chance to dodge magic/trap based stuff
        self.will = will #chance to resist mental attacks
        self.dmg = dmg #physical damage (random number from 1 to damage)
        self.dmgbonus = dmgbonus #flat modifier to damage
        self.atktype = atktype
        self.range1 = range1
        self.ab2 = ab2
        self.dmg2 = dmg2
        self.dmgb2 = dmgb2
        self.atkt2 = atkt2
        self.range2 = range2
        self.ab3 = ab3
        self.dmg3 = dmg3
        self.dmgb3 = dmgb3
        self.atkt3 = atkt3
        self.range3 = range3
        self.speed = speed
        self.level = level #unused thus far
        self.tag = tag #potentially used for variable responses to spells (i.e. undead are immune to poison) - thus far unimplemented
        self.group = group #area of effect multiplier
        self.stun = 0 #marker for stunning - stunned creatures skip turns
        self.flatfooted = False #marker for if turn has been taken this combat
        self.damageOverTime = 0 #damage dealt to monster each turn


    def physicalAttack(self,effect, effectBonus, defender): #player weapons/monsters doing damage
        if effect == 500:
            if player.level > 4:
                defender.hp -= defender.hp//(6/random.randint(1,effectBonus))
            else:
                defender.hp -= defender.hp//(player.level/random.randint(1,effectBonus))
        else:
            damageDealt = (random.randint(1,effect)+effectBonus)
            defender.hp -= damageDealt
            print(str(damageDealt)+" damage dealt")

    def attack(self,attack,monster): # physical attacks
        if attack == "fullattack": #monster is within their primary attack range of the player
            if monster.range1 >= player.distance:
                atk1Succ = check(monster.bab,self.spellChecker(monster.atktype,player))
                if atk1Succ == True:
                    print("The monster hit!")
                    self.physicalAttack(monster.dmg,monster.dmgbonus,player)
                else:
                    print("The monster missed!")
            if monster.range2 >= player.distance:
                atk1Succ = check(monster.ab2,self.spellChecker(monster.atkt2,player))
                if atk1Succ == True:
                    print("The monster hit!")
                    self.physicalAttack(monster.dmg2,monster.dmgb2,player)
                else:
                    print("The monster missed!")
            if monster.range3 >= player.distance:
                atk1Succ = check(monster.ab3,self.spellChecker(monster.atkt3,player))
                if atk1Succ == True:
                    print("The monster hit!")
                    self.physicalAttack(monster.dmg3,monster.dmgb3,player)
                else:
                    print("The monster missed!")
        if attack == "charge": #monster was within 2x movespeed of player, and has charged
            atk1Succ = check(monster.bab+2,self.spellChecker(monster.atktype,player))
            if atk1Succ == True:
                self.physicalAttack(monster.dmg,monster.dmgbonus,player)
        if attack == "pAttack": #player hits monster with melee weapon
            if player.range1 >= player.distance:
                pSucc = check(player.bab+player.str,self.spellChecker("melee",monster))
                if pSucc == True:
                    player.physicalAttack(player.dmg,player.dmgbonus,monster)
                else:
                    print("you missed!")
            else:
                return("fail")
        if attack == "rangedAttack": #player hits monster with ranged weapon
            if player.range1*5  >= player.distance:
                pSucc = check(player.bab+player.dex-((player.distance//player.range1)*2),self.spellChecker("ranged",monster))
                if pSucc == True:
                    player.physicalAttack(player.dmg,player.dmgbonus,monster)
                else:
                    print("you missed!")
            else:
                return("fail")

    def spellChecker(self,spellType,defender): #checks any attack, not just spells, returns the appropriate defense numbers
        base = 0
        if str.find(spellType,"fort")>-1:
            base = defender.fort
        elif str.find(spellType,"ref")>-1:
            base =  defender.ref
        elif str.find(spellType,"will")>-1:
            base =  defender.will
        elif str.find(spellType,"touch")>-1:
            base =  defender.tac
        else:
            base =  defender.ac
        if defender.flatfooted == True:
            base -= (defender.ffac-10)
        return base


    def spellEffect(self,spellStats): #doles out effects of spells
        spellELevel = 0
        if spellStats[2] > player.level:
            spellELevel = player.level
        else:
            spellELevel = spellStats[2]
        spellDamage = 0
        if spellStats[0] > 696:
            self.damageOverTime = spellStats[0]-696
            print("you applied a "+str(spellStats[0]-696)+" damage DoT.")
        elif spellStats[0] > 695:
            self.stun = 100
            print("you applied a continuous stun!")
        elif spellStats[0] > 666:
            self.stun = random.randint(1,spellStats[0]-666)
            print("you applied a stun!")
        elif spellStats[0] > 69:
            for i in range (spellELevel):
                spellDamage += random.randint(1,spellStats[0]-69)
            spellDamage += player.int
            print("you applied a 1-turn stun!")
            self.stun = 1
        else:
            for i in range (spellELevel):
                spellDamage += random.randint(1,spellStats[0])
            spellDamage += player.int
        if str.find(spellStats[1],"area") > -1:
            spellDamage = spellDamage*monster.group
        print("you dealt "+str(spellDamage)+" damage!")
        self.hp -= spellDamage
    

    def spellAttack(self,spell,spellLevel):
        if spellLevel == "1":
            spellStats = listOfSpells1[spell]
            if spellStats[3] >= player.distance:
                if check(player.cha+1,self.spellChecker(spellStats[1],self)) == True:
                    self.spellEffect(spellStats)
                    return("it worked!")
                else:
                    return("the spell failed!")
            else:
                print("range insufficient")
        if spellLevel == "2":
            spellStats = listOfSpells2[spell]
            if spellStats[3] >= player.distance:
                if check(player.cha+2,self.spellChecker(spellStats[1],self)) == True:
                    self.spellEffect(spellStats)
                    return("it worked!")
                else:
                    return("the spell failed!")
            else:
                print("range insufficient")
        if spellLevel == '3':
            spellStats = listOfSpells3[spell]
            if spellStats[3] >= player.distance:
                if check(player.cha+3,self.spellChecker(spellStats[1],self)) == True:
                    self.spellEffect(spellStats)
                    return("it worked!")
                else:
                    return("the spell failed!")
        if spellLevel == '4':
            spellStats = listOfSpells4[spell]
            if spellStats[3] >= player.distance:
                if check(player.cha+4,self.spellChecker(spellStats[1],self)) == True:
                    self.spellEffect(spellStats)
                    return("it worked!")
                else:
                    return("the spell failed!")
        if spellLevel == '5':
            spellStats = listOfSpells5[spell]
            if spellStats[3] >= player.distance:
                if check(player.cha+5,self.spellChecker(spellStats[1],self)) == True:
                    self.spellEffect(spellStats)
                    return("it worked!")
                else:
                    return("the spell failed!")
        if spellLevel == '6':
            spellStats = listOfSpells6[spell]
            if spellStats[3] >= player.distance:
                if check(player.cha+6,self.spellChecker(spellStats[1],self)) == True:
                    self.spellEffect(spellStats)
                    return("it worked!")
                else:
                    return("the spell failed!")
        if spellLevel == '7':
            spellStats = listOfSpells7[spell]
            if spellStats[3] >= player.distance:
                if check(player.cha+7,self.spellChecker(spellStats[1],self)) == True:
                    self.spellEffect(spellStats)
                    return("it worked!")
                else:
                    return("the spell failed!")
        if spellLevel == '8':
            spellStats = listOfSpells8[spell]
            if spellStats[3] >= player.distance:
                if check(player.cha+8,self.spellChecker(spellStats[1],self)) == True:
                    self.spellEffect(spellStats)
                    return("it worked!")
                else:
                    return("the spell failed!")
        if spellLevel == '9':
            spellStats = listOfSpells9[spell]
            if spellStats[3] >= player.distance:
                if check(player.cha+9,self.spellChecker(spellStats[1],self)) == True:
                    self.spellEffect(spellStats)
                    return("it worked!")
                else:
                    return("the spell failed!")





kobold = Creature('kobold', 4, 3, 3, 15, 12, 14, 12, 11, 9, 3, 0, 'ranged', 50, -1, 6, -1, "melee", 5,0,0,0,"none",0,20, 1, 'human',1)
evilcat = Creature('evil cat', 2, 4, 4, 14, 14, 12, 12, 14, 11, 1, 0, 'melee', 5, 4, 1, 0, 'melee', 5, -1, 1, 0, 'melee', 5, 30, 1, 'animal',1)
evilpony = Creature('evil pony', 11, 1, -3, 13, 11, 12, 14, 14, 10, 3, 0, 'melee', 5, -3, 3, 0,"melee", 5, 0,0,0,"none",0,40, 1, 'animal',1)
listOfCreatures1 =[kobold, evilcat, evilpony]
evilhawk = Creature('evil hawk', 4, 3, 5, 17, 15, 14, 12, 15, 12, 3, -1, 'melee',5,3,3,-1,"melee",5,0,0,0,"none",0, 60, 1, 'animal',1)
skeleton = Creature('skeleton', 6, 5, 1, 15, 11, 14, 10, 11, 12, 4, 1, 'melee',5,5,4,1,"melee",5,0,0,0,"none",0, 30, 1, 'undead',1)
goblin = Creature('goblin', 5,1,3,15,12,13,13,11,9,4,0,'ranged',20,2,6,0,'melee',5,0,0,0,"none",0,30,1,'human',1)
listOfCreatures2 = [evilhawk,skeleton,goblin]
zombie = Creature('zombie',16,-1,2,11,9,11,10,9,13,6,1,'melee',5,0,0,0,"none",0,0,0,0,"none",0,30,2,'undead',1)
stirge = Creature('stirge',5,4,7,16,16,12,12,16,11,500,2,'melee',5,0,0,0,"none",0,0,0,0,"none",0,40,1,'weak',1)
evilelf = Creature('evil elf',4,3,1,15,11,14,12,11,9,8,1,'ranged',0,0,0,0,"none",0,0,0,0,"none",0,35,1,'human',1)
listOfCreatures3 = [zombie,stirge,evilelf]
spookywolf = Creature('spooky wolf',13,7,2,15,13,12,10,13,13,6,1,'melee',5,0,0,0,"none",0,0,0,0,"none",0,50,2,'undead',1)
listOfCreatures4 = [spookywolf]
whitedragon = Creature('White Dragon Wyrmling',22,7,5,17,15,14,14,16,12,8,3,'melee',5,2,8,0,"reflex",30,0,0,0,"none",0,200,3,'fire',1)
listOfCreatures5 = [whitedragon]
watermephit = Creature('water mephit',19,0,6,16,11,16,14,13,13,3,2,'melee',5,3,8,0,"reflex",15,0,0,0,"none",0,40,3,'none',1)
listOfCreatures6 = [watermephit]




class Player(Creature):
    def __init__(self,save,strength,dex,con,intelligence,wis,cha,level,dimDoor,shivTouch,teleport,floor):
        self.save = save
        self.str = strength
        self.dex = dex
        self.con = con
        self.int = intelligence
        self.wis = wis
        self.cha = cha
        self.dimDoor = dimDoor
        self.shivTouch = shivTouch
        self.teleport = teleport
        self.levelMarker = level
        self.floor = floor
        if self.save == False:
            print("CHARACTER CREATION")
            print("Step One: Set attributes")
            print("Your character has 6 attributes. Strength, Dexterity, Constitution, Intelligence, Wisdom, Charisma.")
            print("Strength determines your thrown/melee weapon damage, and melee accuracy.")
            print("Dexterty determines your dodge chance, initiative, and ranged accuracy.")
            print("Constitution determines your health and resistance to poison.")
            print("Intelligence determines your spell damage.")
            print("Wisdom determines your mental defense.")
            print("Charisma determines your spell accuracy and spells available.")
            print("Here are your attributes numbers:")
            stats = []
            skip = False
            stats.append(random.randint(1,6)+random.randint(1,6)+6)
            stats.append(random.randint(1,6)+random.randint(1,6)+6)
            stats.append(random.randint(1,6)+random.randint(1,6)+6)
            stats.append(random.randint(1,6)+random.randint(1,6)+6)
            stats.append(random.randint(1,6)+random.randint(1,6)+6)
            stats.append(random.randint(1,6)+random.randint(1,6)+6)
            print(stats)
            pointStats = [8,8,8,8,8,8]
            pointsLeft = 32
            pointBuyQ = question("You make take these rolls, or if you prefer, you can take a 32 point buy, or a prebuilt array. Pick one, and then (unless array was chosen) you will assign the numbers to the abilities.", "pointbuy", "array", "rolls")
            if pointBuyQ == "pointbuy":
                pointAddQ = "banana"
                while pointsLeft > 0 and pointAddQ != "done":
                    print("These are your stats (you will assign them to attributes later)")
                    print(pointStats)
                    print("You have "+str(pointsLeft)+" points left.")
                    print("+1 to a stat of 13 or lower costs 1. +1 to a stat of 14-15 costs 2. +1 to a stat of 16-17 costs 3.")
                    pointAddQ = question("What stat would you like to increase?",'0','1','2','3','4',"5","done")
                    if pointAddQ != "done":
                        cost = 1
                        if pointStats[int(pointAddQ)] > 13:
                            cost = 2
                        if pointStats[int(pointAddQ)] > 15:
                            cost = 3
                        if pointStats[int(pointAddQ)] > 17:
                            print("you can't go above 18!")
                        if cost <= pointsLeft:
                            pointStats[int(pointAddQ)] += 1
                            pointsLeft -= cost
                        else:
                            print("you don't have enough points!")
                    stats = pointStats
            if pointBuyQ == "array":
                skip = True
                self.cha = 3
                self.int = 2
                self.wis = -1
                self.con = 2
                self.dex = 1
                self.str = 2
            if skip != True:
                #placeholders
                self.cha = -3
                self.int = -3
                self.wis = -3
                self.con = -3
                self.dex = -3
                self.str = -3

                assignedStats = []
                while self.cha == -3 or self.int == -3 or self.wis == -3 or self.con == -3 or self.dex == -3 or self.str == -3: 
                    aFlag = True
                    print("Your stats are:")
                    print(stats)
                    print("You have assigned:")
                    print(assignedStats)
                    assignQ = question("Which stat would you like to assign?",'0','1','2','3','4','5')
                    attributeQ = question("Which attribute would you like to assign it to?","strength","dexterity","constitution","intelligence","wisdom","charisma")
                    if stats[int(assignQ)] != "assigned":
                        assignNum = stats[int(assignQ)]
                        stats[int(assignQ)] = "assigned"
                    else:
                        print("that stat has already been assigned!")
                        aFlag = False
                    if aFlag == True:
                        if attributeQ == "strength":
                            if self.str != "assigned":
                                self.str = (assignNum-10)//2
                                assignedStats.append("str:"+str(assignNum))
                            else:
                                print("that attribute has already been assigned!")
                        if attributeQ == "dexterity":
                            if self.dex != "assigned":
                                self.dex = (assignNum-10)//2
                                assignedStats.append("dex:"+str(assignNum))
                            else:
                                print("that attribute has already been assigned!")
                        if attributeQ == "constitution":
                            if self.con != "assigned":
                                self.con = (assignNum-10)//2
                                assignedStats.append("con:"+str(assignNum))
                            else:
                                print("that attribute has already been assigned!")
                        if attributeQ == "intelligence":
                            if self.int != "assigned":
                                self.int = (assignNum-10)//2
                                assignedStats.append("int:"+str(assignNum))
                            else:
                                print("that attribute has already been assigned!")
                        if attributeQ == "wisdom":
                            if self.wis != "assigned":
                                self.wis = (assignNum-10)//2
                                assignedStats.append("wis:"+str(assignNum))
                            else:
                                print("that attribute has already been assigned!")
                        if attributeQ == "charisma":
                            if self.cha != "assigned":
                                self.cha = (assignNum-10)//2
                                assignedStats.append("cha:"+str(assignNum))
                            else:
                                print("that attribute has already been assigned!")

            self.dimDoor = dimDoor
            self.shivTouch = shivTouch
            self.teleport = teleport
            self.floor = 0
        self.hp = 12+self.con
        self.bab = 0
        self.ac = self.dex+10
        self.tac = self.dex+10
        self.ffac = 10
        self.fort = self.con+10
        self.ref = self.dex+10
        self.will = self.wis+10
        self.dmg = 3
        self.range1 = 5
        self.dmgbonus = self.str
        self.atktype = "melee"
        self.speed = 30
        self.level = 1
        self.skills = []
        self.init = self.dex
        self.hpmax = 12+self.con
        self.gold = (random.randint(1,4)+random.randint(1,4)+random.randint(1,4))*10
        self.doorkeys = 0
        self.chestkeys = 0
        self.acheck = 0
        self.exp = 0
        self.days = 0
        self.spellslots = [3+(3+self.cha)//4,0,0,0,0,0,0,0,0]
        self.currentslots = [3+(3+self.cha)//4,0,0,0,0,0,0,0,0]
        self.flatfooted = False
        self.quickenL = False
        self.quickenM = False
        self.quickenG = False
        self.quickenCharge = 3
        self.enhanceAC = 0
        self.enhanceAtk = 0
        self.maximize = False
        self.maximizeCharge = 3


    def saveGame(self):
        saved = (open("warmageSimSave.txt","w"))
        saved.write(str(self.str)+" "+str(self.dex)+" "+str(self.con)+" "+str(self.int)+" "+str(self.wis)+" "+str(self.cha)+" "+str(self.level)+" "+str(self.dimDoor)+" "+str(self.shivTouch)+" "+str(self.teleport)+" "+str(self.floor))
        os.exit(1)

    def updateSpells(self):
        #updates level-variable aspects of spells
        #spells are ordered [damage per level, attack type, level cap, range]
        global listOfSpells1
        global listOfSpells2
        global listOfSpells3
        global listOfSpells4
        global listOfSpells5
        global listOfSpells6
        global listOfSpells7
        global listOfSpells8
        global listOfSpells9
        listOfSpells1 = {"lesseracidorb":[3,"rangedTouch",10,25+(self.level*5)//2],"lesserfireorb":[3,"rangedTouch",10,5+(self.level*5)//2],"lessercoldorb":[3,"rangedTouch",10,5+(self.level*5)//2],"lessersonicorb":[3,"rangedTouch",10,5+(self.level*5)//2],"lesserelectricorb":[3,"rangedTouch",10,5+(self.level*5)//2],"burninghands":[4,"areaReflex",5,15],"shockinggrasp":[6,"meleeTouch",5,5]}
        listOfSpells2 = {"scorchingray":[6,"rangedTouch",12,25+(self.level*5)//2],"fireburst":[8,"area",5,5],"acidarrow":[704,"rangedTouch",1,400+(self.level*40)],"flamingsphere":[716,"areaRef",1, 100+(self.level*10)]}
        listOfSpells3 = {"fireball":[6,"areaRef",10,400+self.level*40],"lightningbolt":[6,"areaRef",10,120],"stinkingcloud":[670,"areaFort",1,100+(self.level*10)],"sleetstorm":[696,"areaRef",1,400+(self.level*40)]}
        listOfSpells4 = {"blacktentacles":[696,"areaRef",1,100+10*self.level],"contaigon":[665, "meleeTouch", 1, 5],"orboffire":[75,"rangedTouch",10,25+(self.level*5)//2],"orbofcold":[75,"rangedTouch",10,25+(self.level*5)//2],"orbofacid":[75,"rangedTouch",10,25+(self.level*5)//2],"orbofelectricity":[75,"rangedTouch",10,25+(self.level*5)//2],"orbofsonic":[75,"rangedTouch",10,25+(self.level*5)//2]}
        listOfSpells5 = {"greaterfireburst":[12,"areaRef",10,10], "coneofcold":[6,"areaRef",15,60], "flamestrike":[6,"areaRef",15,100+10*self.level], "arclightning":[6,"areaRef",15,100+10*self.level], "cloudkill":[700,"areaFort",20,100+10*self.level],}
        listOfSpells6 = {""}
        listOfSpells7 = {}
        listOfSpells8 = {}
        listOfSpells9 = {}
        self.currentslots = self.spellslots 

    def levelUp(self): #updates stats for a new level
        self.exp = 0
        if self.level > 9:
            print("You're at the current level cap.")
            self.exp = 0
        else:    
            self.level = self.level+1
            print("You are level "+str(self.level))
            if self.level > 4:
                self.hp = self.level*(self.level//3+2+self.con)
            else:
                self.hp = 6+6*self.level
            print("Your hp is "+str(self.hp))
            self.bab = self.level//2+self.str
            print("Your attack bonus is "+str(self.bab))
            self.ref = self.level//3+self.dex
            print("Your reflex bonus is "+str(self.ref))
            self.fort = self.level//3+self.con
            print("Your fortitude bonus is "+str(self.fort))
            self.will = self.level//2+2+self.wis
            print("Your will bonus is "+str(self.will))
            for spellLevel in range(1,10):
                if self.level > spellLevel*2-2:
                    if self.level < spellLevel*2+2:
                        self.spellslots[spellLevel] = self.level-spellLevel*2+5
                    else:
                        self.spellslots[spellLevel] = 7
                    print("You have "+str(self.spellslots[spellLevel])+" spells of "+str(spellLevel)+"th level.")
            self.updateSpells()

player = Player(True,8,8,8,8,8,8,1,0,0,0,0)

def load():
    saved = (open("warmageSimSave.txt","a"))
    saved = (open("warmageSimSave.txt","r"))
    saveLine = saved.readline()
    splitSave = saveLine.split(" ")
    strength = int(splitSave[0])
    dex = int(splitSave[1])
    con = int(splitSave[2])
    intelligence =int(splitSave[3])
    wis = int(splitSave[4])
    cha = int(splitSave[5])
    level = int(splitSave[6])
    dimDoor = int(splitSave[7])
    shivTouch = int(splitSave[8])
    teleport = int(splitSave[9])
    floor = int(splitSave[10])
    player = Player(True,strength,dex,con,intelligence,wis,cha,level,dimDoor,shivTouch,teleport,floor)
    for i in range(int(level)-1):
        player.levelUp()
    saved = (open("warmageSimSave.txt","w"))
    saved.write("")

mainMenu = question("Do you have a game to load?", "yes", "no")
if mainMenu == "yes":
    load()
else:
    player = Player(False,8,8,8,8,8,8,1,0,0,0,0)


if wizardmode == True:
    player.levelUp()
    player.levelUp()
    player.levelUp()
    player.levelUp()
    player.levelUp()
    player.levelUp()
    player.levelUp()
    player.levelUp()
    player.levelUp()
    player.levelUp()
    player.levelUp()
    player.levelUp()
    player.gold = 100000
player.updateSpells

monster = Creature('water mephit',19,0,6,16,11,16,14,13,13,3,2,'melee',5,3,8,0,"reflex",15,0,0,0,"none",0,40,3,'none',1)

listOfSpells1 = {"lesseracidorb":[3,"rangedTouch",10,25+(5)//2],"lesserfireorb":[3,"rangedTouch",10,5+(5)//2],"lessercoldorb":[3,"rangedTouch",10,5+(5)//2],"lessersonicorb":[3,"rangedTouch",10,5+(5)//2],"lesserelectricorb":[3,"rangedTouch",10,5+(5)//2],"burninghands":[4,"areaReflex",5,15],"shockinggrasp":[6,"meleeTouch",5,5]}
listOfSpells2 = {"scorchingray":[6,"rangedTouch",12,25+(5)//2],"fireburst":[8,"area",5,5],"acidarrow":[704,"rangedTouch",1,400+(40)],"flamingsphere":[716,"areaRef",1, 100+(10)]}
listOfSpells3 = {"fireball":[6,"areaRef",10,400+40],"lightningbolt":[6,"areaRef",10,120],"stinkingcloud":[670,"areaFort",1,100+(10)],"sleetstorm":[696,"areaRef",1,400+(40)]}
listOfSpells4 = {"blacktentacles":[696,"areaRef",1,100+10],"contaigon":[665, "meleeTouch", 1, 5],"orboffire":[75,"rangedTouch",10,25+(5)//2],"orbofcold":[75,"rangedTouch",10,25+(5)//2],"orbofacid":[75,"rangedTouch",10,25+(5)//2],"orbofelectricity":[75,"rangedTouch",10,25+(5)//2],"orbofsonic":[75,"rangedTouch",10,25+(5)//2]}
listOfSpells5 = {"greaterfireburst":[12,"areaRef",10,10], "coneofcold":[6,"areaRef",15,60], "flamestrike":[6,"areaRef",15,100+10], "arclightning":[6,"areaRef",15,100+10], "cloudkill":[700,"areaFort",20,100+10],}
listOfSpells6 = {}
listOfSpells7 = {}
listOfSpells8 = {}
listOfSpells9 = {}




def printSituation():
    print("you are on floor "+str(player.floor))
    print("it is a "+str(floortype))

def printStats():
    print("hit points: "+str(player.hp))
    print("fortitude: "+str(player.fort))
    print("reflex: "+str(player.ref))
    print("will: "+str(player.will))
    print("base attack bonus: "+str(player.bab))
    print("armor class: "+str(player.ac))



def goldcheck(gold):
    if player.gold > gold:
        return True
    else:
        print("you don't have enough money!")
        return False

def check(bonus, DC):
    result = random.randint(1,20)
    if result+bonus >= DC:
        return True
    else:
        return False

done = False

def playerTurn(monster):
    standard = 1
    move = 1
    swift = 1
    turnLoop = True
    while turnLoop == True and monster.hp > 0:
        turnChoice = "banana"
        if standard == 0 and move == 0:
            print("You're out of actions! End of turn.")
            turnChoice = "end turn"
        else:
            turnChoice = question("It is your turn. What would you like to do?", "attack", "cast", "retreat", "advance", "end turn")
        if turnChoice == "attack":
            if standard > 0:
                if player.atktype == "melee":
                    attackSucc = player.attack("pAttack",monster)
                    if attackSucc == "fail":
                        print("You're not in range!")
                    else:
                        standard -= 1
                if player.atktype == "ranged":
                    attackSucc = player.attack("rangedAttack",monster)
                    if attackSucc == "fail":
                        print("You're not in range!")
                    else:
                        standard -= 1
            else:
                print("You don't have the actions!")
        if turnChoice == "cast":
            if standard < 1:
                print ("you don't have the actions!")
            else:
                spellLevelQ = question("What level of spell would you like to cast?", "1", "2", "3","4","5","6","7","8","9", "none")
                spell = "nah"
                if spellLevelQ == "1":
                    if player.currentslots[0] > 0:
                        spellQ = question("What spell?", "lesseracidorb", "lesserelectricorb", "lessersonicorb", "lessercoldorb", "lesserfireorb", "burninghands", "shockinggrasp")
                        spell = spellQ
                if spellLevelQ == "2":
                    if player.currentslots[1] > 0:
                        spellQ = question("What spell?", "scorchingray", "fireburst", "acidarrow", "flamingsphere")
                        spell = spellQ
                if spellLevelQ == "3":
                    if player.currentslots[2] > 0:
                        spellQ = question("What spell?", "fireball", "lightningbolt", "stinkingcloud", "sleetstorm")
                        spell = spellQ
                if spellLevelQ == "4":
                    if player.currentslots[3] > 0:
                        spellQ = question("What spell?", "blacktentacles", "orboffire", "orbofsonic", "orbofelectricity", "orbofcold", "orbofacid",
                         "contaigon")
                        spell = spellQ
                if spellLevelQ == "5":
                    if player.currentslots[4] > 0:
                        spellQ = question("What spell?", "greaterfireburst", "flamestrike", "arclightning", "coneofcold", "cloudkill")
                        spell = spellQ
                if spellLevelQ == "6":
                    print("not implemented")
                if spellLevelQ == "7":
                    print("not implemented")
                if spellLevelQ == "8":
                    print("not implemented")
                if spellLevelQ == "9":
                    print("not implemented")
                if spell != "nah":
                    filler = monster.spellAttack(spell,spellLevelQ)
                    if filler == "the spell failed!" or filler == "it worked!":
                        print(filler)
                        player.spellslots[int(spellLevelQ)] -= 1
                        standard -= 1
                    else:
                        print (filler)
                elif spellLevelQ == "none":
                    spell = "nah"
                else:
                    print("you don't have those spells!")
        if turnChoice == "retreat":
            if move > 0:
                move -= 1
                player.distance += player.speed
                print("Distance from monster: "+str(player.distance))
            elif standard > 0:
                standard -= 1
                player.distance += player.speed
                print("Distance from monster: "+str(player.distance))
            else:
                print("you don't have the actions!")
        if turnChoice == "advance":
            if move > 0:
                move -= 1
                player.distance -= player.speed
                if player.distance < 5:
                    player.distance = 5
                print (player.distance)
            elif standard > 0:
                standard -= 1
                player.distance -= player.speed
                if player.distance < 5:
                    player.distance = 5

                print (player.distance)
            else:
                print("you don't have the actions!")
        if turnChoice == "quicken":
            if swift < 1:
                print ("you don't have the actions!")
            else:
                spellLevelQ = question("What level of spell would you like to cast?", "1", "2", "3","4","5","6","7","8","9", "none")
                spell = "nah"
                if spellLevelQ == "1":
                    if player.currentslots[0] > 0:
                        spellQ = question("What spell?", "lesseracidorb", "lesserelectricorb", "lessersonicorb", "lessercoldorb", "lesserfireorb", "burninghands", "shockinggrasp")
                        spell = spellQ
                if spellLevelQ == "2":
                    if player.currentslots[1] > 0:
                        spellQ = question("What spell?", "scorchingray", "fireburst", "acidarrow", "flamingsphere")
                        spell = spellQ
                if spellLevelQ == "3":
                    if player.currentslots[2] > 0:
                        spellQ = question("What spell?", "fireball", "lightningbolt", "stinkingcloud", "sleetstorm")
                        spell = spellQ
                if spellLevelQ == "4":
                    if player.currentslots[3] > 0:
                        spellQ = question("What spell?", "blacktentacles", "orboffire", "orbofsonic", "orbofelectricity", "orbofcold", "orbofacid",
                         "contaigon")
                        spell = spellQ
                if spellLevelQ == "5":
                    if player.currentslots[4] > 0:
                        spellQ = question("What spell?", "greaterfireburst", "flamestrike", "arclightning", "coneofcold", "cloudkill")
                        spell = spellQ
                if spellLevelQ == "6":
                    print("not implemented")
                if spellLevelQ == "7":
                    print("not implemented")
                if spellLevelQ == "8":
                    print("not implemented")
                if spellLevelQ == "9":
                    print("not implemented")
                if spell != "nah":
                    filler = monster.spellAttack(spell,spellLevelQ)
                    if filler == "the spell failed!" or filler == "it worked!":
                        print(filler)
                        player.spellslots[int(spellLevelQ)] -= 1
                        swift -= 1
                    else:
                        print (filler)
                elif spellLevelQ == "none":
                    spell = "nah"
                else:
                    print("You don't have those spells!")
        if turnChoice == "end turn":
            turnLoop = False



def fight(monsterList):
    randomMonster = random.randint(0,len(monsterList)-1)
    monster = monsterList[randomMonster]
    initiativeMonster = random.randint(1,20)+monster.init
    initiativeHero = random.randint(1,20)+player.init
    player.distance = random.randint(1,100)*5
    print ("You are fighting "+str(monster.name))
    turn = "hero"
    if initiativeHero > initiativeMonster:
        turn = "hero"
        monster.flatfooted = True
    else:
        turn = "monster"
        player.flatfooted = True
    while player.hp > 0 and monster.hp > 0:
        if turn == "hero" and player.hp > 0:
            print("Your hp: "+str(player.hp))
            print("Monster hp: "+str(monster.hp))
            print("Distance from monster: "+str(player.distance))
            playerTurn(monster)
            monster.flatfooted = False
            turn = "monster"
        if turn == "monster" and monster.hp > 0:
            print("It is the monster's turn!")
            monster.hp -= monster.damageOverTime 
            if monster.stun == 100:
                escapeSucc = check (monster.bab,player.cha+14)
                if escapeSucc == True:
                    monster.stun = 0
            elif monster.stun > 0:
                monster.stun -= 1
            else:
                if player.distance > monster.range1 and player.distance > monster.range2 and player.distance > monster.range3:
                    player.distance -= monster.speed
                    if player.distance > monster.speed*3:
                        player.distance -= monster.speed*3
                        print("The monster ran at you!")
                    elif player.distance >= monster.speed:
                        player.distance = 5
                        print("the monster ran at you!")
                    else:
                        player.distance = 5
                        print("the monster charged!")
                        monster.attack("charge",monster)
                else:
                    print("the monster full attacked!")
                    monster.attack("fullattack",monster)
            player.flatfooted = False
            turn = "hero"
    if player.hp < 0:
        print("YOU DIED")
    if monster.hp < 0:
        print("You beat the monster!")
        monster.hp = monster.maxhp




def loot(level):
    goldEarned = random.randint(level*80,level*120)
    player.gold += goldEarned
    print("")
    print("you earned "+str(goldEarned)+" gold!")
    print("")




playing = True


while playing:
    print('')
    if player.hp < 0:
        print("YOU DIED")
        replayQ = question("Would you like to continue?", 'yes', 'no')
        if replayQ == "no":
            quit()
        if replayQ == "yes":
            dimDoor = player.dimDoor
            shivTouch = player.shivTouch
            teleport = player.teleport
            player = Player(False,8,8,8,8,8,8,1,dimDoor,shivTouch,teleport,0)
    if player.exp > player.level*1000:
        print("LEVEL UP!")
        player.levelUp()
    if player.floor == 0:
        print("You are in the village.")
    else:
        print("you are on floor "+str(player.floor))
    if player.floor == 0:
        done = False
        while done == False:
            print ("you have "+str(player.gold)+" gold")
            shoppingChoice = question("Would you like to buy something?", 'healing', 'items', 'rest', 'no')
            if shoppingChoice == 'healing':
                print ("you have "+str(player.gold)+" gold")
                cont = True
                while player.gold > 10 and player.hp < player.hpmax and cont != False:
                    player.gold -= 10
                    healingAmount = randint(2,9)
                    player.hp += healingAmount
                    if player.hp > player.hpmax:
                        player.hp = player.hpmax
                    print("You've been healed for "+str(healingAmount)+" hp, to a total of "+str(player.hp)+'/'+str(player.hpmax))
                    healQ = question("keep healing?", "yes", "no")
                    if healQ == "no":
                        cont = False
            if shoppingChoice == 'items':
                cont = True
                while cont != False:
                    print ("you have "+str(player.gold)+" gold")
                    itemQ = question("What type of item would you like to buy?", 'armor', 'weapons', 'win the game', 'none')
                    if itemQ == 'armor':
                        print('"Welcome to the armor shop." \n padded - 5 gold, +1 ac \n leather - 10 gold, +2 ac \n studded leather - 25 gold, +3 ac \n chainshirt - 100 gold, +4 ac \n breastplate - 200 gold, +5 ac, level 8+ only, \n mithral fullplate - 10500 gold, +8 ac, level 8+ only')
                        armorQ = question("What type of armor would you like?", 'padded','leather','studded','chainshirt','breastplate','mithral fullplate')
                        if armorQ == 'padded':
                            if goldcheck(5) == True:
                                player.acheck = 0
                                player.ac = 14
                        if armorQ == 'leather':
                            if goldcheck(10) == True:
                                player.acheck = 1
                                player.ac = 15
                        if armorQ == 'studded':
                            if goldcheck(25) == True:
                                player.acheck = 1
                                player.ac = 16
                        if armorQ == 'chainshirt':
                            if goldcheck(100) == True:
                                player.acheck = 2
                                player.ac = 17
                        if armorQ == 'breastplate':
                            if player.level > 7:
                                if goldcheck(200) == True:
                                    player.acheck = 4
                                player.ac = 18
                        if armorQ == 'mithral fullplate':
                            if player.level > 7:
                                if goldcheck(10500) == True:
                                    player.acheck = 4
                                player.ac = 20

                    if itemQ == 'weapons':
                        print('"Welcome to the weapon shop." \n sling - 1 gp, range 50, dmg 1d4, no dmg bonus \n javelins - 10 gp, range 30, dmg 1d6, str to dmg \n spears - 10 gp, range 20, dmg 1d8, str to dmg \n quarterstaff - 0 gp, range 5, dmg 1d8, x1.5 str to dmg \n greataxe - 50 gp, range 5, dmg 1d12, x1.5 str to dmg, requires feat \n composite longbow - 100 gp + 75 gp/str, range 110, dmg 1d8, str to dmg, requires feat \n fullblade - 150 gp, range 5, dmg 1d20, x1.5 str to dmg, requires feat \n footbow - ')
                        weaponQ = question("What type of weapon would you like?", 'sling', 'javelins', 'spears', 'quarterstaff', 'composite longbow', 'fullblade')
                        if weaponQ == 'sling':
                            if goldcheck(1) == True:
                                player.atktype = "ranged"
                                player.range1 = 50
                                player.dmg = 4
                                player.dmgbonus = 0
                        if weaponQ == 'javelins':
                            if goldcheck(10) == True:
                                player.atktype = "ranged"
                                player.range1 = 30
                                player.dmg = 6
                                player.dmgbonus = player.str
                        if weaponQ == 'spears':
                            if goldcheck(10) == True:
                                player.atktype = "ranged"
                                player.range1 = 20
                                player.dmg = 8
                                player.dmgbonus = player.str
                        if weaponQ == 'quarterstaff':
                            player.atktype = "melee"
                            player.range1 = 20
                            player.dmg = 8
                            player.dmgbonus = (player.str*1.5)//1
                        if weaponQ == 'fullblade':
                            flag = False
                            for wep in player.profList:
                                if wep == 'fullblade':
                                    flag = True
                            if flag == True:
                                if goldcheck(150) == True:
                                    player.atktype = "melee"
                                    player.range1 = 5
                                    player.dmg = 20
                                    player.dmgbonus = (player.str*1.5)//1
                            else:
                                print("You don't have Weapon Proficiency in that weapon!")
                        if weaponQ == 'composite longbow':
                            flag = False
                            for wep in player.profList:
                                if wep == 'composite longbow':
                                    flag = True
                            if flag == True:
                                if goldcheck(100+75*player.str) == True:
                                    player.atktype = "ranged"
                                    player.range1 = 110
                                    player.dmg = 8
                                    player.dmgbonus = player.str
                            else:
                                print("You don't have Weapon Proficiency in that weapon!")
                        if weaponQ == 'talenta sharrash':
                            flag = False
                            for wep in player.profList:
                                if wep == 'talenta sharrash':
                                    flag = True
                            if flag == True:
                                if goldcheck(50) == True:
                                    player.atktype = "melee"
                                    player.range1 = 10
                                    player.dmg = 8
                                    player.dmgbonus = (player.str*1.5)//1
                            else:
                                print("You don't have Weapon Proficiency in that weapon!")

                    if itemQ == 'win the game':
                        winQ = question("Are you sure? Winning the game is only 8400 gp, but you may want to get more achievements.", "yes", "no")
                        if goldcheck(8400) == True:
                            print("YOU WIN!")

                            dimDoor = player.dimDoor
                            shivTouch = player.shivTouch
                            teleport = player.teleport
                            player = Player(False,8,8,8,8,8,8,1,dimDoor,shivTouch,teleport,0)
                    doneQ = question("keep buying items?", "yes", "no")
                    if doneQ == 'no':
                        cont = False
            if shoppingChoice == 'rest':
                if goldcheck(10*player.level) == True:
                    print("You rest a day, regaining spells and health.")
                    player.currentslots = player.spellslots
                    player.hp += 2*player.level
                    if player.hp > player.hpmax:
                        player.hp = player.hpmax
                    player.days += 1
            if shoppingChoice != 'no':
                doneQ = question("keep shopping?", "yes", "no")
                if doneQ == 'no':
                    done = True
            else:
                done = True
    elif player.floor > 0 and player.floor < 4:
        fight(listOfCreatures1)
        player.exp += 300
        loot(1)
    elif player.floor > 3 and player.floor < 7:
        fight(listOfCreatures2)
        player.exp += 600
        loot(2)
    elif player.floor > 6 and player.floor < 10:
        fight(listOfCreatures3)
        player.exp += 900
        loot(3)
    elif player.floor > 9 and player.floor < 13:
        fight(listOfCreatures4)
        player.exp += 1350
        loot(6)
    elif player.floor == 14:
        print("the floor here is cold to the touch")
        if player.doorkeys < 1:
            firstBossQ = question("are you sure you want to continue?", "yes", "no")
            if firstBossQ == "yes":
                fight(listOfCreatures5)
                player.exp += 1800
                playerfloor = 15
                player.doorkeys = 1
                loot(10)
        else:
            restQ = question("No monsters dare enter the dragon's lair. Would you like to rest?", "yes", "no")
            if restQ == "yes":
                player.currentslots = player.spellslots
                player.hp += 2*player.level
                if player.hp > player.hpmax:
                    player.hp = player.hpmax
                player.days += 1

    elif player.floor > 14 and player.floor < 17:
        fight(listOfCreatures6)
        player.exp += 2700
        loot(9)
    elif player.floor > 18:
        print("unimplemented")
        player.floor = 0
    floormove = "banana"
    if player.floor == 0:
        print("Would you like to leave the village (floor 0)?")
        villagemove = question("","yes","no")
        if villagemove == "yes":
            player.floor += 1
    else:
        floormove = question("Would you like to go up or down?", "up", "down")
    if floormove == "up":
        player.floor += 1
    if floormove == "down":
        if player.floor > 0:
            player.floor -= 1
        else:
            print("You're already in town!")
    saveQ = question("Would you like to save and quit?","yes","no")
    if saveQ == "yes":
        player.saveGame()