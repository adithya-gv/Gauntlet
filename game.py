import random
import time

class Character:

    def __init__(self, name, level):
        self.name = name
        self.level = level
        
        self.atkMod = (int)((0.4 * random.uniform(0, 1) + 0.8) * 10)
        self.defMod = (int)((0.4 * random.uniform(0, 1) + 0.8) * 10)
        self.spdMod = (int)((0.4 * random.uniform(0, 1) + 0.8) * 5)
        self.hpMod = (int)((0.4 * random.uniform(0, 1) + 0.8) * 12)
        
        self.maxHp = 10 + self.hpMod
        self.baseAtk = 6 + self.atkMod
        self.baseDef = 6 + self.defMod
        self.baseSpd = 3 + self.spdMod

        self.hp = 0
        self.atk = 0
        self.df = 0
        self.spd = 0

        self.XP = 0
        self.updateStats(0)
    
    def updateStats(self, prevLevel):
        for i in range(prevLevel, self.level):
            self.maxHp = self.maxHp + (int)(2 * ((random.uniform(0, 1)) + 0.6) + (i / 5.0))
            self.baseAtk = self.baseAtk + (int)(1.5 * ((random.uniform(0, 1)) + 0.6) + (i / 5.0))
            self.baseDef = self.baseDef + (int)(1 * ((random.uniform(0, 1)) + 0.6) + (i / 5.0))
            self.baseSpd = self.baseSpd + (int)(0.5 * ((random.uniform(0, 1)) + 0.6) + (i / 5.0))
    
    def getStats(self):
        print("Level: " + str(self.level))
        print("HP: " + str(self.hp))
        print("Attack: " + str(self.atk))
        print("Defense: " + str(self.df))
        print("Speed: " + str(self.spd))

    def reset(self):
        self.hp = self.maxHp
        self.atk = self.baseAtk
        self.df = self.baseDef
        self.spd = self.baseSpd
    
    def damage(self, opponent, r):
        num = (float)(pow(self.atk, 1.5))
        den = (float)(opponent.df)
        modifier = (float)(self.level / opponent.level)
        change = (int)(num / den * modifier * r)
        if (change < 1):
            change = 1
        if (change > opponent.hp):
            change = opponent.hp
        opponent.hp = opponent.hp - change
        return change

    def punch(self, opponent):
        chance = random.uniform(0, 1)
        if (chance < 0.95):
            change = self.damage(opponent, (self.level / 10.0) * random.uniform(0.85, 1) + 1)
            print(self.name + "\'s Punch Hit! Dealt " + str(change) + " damage!")
        else:
            print(self.name + "\'s Punch Missed!")

    def kick(self, opponent):
        chance = random.uniform(0, 1)
        if (chance < 0.8):
            change = self.damage(opponent, (self.level / 10.0) * random.uniform(0.85, 1) + 1.6)
            print(self.name + "\'s Kick Hit! Dealt " + str(change) + " damage!")
            self.df = (int)(self.df * 0.5)
            print(self.name + "\'s defense dropped a lot!")
        else:
            print(self.name + "\'s Kick Missed!")
        
    def block(self):
        print(self.name + " is gathering strength for a block. Their defense increased!")
        self.df = (int)(self.df * 1.4)
        HPChange = (int)(0.05 * self.maxHp)
        if (HPChange > self.hp):
            HPChange = self.hp
        print(self.name + " lost " + str(HPChange) + " HP!")
        self.hp = self.hp - HPChange
    
    def focus(self):
        print(self.name + " is focusing. Their attack and speed increased!")
        self.atk = (int)(self.atk * 1.4)
        self.spd = (int)(self.spd * 1.4)
        HPChange = (int)(0.15 * self.maxHp)
        if (HPChange > self.hp):
            HPChange = self.hp
        print(self.name + " lost " + str(HPChange) + " HP!")
        self.hp = self.hp - HPChange

    def heal(self):
        print(self.name + " healed themselves by " + str(self.maxHp - self.hp) + " health.")
        self.hp = self.maxHp
        print(self.name + "\'s defense and speed decreased!")
        self.df = (int)(self.df * 0.8)
        self.spd = (int)(self.spd * 0.8)

    def awardXP(self, XP):
        for i in range(0, XP):
            self.XP = self.XP + 1
            if (self.XP == pow(self.level + 1, 2)):
                self.XP = 0
                self.level = self.level + 1
                print("You leveled up to Level " + str(self.level) + "!")
                self.updateStats(self.level - 1)
        print("You need: " + str((int)(pow(self.level + 1, 2) - self.XP)) + " XP to level up to Level " + str(self.level + 1))
    
    def simulate(self, player, opponent, lastAttack):
        p1 = SimuCharacter(player.name, player.level, player.hp, player.atk, player.df, player.spd)
        o1 = SimuCharacter(opponent.name, opponent.level, opponent.hp, opponent.atk, opponent.df, opponent.spd)
        index = 0

        hpDiff1 = 0
        if (lastAttack == "punch" or lastAttack == "block" or lastAttack == "void"):
            p1.punch(o1)
            hpDiff1 = o1.maxHp - o1.hp
        else:
            p1.kick(o1)
            hpDiff1 = o1.maxHp - o1.hp
        oInit = o1.hp
        o1.hp = o1.maxHp

        p1 = SimuCharacter(player.name, player.level, player.hp, player.atk, player.df, player.spd)
        
        punchDiff = 0
        o1.punch(p1)
        punchDiff = p1.maxHp - p1.hp
        p1.hp = p1.maxHp
        scorePunch = 0
        if (punchDiff >= p1.maxHp):
            scorePunch = 10000
        else:
            scorePunch = punchDiff

        o1 = SimuCharacter(opponent.name, opponent.level, opponent.hp, opponent.atk, opponent.df, opponent.spd)
        
        kickDiff = 0
        o1.kick(p1)
        kickDiff = p1.maxHp - p1.hp
        p1.hp = p1.maxHp
        scoreKick = 0
        if (kickDiff >= p1.maxHp):
            scoreKick = 10000
        else:
            scoreKick = kickDiff
        
        scoreHeal = 0
        o2 = SimuCharacter(opponent.name, opponent.level, opponent.maxHp, opponent.atk, opponent.df, opponent.spd)
        o2.hp = o1.hp
        def1 = o2.df
        spd1 = o2.spd
        o2.heal()
        def2 = o2.df
        spd2 = o2.spd
        defChange = def1 - def2
        spdChange = spd1 - spd2

        if (lastAttack == "punch" or lastAttack == "block" or lastAttack == "void"):
            p1.punch(o2)
        else:
            p1.kick(o2)

        if (o2.hp > 0 and oInit == 0):
            scoreHeal = 1000
        elif (o2.hp > 0):
            scoreHeal = o2.hp - o1.hp - defChange - spdChange
        else:
            scoreHeal = -1000
        
        scoreBlock = 0
        o2 = SimuCharacter(opponent.name, opponent.level, opponent.maxHp, opponent.atk, opponent.df, opponent.spd)
        o2.hp = o1.hp
        def1 = o2.df
        o2.block()
        def2 = o2.df
        defChange = def2 - def1

        if (lastAttack == "punch" or lastAttack == "block" or lastAttack == "void"):
            p1.punch(o2)
        else:
            p1.kick(o2)

        if (o2.hp > 0 and oInit == 0):
            scoreBlock = 1000
        elif (o2.hp > 0):
            scoreBlock = o2.hp - o1.hp - 1 + defChange
        else:
            scoreBlock = -1000

        o1 = SimuCharacter(opponent.name, opponent.level, opponent.hp, opponent.atk, opponent.df, opponent.spd)
        
        scoreFocus = 0
        atk1 = o1.atk
        spd1 = o1.spd
        o1.focus()
        atk2 = o1.atk
        spd2 = o1.spd
        diffAtk = atk2 - atk1
        diffSpd = spd2 - spd1
        scoreFocus = diffSpd + diffAtk - 4

        scores = [scorePunch, scoreKick, scoreHeal, scoreBlock, scoreFocus]
        score = max(scores)
        index = scores.index(score)

        return index


class SimuCharacter(Character):
    def __init__(self, name, level, h, a, d, s):
        self.name = name
        self.level = level
        self.hp = h
        self.maxHp = h
        self.atk = a
        self.baseAtk = a
        self.df = d
        self.baseDef = d
        self.spd = s
        self.baseSpd = s     

    def damage(self, opponent, r):
        num = (float)(pow(self.atk, 1.5))
        den = (float)(opponent.df)
        modifier = (float)(self.level / opponent.level)
        change = (int)(num / den * modifier * r)
        if (change < 1):
            change = 1
        if (change > opponent.hp):
            change = opponent.hp
        opponent.hp = opponent.hp - change
        return change

    def punch(self, opponent):
        chance = random.uniform(0, 1)
        if (chance < 0.95):
            change = self.damage(opponent, (self.level / 10.0) * random.uniform(0.85, 1) + 1)

    def kick(self, opponent):
        chance = random.uniform(0, 1)
        if (chance < 0.8):
            change = self.damage(opponent, (self.level / 10.0) * random.uniform(0.85, 1) + 1.6)
            self.df = (int)(self.df * 0.5)
        
    def block(self):
        self.df = (int)(self.df * 1.4)
        HPChange = (int)(0.05 * self.maxHp)
        if (HPChange > self.hp):
            HPChange = self.hp
        self.hp = self.hp - HPChange
    
    def focus(self):
        self.atk = (int)(self.atk * 1.4)
        self.spd = (int)(self.spd * 1.4)
        HPChange = (int)(0.15 * self.maxHp)
        if (HPChange > self.hp):
            HPChange = self.hp
        self.hp = self.hp - HPChange

    def heal(self):
        self.hp = self.maxHp
        self.df = (int)(self.df * 0.8)
        self.spd = (int)(self.spd * 0.8)   

        
def turnHP(players):
    for player in players:
        print(player.name + "\'s HP: " + str(player.hp))

def opponentMove(player, opponent, lastAttack):
    oppMove = opponent.simulate(player, opponent, lastAttack)
    if oppMove == 0:
        opponent.punch(player)
    elif oppMove == 1:
        opponent.kick(player)
    elif oppMove == 2:
        opponent.block()
    elif oppMove == 3:
        opponent.focus()
    else:
        opponent.heal()

def yourMove(player, opponent):
    move = input("Select an attack: Punch, Kick, Block, Focus, or Heal: ")
    move = move.lower()
    if (move == "punch"):
        player.punch(opponent)
        lastAttack = "punch"
    elif (move == "kick"):
        player.kick(opponent)
        lastAttack = "kick"
    elif (move == "block"):
        player.block()
        lastAttack = "block"
    elif (move == "focus"):
        player.focus()
        lastAttack = "focus"
    elif (move == "heal"):
        player.heal()
        lastAttack = "heal"
    else:
        print("No Valid Move Selected!")
        lastAttack = "void"
    return lastAttack

def checkWin(player, opponent):
    if (player.hp <= 0 or opponent.hp <= 0):
        return True
    else:
        return False

def game(players, player, i):
    opponent = Character("Opponent", i)
    players.append(opponent)
    opponent.reset()
    turn = 1
    turnHP(players)
    print()
    lastAttack = "void"
    while (player.hp > 0 and opponent.hp > 0):
        time.sleep(0.5)
        print("Turn " + str(turn))
        if (player.spd >= opponent.spd):
            lastAttack = yourMove(player, opponent)
            turnHP(players)
            print()
            if checkWin(player, opponent):
                break
            time.sleep(0.5)
            opponentMove(player, opponent, lastAttack)
            turnHP(players)
        else:
            opponentMove(player, opponent, lastAttack)
            turnHP(players)
            print()
            if checkWin(player, opponent):
                break
            time.sleep(0.5)
            lastAttack = yourMove(player, opponent)
            turnHP(players)
        turn = turn + 1
        print()
    if (opponent.hp <= 0):
        print("You Won!")
        time.sleep(0.5)
        getXP = 6 * (opponent.level + (opponent.level - player.level)) +  (int)(5 * random.uniform(0, 1))
        if (getXP < 1):
            getXP = 1
        print("Awarding " + str(getXP) + " XP.")
        player.awardXP(getXP)
        players.remove(opponent)
        return True
    else:
        print("You Lost!")
        return False

print("Welcome to Gauntlet!")
time.sleep(0.5)
name = input("What is your name?: ")
player = Character(name, 1)
players = [player]
iMax = 0
for i in range(1, 11):
    print()
    print("Opponent # " + (str)(i) + ":")
    time.sleep(0.5)
    player.reset()
    status = game(players, player, i)
    iMax = i
    if(not status):
        break

time.sleep(0.5)
if(iMax == 10):
    print("You beat Gauntlet! Congrats!")
else:
    print("You reached opponent level: " + (str)(iMax))