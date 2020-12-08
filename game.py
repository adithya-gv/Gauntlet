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

def turnHP(players):
    for player in players:
        print(player.name + "\'s HP: " + str(player.hp))

def opponentMove(player, opponent):
    oppMove = random.randint(0, 4)
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
    elif (move == "kick"):
        player.kick(opponent)
    elif (move == "block"):
        player.block()
    elif (move == "focus"):
        player.focus()
    elif (move == "heal"):
        player.heal()
    else:
        print("No Valid Move Selected!")

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
    while (player.hp > 0 and opponent.hp > 0):
        time.sleep(0.5)
        print("Turn " + str(turn))
        if (player.spd >= opponent.spd):
            yourMove(player, opponent)
            turnHP(players)
            print()
            if checkWin(player, opponent):
                break
            time.sleep(0.5)
            opponentMove(player, opponent)
            turnHP(players)
        else:
            opponentMove(player, opponent)
            turnHP(players)
            print()
            if checkWin(player, opponent):
                break
            time.sleep(0.5)
            yourMove(player, opponent)
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