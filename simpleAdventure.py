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
	"inventory" : [],
	"level" : 1,
	"xp" : 0,
	"xpForNextLevel" : 100,
	"exploredTiles" : 1
}

# Initialize gamemap and tile types.
gameMap = {}
tileType = ["Town","Plains","Hills","Mountains","Forest","Swamp","Badlands","Dungeon","Desert","Tundra","Prairie",
			"Lake","City"]
items_weapons = ["Knife","Staff","Club","Sword","Spear","Axe","Flail","Warhammer","Dagger","Morningstar",
				 "Brass Knuckles","Halberd","Bow","Crossbow","Dart","Javelin"]
items_armor = ["Underwear","Shoddy Clothes","Normal Clothes","Sturdy Clothes","Leather Armor","Studded Leather Armor",
			   "Ring Mail Armor","Chain Mail Armor","Steel Plate Armor","Enchanted Clothes","Enchanted Leather Armor",
			   "Enchanted Ring Mail Armor","Enchanted Plate Mail Armor","Enchanted Chain Mail Armor"]
items_treasure = ["Silver Ring","Gold Ring","Silver Pendant","Gold Pendant","Silver Brooch","Gold Brooch",
				  "Gem Studded Silver Ring","Gem Studded Gold Ring","Gem Studded Silver Pendant",
				  "Gem Studded Gold Pendant","Gold Scepter","Gold Tiara","Silver Tiara","Gold Crown",
				  "Enchanted Gold Ring","Enchanted Gold Pendant"]
items_misc = ["Piece of Amber","Hammer","Warm Blanket","Shoes","Journal","Glass Beads","30' Rope","Waterskin",
			  "Whetstone","Firestarter","Stone Mortar","Sewing Kit","Chisel","Torch","Fishing Rod","Clay Jar"]
world_x_size = 16
world_y_size = 16
home_coords = str(round(world_y_size/2))+"_"+str(round(world_x_size/2))
player["locationID"] = home_coords
player["locationX"] = round(world_x_size/2)
player["locationY"] = round(world_y_size/2)

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
	global gameMap
	global home_coords
	thisRow = 0
	thisCol = 0
	thisTile = "0_0"
	for r in range(0,rows):
		for c in range(0,columns):
			thisTile = str(thisRow)+"_"+str(thisCol)
			gameMap[thisTile] = makeTile(thisTile,thisRow,thisCol)
			if gameMap[thisTile]["mapID"] == home_coords:
				gameMap[thisTile]["type"] = "Home"
				gameMap[thisTile]["explored"] = True
			thisCol += 1
		thisRow += 1
		thisCol = 0
	
# generate a player.		
def makePlayer():
	player["name"] = input("Give your character a name: ")
	player["inventory"].append(random.choice(items_misc))
	player["inventory"].append(random.choice(items_weapons))
	print ("\nYour character is named {0}. Your health is full ({1} hp), and you currently hold {2} gold pieces. You inventory contains a couple of items.".format(player["name"], player["health"],player["gold"]))
	print ("\t%s is a 1st level character, who needs %s xp to gain a level. Doing so will lead to more health. You get xp from exploring and overcoming encounters." % (player["name"],player["xpForNextLevel"]))
	print ("\tYour adventure begins in your home town of Slumberville. Time to go explore the lands...")

def hitEnter():
	input("\nHit Enter to continue.")
	
# Load tile description
def description():
	print("\nCurrent location: " + gameMap[player["locationID"]]["type"])
	isExplored = "explored"
	if gameMap[player["locationID"]]["explored"] == False:
		isExplored = "unexplored"
	print ("(X: " + str(player["locationX"]) + ", Y: " + str(player["locationY"]) + ") This area is " + isExplored + ". TILE# " + str(player["locationID"]))

# move around the map.
def movePlayer(direction):
	global gameMap
	if direction == "n":
		if player["locationY"] + 1 <= world_y_size-1:
			player["locationY"] += 1
		else:
			player["locationY"] = 0
	elif direction == "s":
		if player["locationY"] - 1 >= 0:
			player["locationY"] -= 1
		else:
			player["locationY"] = world_y_size-1
	elif direction == "e":
		if player["locationX"] + 1 < world_x_size:
			player["locationX"] += 1
		else:
			player["locationX"] = 0
	else: # direction == "w"
		if player["locationX"] - 1 >= 0:
			player["locationX"] -= 1
		else:
			player["locationX"] = world_x_size-1

	tileID = str(player["locationY"])+"_"+str(player["locationX"])
	player["locationID"] = tileID #gameMap[tileID]["mapID"]
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
	maxHeal = player["maxHealth"]-player["health"]
	if (maxHeal > player["gold"]*3):
		maxHeal = player["gold"]/3
	healcost = maxHeal*3
	player["gold"] -= healcost
	print ("You have healed %s hit points for %s gold (%s gold remaining)." % (maxHeal, healcost, player["gold"]))
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
	global home_coords
	heal_enabled = False
	print ("\nAvailable actions:")
	actionString = ""
	if gameMap[player["locationID"]]["explored"] == False:
		actionString += "\nx = explore the area."
	if player["locationID"] == home_coords or gameMap[player["locationID"]]["type"] == "City":
		if player["health"] < player["maxHealth"]:
			actionString += "\nr = rest and recover."
			heal_enabled = True
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
			sumNum = random.choice([0,0,1,2,2])
			if gameMap[player["locationID"]]["type"] == "Dungeon" or gameMap[player["locationID"]]["type"] == "Badlands":
				sumNum = random.choice([0,1,2,2,2])
			if gameMap[player["locationID"]]["type"] == "Town" or gameMap[player["locationID"]]["type"] == "City":
				sumNum = random.choice([0,0,0,1,2])
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
	elif choice == "r" and heal_enabled == True:
		healPC()
	# display character sheet
	elif choice == "c":
		print (player["name"] + " / Level: " + str(player["level"]) + " XP: " + str(player["xp"]) + " (" + str(player["xpForNextLevel"]) + " needed)")
		print ("Hit points: " + str(player["health"]) + " (max: " + str(player["maxHealth"]) + ")")
	
	else:
		print ("I don't know that command.")
# This is where the game action happens...

def main():
	# Generate the world...
	global world_x_size
	global world_y_size
	global home_coords
	makeMap(world_x_size,world_y_size)

	# Initialize player
	makePlayer()
	still_alive = True

	description()
	hitEnter()

	# game loop
	while still_alive:
		getAction()
		if player["exploredTiles"] == (world_x_size*world_y_size): #map is fully explored, a new one is generated...
			print ("You have explored the entire map!\nA friendly wizard teleports you to a new one...")
			#this basically resets the game, except for the player who is only moved to the new "home" tile.
			hitEnter()
			player["locationID"] = home_coords
			player["locationX"] = round(world_x_size/2)
			player["locationY"] = round(world_y_size/2)
			gamemap = {}
			makeMap(world_x_size, world_y_size)
			player["exploredTiles"] = 1
			description()
		if player["health"] <= 0: # the player died
			print ("\nYou have died.")
			still_alive = False
			#the game ends.

if __name__ == "__main__":
	main()