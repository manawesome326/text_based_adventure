#!/bin/python3
# encoding=utf-8

def true_input():
	return input("> ")


allitems = []
class Aisle:
	global allitems
	def __init__(self, opening, look, next_place): #opening prints on arrival, look prints on 'look', next_place is where ur goin next
		self.opening = opening
		self.look = look
		self.next_place = next_place
	@property
	def items(self):
		global allitems
		return [x for x in allitems if (x.location == self or x.location == everywhere)] 
class Item:
	def __init__(self, name, description, location, verbs = {}, scenery = False): #name is the name, description prints on x, scenery is whether or not it's listed and takable, verbs are the verbs you can use, location is where it is, and synonyms are other words for it
		global allitems
		self.name = name
		self.description = description
		self.scenery = scenery
		self.location = location
		allitems += [self]
		self.verbs = {**{take:"Taken.", drop:"Dropped."}, **verbs} #if these aren't defined, just use the defualts	

#define our verbs
def violence(noun = None):
	print2("Violence is not the answer to this one.")
def take(noun):
	global hammerspace
	global inventory
	if noun in inventory:
		print2("You're already carrying that.")
	elif noun.verbs[take]:
		print2(noun.verbs[take])
		inventory.append(noun)
		noun.location = hammerspace 
	else:
		print2("That's hardly portable.")

def examine(noun):
	print2(noun.description)

def drop(noun):
	global current_location
	global inventory
	if noun not in inventory:
		print2("You can't drop something you're not carrying!")
	elif noun.verbs[drop]:
		print2(noun.verbs[drop])
		inventory.remove(noun)
		noun.location = current_location
	else:
		print2("You'd rather keep that, for the time being")

def inventory():
	global inventory
	print2("You're holding:")
	for i in [x.name for x in inventory]:
			print2(i, 0.15)

def print_help():
	print2("This section plays like a normal text adventure game. Except, because I'm lazy, every command MUST be written as VERB NOUN, or just VERB if no noun is relevant. For a list of most of the commands, do 'list'")

def print_commands():
	print2("All the following commands are not case sensitive. Those that require a noun have NOUN written after them:", 1)
	print2("LOOK (or L)", 0.1)
	print2("TAKE NOUN", 0.1)
	print2("INVENTORY (or I)", 0.1)
	print2("DROP NOUN", 0.1)
	print2("EXAMINE NOUN (or X)", 0.1)
	print2("WEST (or W, or SOUTH, or S, or NORTH, or N, or EAST, or E)", 0.1)
	print2("EAT NOUN", 0.1)
	print2("SIT", 0.1)
	print2("DESTROY NOUN(or BREAK or SMASH or ATTACK or LITERALLY ANY OTHER VIOLENT ACTION)", 0.1)
	print2("WAIT (or Z)", 0.1)

def look_around():
	global current_location
	print2(current_location.look,2)
	items_here = [x for x in allitems if x.location == current_location and not x.scenery]
	if len(items_here) == 1:
		print2("There's one thing here which stands out to you: " + items_here[0].name)
	elif len(items_here) > 1:
		print2("A few items stand out to you here:")
		for i in [x.name for x in items_here]:
			print2(i, 0.15)
score = 0
flagged = False

def flag():
	global flagged, score
	if current_location == trashed_aisle and not flagged:
		score += 50
		print2("You hear a strange echo from far away...", 2)
		print2('"' + getpass.getuser() + " scouted an aisle for 50 points.\"", 3)
		print2("Weird, huh.")
	elif current_location != trashed_aisle:
		print2("You can't do that here.")
	else:
		print2("You've already flagged this area")

def eat(noun):
	global inventory
	if noun == pretzels:
		print2("Ah, that really hit the spot.")
		inventory.remove(pretzels)
		pretzels.location = "hell"
	else:
		print2("That's plainly inedible.")

def sit():
	global current_location
	if current_location == furniture_aisle:
		print2("You sit down on one of the many chairs here, for a moment. As you expected, it's very comfortable.")
	elif len([x for x in allitems if x.location == current_location and x.name == "A chair"]) > 0:
		print2("You sit down on the chair, for a moment. It's very comfortable.")
	else:
		print2("You sit on the floor, for a moment. Not very comfortable.")

def wait():
	print2("You would do that, except you realise that it's a huge waste of time.")

def try_the_toy(noun): #NOT A EUPHENISM
	if noun != bop_it:
		print2("I'm not sure how to 'try' that")
	else:
		print2("It's dead out of batteries. Oh well.")


def north():
	move("n")
def east():
	move("e")
def south():
	move("s")
def west():
	move("w")

last_direction = "wenis"
#almost a verb
def move(direction):
	global last_direction
	global current_location
	opposites = {"n":"s", "e":"w", "s":"n", "w":"e", "wenis":"hell no"}
	print2("You wander the shelves...", 3)
	if opposites[last_direction] == direction:
		print2("The reality of fabric seems to warp around you... looks like you can't get back to an area you've been to before.", 3)
	current_location = current_location.next_place
	print2(current_location.opening)
	last_direction = direction


#not a verb
def be_sensible(noun):
	if noun[:2] == "a ":
		noun = noun[2:] #chop off "A ..."
	if noun[:4] == "the ":
		noun = noun[4:] #chop off "the ..."
	try:
		actual_noun = synonyms[noun]
	except KeyError:
		return(False)
	if actual_noun.location == current_location or actual_noun.location == everywhere or actual_noun.location == hammerspace:
		return(actual_noun)
	else:
		return(False)


spooked = False #that's for the final aisle
everywhere = "everywhere, at all."
hammerspace = "your own inventory"
#medicine_aisle = Aisle("You're now in an aisle of ")
furniture_aisle = Aisle("You're now in an aisle full of furniture. Mostly just chairs.", "You see furniture of all types, but mostly chairs. They look very comfortable...", None)
trashed_aisle = Aisle("You're now in an aisle full of junk food, and an aisle full of novelty license plates. That is, the two bisect another at odd angles that shouldn't be physically possible. You feel like you're supposed to do something...", "You see two shevles interecting in front of you. One of novelty license plates, one of junk food.", furniture_aisle)
childs_toys_aisle = Aisle("You seem to be in an aisle full of children's toys. No matter where you're going, you can't imagine them being useful.", "You see children's toys on the shelves all around you.", trashed_aisle)
#reverse order
shelves = Item("The shelves", "Just some shelves", location = everywhere, scenery = True, verbs = {take:False})
the_floor = Item("The floor", "A perfectly ordinary tiled floor. Nothing strange about it.", location = everywhere, scenery = True, verbs = {take:False})
chair = Item("A chair", "A completely normal sized ordinary chair. It's looks pretty heavy, and doesn't fold up.", location = furniture_aisle)
cloak = Item("A strange white cloak (worn)", "A strange white cloak, which reminds you vaguely of the one Death wore, except Death's was black instead. It's very comfortable.", hammerspace, {drop:False})
bop_it = Item("A bop-it toy", "It's a bop-it. The front of the box says \"TRY ME!\".", location = childs_toys_aisle)
pretzels = Item("Some pretzels", "They're plain pretzels. Not incredibly exciting, but they're edible, unlike most of the food you've seen here.", location = trashed_aisle)
license_plate = Item("A novelty license plate reading 'ISO 8601'", "Something about this license plate tells you that it's the best date and time format possible.", location = trashed_aisle)
#FONCE
def new_dictionary(dictionary):
	temp_dictionary = {}
	for synonyms, verb in dictionary.items():
		for synonym in synonyms:
			temp_dictionary[synonym] = verb
	return temp_dictionary

synonyms = new_dictionary({("take", "grab", "purloin",):take,\
 ("i", "inventory",):inventory, \
 ("hit", "attack", "punch", "smash", "kill", "destroy", "dance", "fireball", "break",):violence, \
 ("examine", "x",):examine, \
 ("drop","remove",):drop, \
 ("help",):print_help, \
 ("list",):print_commands, \
 ("look", "l",):look_around, \
 ("w","west",):west, \
 ("n", "north"):north, \
 ("e", "east"):east, \
 ("s", "south"):south, \
 ("try","use",):try_the_toy, \
 ("shelves","walls","aisle"):shelves, \
 ("flag",):flag, \
 ("sit",):sit, \
 ("wait", "z"):wait, \
 ("eat",):eat, \
 ("floor",):the_floor, \
 ("chair", "furniture"):chair, \
 ("pretzels", "junk food","food"):pretzels, \
 ("license plate", "plate", "novelty license plate", "ISO 8601","license plates", "novelty license plates", "plates"):license_plate, \
 ("cloak", "strange white cloak", "white cloak", "jumper", "uniform",):cloak, \
 ("children's toys", "children's toy", "child's toy", "child's toys", "bop-it", "toy"):bop_it, \
 })


inventory = [cloak]
print2("You wake up.", 2)
print2("In a department store.", 2)
print2("Odd. When you black out, you usually seem to wake up in an alley somewhere instead.", 2)
print2("<type 'help' if you need help with this bit>", 2)
print2(childs_toys_aisle.opening)
current_location = childs_toys_aisle

while True:
	users_input = true_input().lower()
	if users_input == "take chair":
		print2("Thanks!")
	words = users_input.split(" ", 1)
	this_verb = words[0]
	try:
		this_verb_function = synonyms[this_verb]
	except KeyError:
		print2("I'm not sure how to '" + this_verb +"'")
	else:
		if type(this_verb_function) == Item:
			print2("That's a noun, not a verb!")
		else:
			if len(words) == 2:
				this_noun = words[1]
				if be_sensible(this_noun):
					this_noun_item = be_sensible(this_noun) #don't mind the naming
					try:
						this_verb_function(this_noun_item)
					except TypeError:
						print2("You can't just '" + this_verb + "' something.")
				else:
					print2("You can't see a '" + this_noun + "' here")
			else:
				try:
					this_verb_function()
				except TypeError:
					print2("You can't just '"+this_verb+"' nothing.")

		




