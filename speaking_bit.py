#!/bin/python3

#DEBUG ONLY
digest = {"flagged":True, "pretzels eaten":True, "stuff":True, "entry time":time.time()}
#DEBUG ONLY


def make_a_choice(options):
	i = 1
	for option in options:
		try:
			print2("[" + str(i) + '] "' + option.question + '"', 0.2)
		except AttributeError:
			print2("[" + str(i) + '] "' + option + '"', 0.2)
		i += 1
	while True:
		try:
			_decision = input(">> ")
			return(options[int(_decision)-1])
		except (IndexError, ValueError):
			print2("<please pick a number from 1 to " + str(len(options)) + ">")
#
#print2("What followed was an incredibly engaging and highly informative sequence of dialogue.", 3)
#print2("Thing is, though, I didn't actually get it done in time.", 1)
#print2("Let's just jump right into the last combat scene, shall we?")
#print2("Okay...")
#
class Question:
	def __init__(self, question, response_function):
		self.question = question
		self.response_function = response_function
	@property
	def response(self):
		global available_options
		available_options.remove(self)
		return(self.response_function)

#honestly not sure classes are the way to go here, but what the heck

def are_you_death_funct():
	global available_options
	print2("After all, they were holding a scythe...\n", 2)
	print2("𝒀𝒆𝒔", 2)
	print2("You react to this by freaking out.",2)
	print2('"Hah! I\'m just messing with you. My name\'s Jimmy"', 2)
	print2("You stop freaking out, and go back to the base level of 'kinda freaked out' that you've been in all this time.", 3.1)
	print2('"No, I\'m not him, I just work for him, and he prefers the name \'The Grim Reaper\', or just \'Grim\' if you\'re cool, like me."', 3.6)
	print2('"...I\'m still working on my impression"')
	available_options.append(whats_death_like)
	#available_options.append(why_the_outfit)

def where_am_i_funct():
	global available_options
	print2("An obvious question to ask.\n", 2)
	print2('"You\'re in purgatory, but only, uh, kind of."', 2)
	print2('"Kind of?", you prompt.', 2)
	print2('"Honestly, this place is a little hard to describe properly. I\'ll explain later, if we have time."', 2.5)
	available_options.append(whys_it_walmart)

def how_to_pay_funct():
	global available_options
	print2("Of course, you wouldn't be one to steal...\n", 2)
	print2('"You don\'t have to! Everything in purgatory is just here for whoever needs it.\"', 3)
	print2('"...also, I\'ve got no clue where the checkouts are.\"',2)

def ate_loose_pretzels_funct():
	global available_options
	print2("You're beginning to doubt whether eating them was a good idea.\n", 2)
	print2('"Wait, you didn\'t actually eat those, did you?"', 2)
	pretzels_actually_eaten = make_a_choice(["Yes.", "No."])
	if pretzels_actually_eaten == "Yes.":
		time.sleep(2)
		print2('"Oh god. This isn\'t going to be fun for either of us. Looks like I\'ve got a lot of paperwork to do..."', 3)
	else:
		time.sleep(2)
		print2('"That\'s a relief. If you had said yes, I would have had a lot of paperwork to do. Look, if you did, you\'re in for a wild ride..."', 3)

def whats_death_like_funct():
	global available_options
	print2('"He\'s pretty cool, actually. Very hands off, lets us do our job easier."', 2)
	#available_options.append(what_you_do)

def scouted_an_aisle_funct():
	global available_options
	print2('"Oh hey, that was you. Nice job. Once we get this mess sorted out, maybe put in a promotion request!"', 3)
	print2("That wasn't an answer, but you get the feeling asking again would make you look like a bit of an idiot.",3)
	#available_options.append(promotion_request)
	#available_options.append(what_mess)

def whys_it_walmart_funct():
	datetime_nonsense = (datetime(1,1,1) + timedelta(seconds=(time.time() -digest["entry time"])))
	print2('"Don\'t ask me. It didn\'t look like one ' + str(datetime_nonsense.minute) + ' minutes and ' + str(datetime_nonsense.second) + ' seconds ago."', 3)

def how_to_leave_funct():
	print2("You're getting sick of all this dialogue, aren't you? Nevermind all the effort I put into it. Fine, just skip to the cool battle scene.\n", 4)
	print2('"Well, funny story actually..."', 2)
	print2('"I haven\'t really got a clue. It\'s only my third day on the job, Grim never told me what to do when this happened, so you may as well just settle--"',4)
	print2("You hear the sound of a phone ringing.", 2)
	print2("*ʀɪɴɢ... ʀɪɴɢ...*", 2)
	print2("Jimmy digs a phone out from his cloak, and answers.", 2)
	print2("The ensuing conversation didn't make a lot of sense to you.", 2)
	print2('"Well that was good timing. Grim\'s got a job for you. Says that it\'s "very self-explanatory". Any second now you should--"', 4)
	print2("And then everything goes dark.")

are_you_death = Question("Death?", are_you_death_funct)
where_am_i = Question("Where am I?", where_am_i_funct)
how_to_pay = Question("How do I pay for all this stuff I'm carrying?", how_to_pay_funct)
ate_loose_pretzels = Question("What was up with those loose pretzels earlier?", ate_loose_pretzels_funct)
whats_death_like = Question("What's working for the Grim Reaper like?", whats_death_like_funct)
scouted_an_aisle = Question("What was up with the 'scouted an aisle for 50 points' thing from earlier?", scouted_an_aisle_funct)
whys_it_walmart = Question("Why does purgatory look like a department store?", whys_it_walmart_funct)

how_to_leave = Question("So how do I get out of here?", how_to_leave_funct)

free_options = []
available_options = [are_you_death, where_am_i]
if digest["stuff"]:
	free_options.append(how_to_pay)
if digest["pretzels eaten"]:
	free_options.append(ate_loose_pretzels)
if digest["flagged"]:
	free_options.append(scouted_an_aisle)

print2("What follows is a highly engaging dialogue sequence.",1.5)
print2("(just letting you know)", 1.5)
print2("So, what do you say to this mysterious fellow first?", 1.5)
turns_at_dialog_start = turns
while True:
	choice = make_a_choice(available_options)
	time.sleep(0.1)
	choice.response()
	if choice == how_to_leave:
		break
	print2("")
	try:
		available_options.append(free_options.pop(0))
	except IndexError:
		pass
	turns += 1
	if turns - turns_at_dialog_start == 6:
		available_options.append(how_to_leave)

darkness_envelops()
