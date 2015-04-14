# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = [0,0,0,0]

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        myhand = "Hand contains"
        for i in self.hand:
            myhand += " " + str(i)
        return myhand
        
    def add_card(self, card):
        self.hand.append(card)	# add a card object to a hand

    def get_value(self):
        self.value = 0
        count_A = 0
        loop = 1
        temp = 0
        for card in self.hand:
            if card.get_rank() == "A":
                count_A = count_A+1
                self.value += VALUES[card.get_rank()]+10
            else:
                self.value += VALUES[card.get_rank()]           	
        if (count_A!=0) and (self.value >21):
            while loop <=count_A:
                if (0<self.value) and (self.value> 21):
                    self.value -= 10
                loop += 1
         
        return self.value 

    def draw(self, canvas, pos):
        card_loc = (card_size[0] * (0.5 + RANKS.index(self.rank)), card_size[1] * (0.5 + SUITS.index(self.suit)))
        canvas.draw_image(card_images, card_loc, card_size, [pos[0] + card_size[0] / 2, pos[1] + card_size[1] / 2], card_size)
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit,rank))
    
    def shuffle(self):
        return random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop(0)
    
    def __str__(self):
        cards = "Deck contains"
        for card in self.deck:
            cards += " " +str(card)
        return cards


#define event handlers for buttons
def deal():
    global outcome, in_play,player,dealer,newgame,score
    newgame = Deck()
    newgame.shuffle()
    player = Hand()
    dealer = Hand()
    counter = 0
    outcome = ""
    if in_play == True:
        outcome = "Dealer wins!"
        score[2] += 1
        score[1] += 1
        in_play = False
    else:
        while counter <=1:	
            player.add_card(newgame.deal_card())
            dealer.add_card(newgame.deal_card())
            counter +=1 
        in_play = True

def hit():
    global in_play, outcome,player,dealer,newgame
    if player.get_value() <= 21 and in_play == True:
        player.add_card(newgame.deal_card())
        outcome = "Hit or stand"	
        if player.get_value() > 21:
            outcome = "Player has busted, new deal?"
            score[2] += 1
            score[1] += 1
            in_play = False
       
def stand():
    global in_play, outcome,player,dealer,newgame,score
    while dealer.get_value() <= 16 and in_play == True:
        dealer.add_card(newgame.deal_card())
        if dealer.get_value() > 21:
            outcome = "Dealer has busted"
            score[0] += 1
            score[3] += 1
            in_play = False
    while in_play == True:
        if dealer.get_value()< player.get_value():
            outcome = "Player wins, new deal?"
            score[0] += 1
            score[3] += 1
            in_play = False
        else:
            outcome = "Dealer wins, new deal?"
            score[2] += 1
            score[1] += 1
            in_play = False
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global player,in_play,dealer, outcome,score
    canvas.draw_polygon([(0, 0), (600, 0), (600, 60),(0, 60)], 1, 'Blue', 'White')
    canvas.draw_text('BlackJack', (5, 40), 40, 'black')
    canvas.draw_text('Player', (20, 110), 50, 'Red')
    canvas.draw_text('Dealer', (450, 580), 50, 'Red')
    for i in range(40):
        canvas.draw_image(card_back, CARD_CENTER, CARD_SIZE, [100+i*10,335], CARD_SIZE)
    for i in range(len(player.hand)):
        player.hand[i].draw(canvas, [50+(i*15), 140])
    
    if not in_play:
        for i in range(len(dealer.hand)):
            dealer.hand[i].draw(canvas, [430+(i*15), 440])
    else:
        for i in range(len(dealer.hand)):
            dealer.hand[i].draw(canvas, [430+(i*15), 440])
        canvas.draw_image(card_back, CARD_CENTER, CARD_SIZE, [480, 488], CARD_SIZE)
    canvas.draw_text(str(outcome), (80, 270), 40, 'black')
    canvas.draw_text(str("Player"), (310, 37), 20, 'black')
    canvas.draw_text(str("Dealer"), (310, 57), 20, 'black')
    canvas.draw_text(str("win"), (380, 17), 20, 'black')
    canvas.draw_text(str("lose"), (430, 17), 20, 'black')
    canvas.draw_text(str("score"), (480, 17), 20, 'black')
    canvas.draw_text(str(score[0]), (390, 37), 20, 'black')
    canvas.draw_text(str(score[1]), (440, 37), 20, 'black')
    canvas.draw_text(str(score[2]), (390, 57), 20, 'black')
    canvas.draw_text(str(score[3]), (440, 57), 20, 'black')
    canvas.draw_text(str(score[0]-score[1]), (490, 37), 20, 'black')
    canvas.draw_text(str(score[2]-score[3]), (490, 57), 20, 'black')



# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()
