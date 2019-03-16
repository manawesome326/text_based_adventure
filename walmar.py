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
		self.verbs = {**{take:"Taken.", drop:"Dropped.", "read":False, eat:False}, **verbs} #if these aren't defined, just use the defualts	

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
	global books_read
	poisonicine_long_desc = ["POISONICINE -"," May cause irritable skin,"," slight bloating,"," erratic and incredibly violent behaviour,"," elbow discomfort,"," and irreverisible sudden death."," Do not ingest."," In fact, don't do anything with it."," It's incredibly dangerous and we have no idea why it's sold as a packaged product."," Store in a cool, dry environment."]
	if noun == poisonicine:
		print2(poisonicine.description, 1.3)
		for line in poisonicine_long_desc:
			print2(line, 1.2)
	else:	
		print2(noun.description)
	if noun.verbs["read"]:
		books_read.append(noun)

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
def jump():
	print2("You jump on the spot.")

def print_help():
	print2("This section plays like a normal text adventure game. Except, because I'm lazy, every command MUST be written as 'VERB NOUN', or just 'VERB' if no noun is relevant. Every verb is one word, but nouns can be longer. For a list of most of the verbs, do 'list'.")

def print_commands():
	print2("All the following commands are not case sensitive. Those that require a noun have NOUN written after them:", 1)
	print2("LOOK (or L, you should do this one first!)", 0.1)
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
		if current_location != book_aisle:
			print2("A few items stand out to you here:")
		for i in [x.name for x in items_here]:
			print2(i, 0.15)
		if current_location == book_aisle:
			print2("Please just refer too books by their two word title, I'm going to get confused otherwise.", 1.2)
score = 0
flagged = False

def flag():
	global flagged, score
	if current_location == trashed_aisle and not flagged:
		score += 50
		print2("You hear a strange echo from far away...", 2)
		print2('"' + getpass.getuser() + " scouted an aisle for 50 points.\"", 3)
		print2("Weird, huh.")
		flagged = True
	elif current_location != trashed_aisle:
		print2("You can't do that here.")
	else:
		print2("You've already flagged this area.")

def eat(noun):
	global inventory
	global turns
	global score
	if noun == pretzels:
		print2("Ah, that really hit the spot.",3)
		try:
			inventory.remove(pretzels)
		except ValueError:
			pass
		pretzels.location = "hell"
		print2("Wait, did you just eat a bunch of loose pretzels?",2)
		print2("Eww.")
	elif noun == homeopathic_medicine:
		if homeopathic_medicine.verbs[eat]:
			print2("In one fell swoop, you swallow all of the herbal pills in the bottle", 2)
			print2("They don't taste very good.", 2)
			print2("Oh well.")
			homeopathic_medicine.verbs[eat] = False
			homeopathic_medicine.name = homeopathic_medicine.name + " (empty)"
			homeopathic_medicine.description = homeopathic_medicine.description + " It's empty."
		else:
			print2("it's empty. Aww.")
	elif noun == poisonicine:
		if poisonicine.verbs[eat]:
			print2("Why would you want to do that?", 3)
			print2(" *** you have died! ***",3)
			print2("You survived " + str(turns) +" turns, with a score of " + str(score)+". Would you like to RESTART, QUIT, or UNDO your last move?", 4)
			input(">> ")
			print2("I'm just kidding, you can't die in purgatory.", 2)
			print2("Your elbow does hurt though.")
			poisonicine.verbs[eat] = False
			poisonicine.description = "It's empty. " + poisonicine.description[35:]
			poisonicine.name = poisonicine.name + " (empty)"
		else:
			print2("It's empty. Luckily.")
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
	global turns
	print2("You would do that, except you realise that it's a huge waste of time.")
	turns -= 1

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
	global spooked
	global spooked_stage
	global spooked_time
	opposites = {"n":"s", "e":"w", "s":"n", "w":"e", "wenis":"hell no"}
	print2("You wander the shelves...", 2)
	if opposites[last_direction] == direction:
		print2("The reality of fabric seems to warp around you... looks like you can't get back to an area you've been to before.", 3)
	current_location = current_location.next_place
	if current_location == None:
		print2("The strange geometry of this place means you bump straight into the person making the footsteps! They appear to be a store clerk, though not just because their dark, hooded cloak has an employee badge on it. No, it's because the first thing they say to you is...", 3)
		spooked_stage = 6
		return(True)
	print2(current_location.opening, 2)
	last_direction = direction
	if current_location == book_aisle:
		spooked = True
		spooked_stage = 0
		spooked_time = time.time()
		print2(spooky_messages[spooked_stage])


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
	if str(type(actual_noun)) == "<class 'function'>":
		return(False)
	elif (actual_noun.location == current_location) or (actual_noun.location == everywhere) or (actual_noun.location == hammerspace):
		return(actual_noun)
	else:
		return(False)


spooked = False #that's for the final aisle
spooked_stage = -1
books_read = [] #also for final aisle
spooked_time = "E"
spooky_messages = ["As you enter this aisle, you seem to hear footsteps from far away...", "The footsteps seem to be getting louder.", "You wonder if you're going to have to pay for all the stuff you're carrying.", "Even though you're not sure that makes sense based off the way this place works, you think the footsteps are coming right for you!", "You've only got a few seconds before the person making tose footsteps comes around the corner and you have to talk to them! Read something, quick!", "A store attendant walks into the aisle. You know they're a store attendant, because the hooded black cloak they're wearing has an employee badge on it and the first thing they say to you is..."]
everywhere = "everywhere, at all."
hammerspace = "your own inventory"
book_aisle = Aisle("You're now in an aisle of books. Most seem unhelpful to you right now.", "You see books, lots of them. Most seem unhelpful. Though, some of them have bright yellow spines and a familliar logo... These include:", None)
medicine_aisle = Aisle("You're now in an aisle of medicine. Some seems to be more helpful than others.", "You see all kinds of medicine (and all kinds of 'medicine') on the shelves around you. Some seem more helpful than others.", book_aisle)
furniture_aisle = Aisle("You're now in an aisle full of furniture. Mostly just chairs.", "You see furniture of all types, but mostly chairs. They look very comfortable...", medicine_aisle)
trashed_aisle = Aisle("You're now in an aisle full of junk food, and an aisle full of novelty license plates. That is, the two bisect another at odd angles that shouldn't be physically possible. You feel like you're supposed to do something...", "You see two shevles interecting in front of you. One of novelty license plates, one of junk food.", furniture_aisle)
childs_toys_aisle = Aisle("You seem to be in an aisle full of children's toys. No matter where you're going, you can't imagine them being useful.", "You see children's toys on the shelves all around you.", trashed_aisle)
#reverse order
dance_fighting_for_dummies = Item("'Dance fighting, for dummies'", "You learn many new dance moves that should keep the crowd on your side, no matter what.", location = book_aisle, verbs = {"read":True})
time_management_for_dummies = Item("'Time management (in the midst of high-stakes combat), for dummies'", "You learn how to take more time while coming up with what do to next. You also learn that you can start selecting your next move before you're even asked to...", location = book_aisle, verbs = {"read":True})
greater_fireball_for_dummies = Item("'Greater Fireball, for dummies'", "You learn how to make your fireballs burn much hotter. That should come in handy.", location = book_aisle, verbs = {"read":True})
book_selection_for_dummies = Item("'Book selection, for dummies'", "You learn you should have picked a different book.", location = book_aisle, verbs = {"read":True})
shelves = Item("The shelves", "Just some shelves", location = everywhere, scenery = True, verbs = {take:False})
the_floor = Item("The floor", "A perfectly ordinary tiled floor. Nothing strange about it.", location = everywhere, scenery = True, verbs = {take:False})
poisonicine = Item("A bottle labeled 'poisonicine'", "The liquid inside is a vidid pink. The label reads: ", location = medicine_aisle, verbs = {eat:True}) # copy the description from disorient on the murder express into the examine function
three_medkits = Item("3 medkits", "A few medkits. Best save these, you'll never know when you might need them.", location = medicine_aisle)
homeopathic_medicine = Item("A suspicious looking pill container", "The lid is missing, and the bottle says something about herbs. AUST L.", location = medicine_aisle, verbs = {eat:True})
chair = Item("A chair", "A completely normal sized ordinary chair. It's looks pretty heavy, and doesn't fold up.", location = furniture_aisle)
cloak = Item("A strange white cloak (worn)", "A strange white cloak, which reminds you vaguely of the one Death wore, except Death's was black instead. It's very comfortable.", hammerspace, {drop:False})
bop_it = Item("A bop-it toy", "It's a bop-it. The front of the box says \"TRY ME!\".", location = childs_toys_aisle)
pretzels = Item("Some pretzels", "They're plain pretzels. Not incredibly exciting, but they're edible, unlike most of the food you've seen here.", location = trashed_aisle, verbs = {eat:True})
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
 ("examine", "x","read"):examine, \
 ("drop","remove",):drop, \
 ("help",):print_help, \
 ("jump",):jump, \
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
 ("eat","drink"):eat, \
 ("floor",):the_floor, \
 ("chair", "furniture"):chair, \
 ("book selection",):book_selection_for_dummies, \
 ("greater fireball",):greater_fireball_for_dummies,\
 ("time management",):time_management_for_dummies, \
 ("dance fighting",):dance_fighting_for_dummies, \
 ("pretzels", "junk food","food"):pretzels, \
 ("poison", "poisonicine", "pink liquid", "bottle of poison"):poisonicine, \
 ("medkits", "first aid kits", "medkit", "first aid kit", "medpacks", "medpack"):three_medkits, \
 ("medicine", "pill container", "pills", "pill bottle", "medicine bottle", "medicine container", "container"):homeopathic_medicine, \
 ("license plate", "plate", "novelty license plate", "ISO 8601","license plates", "novelty license plates", "plates"):license_plate, \
 ("cloak", "strange white cloak", "white cloak", "strange cloak", "clothes",):cloak, \
 ("children's toys", "children's toy", "child's toy", "child's toys", "bop-it", "toy", "toys"):bop_it, \
 })


inventory = [cloak]
print2("You wake up.", 2)
print2("In a department store.", 2)
print2("Odd. When you black out, you usually seem to wake up in an alley somewhere instead.", 2)
print2("<type 'help' if you need help with this bit>", 2)
print2(childs_toys_aisle.opening)
current_location = childs_toys_aisle
digest["entry time"] = time.time()
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
						turns += 1
					except TypeError:
						print2("You can't just '" + this_verb + "' something.")
				else:
					print2("You can't see a '" + this_noun + "' here")
			else:
				try:
					this_verb_function()
					turns += 1
				except TypeError:
					print2("You can't just '"+this_verb+"' nothing.")
	if spooked:
		if spooked_stage == 6:
			break
		if time.time() - spooked_time > 6:
			spooked_stage += 1
			print2(spooky_messages[spooked_stage], 2)
			if spooked_stage == 5:
				break
			spooked_time = time.time()
print2('"Hi, how can I help you?"') 
digest = {**{"books":books_read, "flagged":flagged, "pretzels eaten":(pretzels.location == "hell"), "medkits":(three_medkits in inventory), "chair":(chair in inventory), "stuff":(len(inventory)>1)}, **digest}
#print(digest) #debug only
input("Hit <ENTER> to continue")
darkness_envelops()

		




