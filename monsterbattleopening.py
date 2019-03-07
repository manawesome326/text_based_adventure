#!/bin/python3
	
		
#copy+pasted from stack overflow
def remove_text_inside_brackets(text, brackets="{}"): 
		count = [0] * (len(brackets) // 2) # count open/close brackets
		saved_chars = []
		for character in text:
				for i, b in enumerate(brackets):
						if character == b: # found bracket
								kind, is_close = divmod(i, 2)
								count[kind] += (-1)**is_close # `+1`: open, `-1`: close
								if count[kind] < 0: # unbalanced bracket
										count[kind] = 0  # keep it
								else:  # found bracket to remove
										break
				else: # character is not a [balanced] bracket
						if not any(count): # outside brackets
								saved_chars.append(character)
		return ''.join(saved_chars)
		
class Attack:
	def __init__(self, name, message, damagerange, damagetype, special=None):
		self.name = name
		self.damagerange = damagerange
		self.damagetype = damagetype
		self.special = special
		self.message = message
	def use(self, user):
		if user == Player:
			damagethistime = self.damage
			print2("You " + remove_text_inside_brackets(self.message)+ ", dealing " + str(damagethistime) +" "+  str(self.damagetype) + " damage." )
			fighter.health -= damagethistime
		else:
			damagethistime = self.damage
			print2(user.name + " " + re.sub("{|}", "", self.message) + ", dealing " + str(damagethistime) +" "+ self.damagetype + " damage." )
			Player.health -= damagethistime
		try:
			self.special(user=user, damagedone=damagethistime)
		except TypeError:
			pass
		print2(user.art)
	@property
	def damage(self):
		return random.choice(list(range2(self.damagerange)))

def deafen(**args):
	global deafened
	global hearing_loss
	print2("It's so loud, you suddenly find it hard to hear!")
	deafened = True
	Player.health -= 5
	hearing_loss += 1
	
def self_hurty(**args):
	print2("...to yourself.")
	fighter.health += args["damagedone"]
	Player.health -= args["damagedone"]
	
def burn(**args):
	global wild_magic
	if args["user"] == Player:
		if fighter.status["burning"] == False:
			print2("The attack burns viciously!")
			print2(fighter.name + " will take extra damage every turn")
			fighter.status["burning"] = True
		if random.random() < wild_magic/20: 
			print2("You roll a 1 on the wild magic check.")
			print2("Cause I can't be bothered to properly implement that, you just take 15 damage")
			Player.health -= 15
		wild_magic += 1
	if args["user"] == fighter:
		print2("The attack burns viciously!")
		print2("You will take extra damage next turn!")
		Player.status["burning"] = True
		if random.random() < 0.05:
			print2(fighter.name + " rolls a 1 on the wild magic check.")
			print2("Cause I can't be bothered to properly implement that, they just take 15 damage")
			fighter.health -= 15

		
	
dances = 1
def determination(**args):
	global firstdance 
	global dances
	if args["user"] == Player and dances >= 0:
		if fighter == Fred and firstdance == False:
			print2("The crowd does wild at the awesome dance battle!")
			print2("The cheering gives you a rush of determination, healing 10 damage!")
			Player.health += 10
			fighter.health += 3
			firstdance = True
		else:
			print2("The crowd cheers at your sick moves!")
			print2("You get a slight rush of determination, healing 2 damage!")
			Player.health += 3
		dances -= 1
	elif args["user"] == Player:
		print2("You've overexhausted your dances and can't come up with any moves!")
		print2("The crowd boos, hurting you mentally!")
		print2("You take 15 damage!")
		Player.health -= 15
		dances -= 1


def stop_drop_and_roll(**args):
	if args["user"].status["burning"]:
		args["user"].status["burning"] = False
		print2("The flames are put out harmlessly-ish")
		args["user"].health += 1
	else:
		print2("Well that was fantastically useless, wasn't it?")

def free_health(**args):
	global medpacks
	global transfixed
	if medpacks <= 0:
		print2("Just kidding, you're completely out")
	else:
		print2("It restores 10 of your health!")
		Player.health += 10
		print2("Your opponent is so transfixed, they lose their turn!")
		transfixed = True
	medpacks -= 1

def frozen(**args):
	print2("You're encased in a pillar of ice!")
	Player.status["frozen"] = True


Dance = Attack("Dance", "do{es} a sick dance", (7,12), "Melee", determination)
Freeze = Attack("Freeze", "encases you in a pillar of ice", (1,3), "Ice", frozen)
Fireball = Attack("Fireball", "shoot{s} a massive fireball", (6,8), "Fire", burn)
Moo = Attack("Moo", "moos loudly", (0,6), "Sonic", deafen)
Distracted = Attack("Distracted", "get distracted and trip over", (1, 5), "Melee", self_hurty)
Roll = Attack("Roll", "stop{s}, drop{s}, and roll{s}", (0,0), "\b", stop_drop_and_roll)
Heal = Attack("Do a heal real quick", "pull out a medpack and heal, in the midst of battle", (0,0), "\b", free_health)

class Monster:
	# give it attributes
	def __init__(self, name, health, attacks, art, lines, AI):
		self.health = health
		self.attacks = attacks
		self.name = name
		self.lines = lines
		self.art = art
		self.selectmove = AI
		self.status = {"burning":False, "frozen":False}
	# teach it chat
	def chat(self):
		return(random.choice(self.lines))

# make our monsters

def Fred_AI():
	if Fred.status["burning"]:
		return Roll
	else:
		return random.choice((Dance,Freeze,Dance))

def Billy_AI():
	if turns == 0:
		return Moo
	else:
		return random.choice(Billy.attacks)

Fred = Monster("Fred", 69, [Dance, Roll, Freeze], """
      ___
  ___|___|____
    { - - }
     /| |\\
     _| |_
		""", [
			"\"Have you ever played EyeWire? It's a lot of fun\"",
			"\"I think I might go and get a pizza later.\"",
			"\"Ah, battling is so relaxing, don't you find?\"",
			"\"Fancy a cup of tea? I must say I'm quite fond of the stuff.\"",
			"\"I was thinking of taking up a teaching position at LHS.\"",
			"\"I really don't think they should force young people to go to school.\"",
			"\"Yep, time for a nap soon I think.\"",
			"\"I found this cool website called ABC news. It's so engrossing.\"",
			"\"I sure love dancing, don't you?\""
		], Fred_AI)
Billy = Monster("Billy", 68, (Moo, Fireball), """
             ^__^
     _______/(oo)
/\\/(       /(__)
     ||w----||   
     ||     ||   """, ["Billy moos", "Billy moos", "Billy stares straight into your soul", "\"moo\""], Billy_AI)#MAKE HEALTH 69 IN RELEASE

Player = Monster("You", 69, (Fireball, Dance, Roll, Heal), """
o.o
 | 
/\\ """, [], None) 

def player_turn():
	global transfixed
	try:
		options_time = time.time()
		triedattack = input("What attack shall you use next? You can use \"" + "\", \"".join([x.name for x in Player.attacks[:-1]]) + "\" or \"" + "".join([x.name for x in Player.attacks[-1:]]) + "\" ")
		usedattack = globals()[triedattack]
		if usedattack == Heal:
			raise KeyError("oh no!")
	except KeyError:
		if triedattack == Heal.name:
			usedattack = Heal
		else:
			usedattack = Distracted
	new_time = time.time()
	if new_time - options_time > 4:
		print2("You took more than 4 seconds to choose, so you flounder the attack!")
		usedattack = Distracted

	if not Player.status["frozen"]:
		usedattack.use(Player)  
	else:
		Player.status["Burning"] = False
		if usedattack == Fireball:
			print2("The fireball unfreezes you!")
			print2("Take another turn!")
			Player.status["frozen"] = False
			transfixed = True
		else:
			print2("You're frozen and can't do that!")
	if Player.status["burning"]:
		Player.health -= 10
		print2("Ouch, that's hot!")
		print2("You take 10 damage from the flames!")
	global dances 
	if dances < 0.8:
		dances += 0.4
	if dances < 0:
		dances /= 2

def enemy_turn():
	global transfixed
	usedattack = fighter.selectmove()
	if not transfixed:
		usedattack.use(fighter)
	else:
		transfixed = False
	if fighter.status["burning"]:
		fighter.health -= 10
		print2("Your opponent takes 10 damage from your flames!")
	print2(fighter.chat())


fighter_order = [Billy, Fred]
deafened = False
firstdance = False
hearing_loss = 0
medpacks = 2
transfixed = False
wins = 0
wild_magic = 1

def turn_loop():
	global transfixed
	global hearing_loss
	global Player
	global turns
	global fighter
	global wins
	while fighter.health > 0 and Player.health > 0:
		player_turn()
		if not transfixed:
			enemy_turn()
		else:
			transfixed = False
		print2("You now have "+ str(Player.health) + " health left. " + fighter.name + " has " + str(fighter.health))
		turns += 1
		hearing_loss -= 0.3
	if fighter.health <= 0:
		wins += 1
		return(True)
	else:
		return(False)


print2("You're in the center of a vast colleseum. You're not sure why, or how, but you are, and you're determined to win.", 4)
print2("Names of attacks must be written exactly as they're shown, btw.", 2)
print2("A fighter approaches. Here's who you're up against: ")
fighter = fighter_order[wins]
print2(fighter.art)
print2("Truly frightening. Well, go get em! ")
victory = turn_loop()
if victory:
	Player.health += 20
	print2("You feel pride in your victory, momentarily, and are just starting to heal (+20 health), when suddenly a new fighter appears. They certainly seem more formidable than the last one.", 4)
	print2("Here's who you're up against:")
	wild_magic /= 3
	wild_magic = math.floor(wild_magic)
	hearing_loss -= 1.3
	fighter = fighter_order[wins]
	print2(fighter.art)
	victory = turn_loop()
	if victory:
		print2("Somehow, miraculously, you survived against your opponent. Your hearing clears...")
		deafened = False
		print2("The crowd begins to cheer your name in excitement!")
		print2("""The thing is, though, that you're not totally sure what they were actually cheering. At the time it seemed obvious to you that it was your name, but when asked about it later you weren't able to actually say for sure what it was. When members of the crowd were asked, roughly half of them had no idea at all, while the other half had varying guesses based off what they thought everybody else was cheering. These guesses varied from "Fred", to "Rincewind", to "Gertrude". None of the guesses seemed like very good names at all, and regardless of whether or not they were right you didn't like the selection. One member of the crowd said that he actually read the program guide, which said that your name was actually \""""+ getpass.getuser()+"""\", a fact which you vehemently denied. Wait, you don't know you're going to do that yet. Dammit!""")
		print2("...", 2)
		print2("Point is, at this point Death comes along and he's gonna kill you anyway, because you weren't actually supposed to be able to win that.", 3)
		with_a_grudge = True
if wins < 2:
	print2("On the edge of death, your hearing clears...",2)
	deafened = False
	print2("You see a spectre of Death before you...",2)
print2("""            ___          
        /   \\\\        
   /\\\\ | . . \\\\       
 ////\\\\|     ||       
////   \\\\ ___//\\       
///      \\\\      \\      
///       |\\\\      |     
//         | \\\\  \\   \\    
/          |  \\\\  \\   \\   
       |   \\\\ /   /   
       |    \\/   /    
       |     \\\\/|     
       |      \\\\|     
       |       \\\\     
       |        |     
       |_________\\ """, 3)
print2("Wait, that's the wrong one, this one actually looks like pretty cool.")
print2("Tʜᴀɴᴋꜱ, I ɢᴜᴇꜱꜱ?")
print2("Wait, you don't have any lines until chapter --", 2)
print2("Forget it. You know what to do!")
print2("Sᴏʀʀʏ ᴀʙᴏᴜᴛ ᴛʜɪꜱ")
print2("Death swings the scythe towards you, and everything goes dark...")
input("Hit <ENTER> to continue")
darkness_envelops()


