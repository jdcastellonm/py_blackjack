import random

ranks = ['ACE', 'TWO', 'THREE', 'FOUR','FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE', 'TEN','JACK', 'QUEEN', 'KING']
suits = ['CLUBS', 'SPADES', 'HEARTS', 'DIAMONDS']
deck = []	# deck of 52 cards
hand = []	# the player's current hand of two cards
score = 0
funds = 0
game_over = True
soft_hand = False

class Card:
	# Card object which contains a suit and a rank. 52 of these will form a deck
	suit = ''
	rank = ''
	value = 0
	
	def __init__(self, suit = '', rank = '', value = 0):
		self.rank = rank
		self.suit = suit
		self.value = value + 1

	def get_card(self):
		# return a string of the card
		return (self.rank + " of " + self.suit)

	def get_value(self):
		# return the value of the card. jack, queen and king are worth 10. ace is either 1 or 11
		if self.rank == 'JACK' or self.rank == 'QUEEN' or self.rank == 'KING':
			return 10
		else:
			return self.value
temp_card = Card()


def initialize_deck():
	# initialize a deck of 52 cards, using two loops
	global deck
	for each_suit in suits:
		for each_rank in ranks:
			deck.append(Card(each_suit, each_rank, ranks.index(each_rank)))	# use index of each card as its value, +1

def deal_hand():
	# deal two random cards from deck into player's hand
	global deck
	global hand
	global score
	global game_over

	score = 0
	hand.append(random.choice(deck)) # draw first card
	temp = random.choice(deck)	# draw second card, but store it in temp to check for duplicate
	while temp in hand:
		temp = random.choice(deck)
	hand.append(temp)
	game_over = result()	# in case the first two cards add up to 21

def hit_me():
	# deal additional card
	global deck
	global hand
	global game_over
	global temp_card
	temp_card = random.choice(deck)
	while temp_card in hand:
		temp_card = random.choice(deck)
	hand.append(temp_card)
	game_over = result()	# determine result after drawing card

def result():
	# check the score and determine win/loss
	global score
	global hand
	global funds
	global game_over
	global soft_hand

	score = 0	# reset score before counting card values

	for each_card in hand:	# show the hand and add up the values
		print(each_card.get_card())
		score += each_card.get_value()
		# count an ace card as 11 points if the total score is less than 12, since 10 + 11 = 21. Every ace is worth 1 otherwise
		if score < 12 and each_card.rank == 'ACE':
			score += 10	
			soft_hand = True	# set soft flag
	
	# determine win/loss	
	if score < 21:
		print("You have " + str(score) + ".")
		return False
	elif score == 21:
		print("You got 21! You win $100.\n")
		funds += 100
		if soft_hand:
			soft_hand = False
		return True
	else:
		if soft_hand:
			score -= 10		# revert the 11 point Ace back to 1 point, if a soft hand is active
			soft_hand = False
			if score < 21:
				return False	# game is not over if hand is below 21 after Ace is reverted
			elif score == 21:
				print("You got 21! You win $100.\n")
				funds += 100
				return True
		print("You have " + str(score) + ". You lose.")
		funds -= 50
		return True
		
initialize_deck()