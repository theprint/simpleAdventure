# simpleAdventure v. 0.2b
# Officially lives here -- https://github.com/theprint/simpleAdventure
# simpleAdventure is really just an exercise in Python, written in 2 days after studying the language for about 2 weeks. The game is a potentially endless text based adventure that allows a character to level up and includes an element of exploration.
# If I had had more time, I would have included a storyline and an ongoing quest to collect items (there is already an inventory included with the player object, I just didn't get around to using it.
# Feel free to add to this code, or modify it in any way you see fit. Thanks, Rasmus - twitter.com/theprint / rasmusrasmussen.com
import random
import math

# This is the player data
player = {
	"name" : "Jack",
	"health" : 10,
	"maxHealth" : 10,
	"gold" : 100,
	"inventory" : ["shoes", "blanket"],
	"level" : 1,
	"xp" : 0,
	"xpForNextLevel" : 100,
	"locationX" : 2,
	"locationY" : 2,
	"locationID" : 13,
	"exploredTiles" : 1
}

# Initialize gamemap and tile types.
gameMap = {}
tileType = ["Town","Plains","Hills","Mountains","Forest","Swamp","Badlands","Dungeon"]

# Generates a tile on the game map.
def makeTile(id,x,y):
	tile = {
		"mapID" : id,
		"x" : x,
		"y" : y,
		"type" : random.choice(tileType),
		"explored" : False
	}
	return tile	

# Generates the game map itself.
def makeMap(rows,columns):
	thisRow = 0
	thisCol = 0
	thisTile = 1
	for r in range(0,rows):
		for c in range(0,columns):
			gameMap[thisTile] = makeTile(thisTile,thisRow,thisCol)
			if gameMap[thisTile]["mapID"] == 13:
				gameMap[thisTile]["type"] = "Home"
				gameMap[thisTile]["explored"] = True
			thisTile += 1
			thisCol += 1
		thisRow += 1
		thisCol = 0
	
# generate a player.		
def makePlayer():
	player["name"] = input("Give your character a name: ")
	print ("\nYour character is named {0}. Your health is full ({1} hp), and you currently hold {2} gold pieces. You inventory is empty.".format(player["name"], player["health"],player["gold"]))
	print ("\t%s is a 1st level character, who needs %s xp to gain a level. Doing so will lead to more health. You get xp from exploring and overcoming encounters." % (player["name"],player["xpForNextLevel"]))
	print ("\tYour adventure begins in your home town of Slumberville. Time to go explore the lands...")

def hitEnter():
	input("\nHit Enter to continue.")
	
# Load tile description
def description():
	isExplored = "explored"
	if gameMap[player["locationID"]]["explored"] == False:
		isExplored = "unexplored"
	print ("\nCurrent location: " + gameMap[player["locationID"]]["type"])
	print ("(X: " + str(player["locationX"]) + ", Y: " + str(player["locationY"]) + ") This area is " + isExplored + ". TILE# " + str(player["locationID"]))

# move around the map.
def movePlayer(direction):
	if direction == "n":
		if player["locationY"] + 1 <= 4:
			player["locationY"] += 1
			player["locationID"] += 5
		else:
			player["locationY"] = 0
			player["locationID"] = (player["locationID"]+5)-25
	elif direction == "s":
		if player["locationY"] - 1 >= 0:
			player["locationY"] -= 1
			player["locationID"] -=5
		else:
			player["locationY"] = 4
			player["locationID"] = (player["locationID"]-5)+25	
	elif direction == "e":
		if player["locationX"] + 1 <= 4:
			player["locationX"] += 1
		else:
			player["locationX"] = 0
		if (player["locationID"] + 1) <= (player["locationY"]+1)*5:
			player["locationID"] += 1
		else:
			player["locationID"] -= 4
	else: # direction == "w"
		if player["locationX"] - 1 >= 0:
			player["locationX"] -= 1
		else:
			player["locationX"] = 4
		if player["locationID"] - 1 > 25-(player["locationY"]+1)*5:
			player["locationID"] -= 1
		else:
			player["locationID"] += 4
	description()
	
# adds xp and levels up the player as necessary.
def awardXP(amount):
	player["xp"] += amount
	print ("\n%s earned %s experience points." % (player["name"],amount))
	if player["xp"] >= player["xpForNextLevel"]:
		player["level"] += 1
		player["maxHealth"] += 5
		player["health"] = player["maxHealth"]
		player["xpForNextLevel"] += int(math.floor(player["xpForNextLevel"]*1.55))
		print ("LEVEL UP -- %s is now level %s!" % (player["name"], player["level"]))
		
def healPC():
	print ("You have healed %s hit points." % (player["maxHealth"]-player["health"]))
	player["health"] = player["maxHealth"]
	
def doFight():
	monsterType = ["Goblin","Orc","Bandit","Zombie","Skeleton","Slime","Kobold","Giant Bat","Giant Beetle","Wolf","Bear"]
	myRace = random.choice(monsterType)
	theMonster = {
		"race" : myRace,
		"hit points" : random.randrange(2,9),
		"treasure" : random.randrange(0,20)
	}
	print ("\n1 %s appears before you." % theMonster["race"])
	
def getAction():
	print ("\nAvailable actions:")
	actionString = ""
	if gameMap[player["locationID"]]["explored"] == False:
		actionString += "\nx = explore the area."
	if player["locationID"] == 13 and player["health"] < player["maxHealth"]:
		actionString += "\nr = rest and recover."
	print (actionString )
	print ("n = north / s = south / w = go west / e = go east.")
	print ("i = view inventory and gold.")
	print ("c = character sheet.")
	# get a command from the player:
	choice = input("Pick an action and hit Enter: ").lower()
	
	#out put result of command...
	print ("\n")
	
	#display inventory
	if choice == "i":
		print ("You are currently carrying: " + "%s" % ", ".join(map(str, player["inventory"])))
		print ("Gold: " + str(player["gold"]))
	# Moving along
	elif choice == "n" or choice == "e" or choice == "w" or choice == "s":
		movePlayer(choice)
	# Explore the area
	elif choice == "x":
		if gameMap[player["locationID"]]["explored"] == False:
			player["exploredTiles"] += 1
			sumNum = random.randrange(1,3)
			if sumNum == 1:
				print ("\nYou find gold!")
				gold = random.randrange(10,60)
				print (str(gold) + " added to your holdings...")
				player["gold"] += gold
				awardXP(int(math.floor(gold/12)))
			elif sumNum == 2:
				print ("Oh no! Monsters!")
				damage = random.randrange(1,4)
				print ("You take " + str(damage) + " points of damage.")
				player["health"] -= damage
				if player["health"] > 0:
					awardXP(damage*5)
			else:
				print ("You look around, but find nothing of interest...")
				awardXP(1)
			
			gameMap[player["locationID"]]["explored"] = True
		else:
			print ("There is nothing to explore here.")
	# rest and recover
	elif choice == "r" and player["locationID"] == 13 and player["health"] < player["maxHealth"]:
		healPC()
	# display character sheet
	elif choice == "c":
		print (player["name"] + " / Level: " + str(player["level"]) + " XP: " + str(player["xp"]) + " (" + str(player["xpForNextLevel"]) + " needed)")
		print ("Hit points: " + str(player["health"]) + " (max: " + str(player["maxHealth"]) + ")")
	
	else:
		print ("I don't know that command.")
# This is where the game action happens...

# Generate the world...
makeMap(5,5)

# Initialize player
makePlayer()
still_alive = True

description()
hitEnter()

# game loop
while still_alive:
	getAction()
	if player["exploredTiles"] == 25: #map is fully explored, a new one is generated...
		print ("You have explored the entire map!\nA friendly wizard teleports you to a new one...")
		#this basically resets the game, except for the player who is only moved to the new "home" tile.
		hitEnter()
		player["locationID"] = 13
		player["locationX"] = 2
		player["locationY"] = 2
		gamemap = {}
		makeMap(5,5)
		player["exploredTiles"] = 1
		description()
	if player["health"] <= 0: # the player died
		print ("\nYou have died.")
		still_alive = False
		#the game ends.