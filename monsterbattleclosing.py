#!/bin/python3
#debug - remove this
DEBUG_fast_mode = False
#digest = {"books":[greater_fireball_for_dummies, dance_fighting_for_dummies, time_management_for_dummies], "flagged":True, "pretzels eaten":False, "medkits":True, "chair":True}

#redefine everything that needs to be
fighter_order = [Billy, Fred]
deafened = False
firstdance = False
hearing_loss = 0
if digest["medkits"]:
	medpacks = 3
else:
	medpacks = 0

Greater_fireball = Attack("Greater fireball", "shoot an absolutely huge fireball", (10,16), "Fire", burn)

if time_management_for_dummies in digest["books"]:
	time_to_beat = 20
if greater_fireball_for_dummies in digest["books"]:
	Player.attacks.append(Greater_fireball)
if dance_fighting_for_dummies in digest["books"]:
	dances = 4
transfixed = False
wins = 0
wild_magic = 1
Fred.health = 60
Billy.health = 60
Player.health = 70
Player.status["burning"], Player.status["frozen"],  Billy.status["burning"], Fred.status["burning"] = False, False, False, False
def smash(**args):
	print2("The chair splinters as you swing it!")
	print2("It's completely destroyed!!!")
	Player.attacks.remove(Chair)
Chair = Attack("Chair smash", "bash your opponent over the head with a chair", (20,30), "Melee", smash)
if digest["chair"]:
	Player.attacks.append(Chair)


print2("You're in the center of a vast colleseum. This time, you know exactly why. And this time, you're gonna win.", 4)
print2("Remember, write attacks with the starting capital letter.", 2)
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
		print2("You've done it. You've won.", 2)
		deafened = False
		print2("Your hearing clears...", 2)
		print2("The crowd starts to cheer your name...",2)
		if digest["grudge"]:
			print2("Death appears before you. This time, they're actually supposed to.", 2)
		else:
			print2("Death appears before you. This time, you're not surprised.",2)
		print2("""      
             ___          
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
           |_________\\    """, 4)
		print2("Nɪᴄᴇ ᴊᴏʙ, Sᴄᴏᴜᴛ", 2)
		print2("Scout. It's not your name, but it'll do, you think.", 3)
		print2("Everything goes white...",3)
		darkness_envelops(white = True)
		print2("That's it, really. That's the end of the game.", 2)
		input("Hit <ENTER> to exit")
		print2("Bʏᴇ!")
		sys.exit()

print2("On the edge of death, your hearing clears...", 2)
deafened = False
print2("Rᴇᴀʟʟʏ?")
sys.exit()
