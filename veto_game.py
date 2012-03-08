#
# Veto card game
#
import random

# each card is represented by a three digit number
# the first digit is the suit
#   1 Hearts
#   2 Diamonds
#   3 Clubs
#   4 Spades
# the second and third digits represent the value
#   01 ace
#   02 2
#   03 3
#   04 4
#   05 5
#   06 6
#   07 7
#   08 8
#   09 9
#   10 10
#   11 jack
#   12 queen
#   13 king
suits=['null','Hearts','Diamonds','Clubs','Spades']
values=['null','Ace','2','3','4','5','6','7','8','9','10','Jack','Queen','King']
def suit(cardNumber):
    return cardNumber//100
def value(cardNumber):
    return cardNumber%100
def cardName(cardNumber):
    return values[value(cardNumber)]+' of '+suits[suit(cardNumber)]

# all common stuff goes here
class Game:
    def __init__(self):
        self.initialChips=1000;
        self.ante=10;
        self.anteStep=5;
        self.handNumber=0;
        self.dealer=0;
        self.common=[000,000,000,000,000] #flop flop flop turn river
        self.phase='flop'
        self.activeCards=[False,False,False,False,False]
        #T T T F F => phase==flop
        #F F F T F => phase==turn
        #F F F F T => phase==river
        self.resetActiveGames()
    def resetActiveGames(self):
        self.activeGames=['Holdem High','Holdem Low','BlackJack','LowBall']

# deck is a class consisting of a list of 52 cards,
#  each of which is the value of a card per above,
#  and an integer to act as the index (1-52)
class Deck:
    def __init__(self):
        self.shuffle()
    def shuffle(self):
        self.pile=[] #must completely rebuild deck
        for i in range(101,402,100): #101, 201, 301, 401
            self.pile[0:0]=range(i, i+13, 1) #101-113
        self.pile=random.sample(self.pile,52)
    def draw(self):
        return self.pile.pop()

# player class
class Player:
    def __init__(self,ID,name):
        self.ID=ID
        self.name=name
        self.reset()
        self.chips=0
    def addChips(self,plusChips):
        self.chips+=plusChips
    def subChips(self,minusChips):
        if minusChips>self.chips:
            print('error: not enough chips')
            return
        else:
            self.chips-=minusChips
    def reset(self):
        self.hits=[False,False,False,False,False] #flop flop flop turn river
        self.cards=[]#own own [flop flop flop turn river]
    def addCard(self,card):
        self.cards.append(card)
    def numberCards(self):
        return len(self.cards)
    def setHits(self,hitList):
        for i in range(len(self.hits)):
            self.hits[i]=self.hits[i] or hitList[i]
    def getBJTotal(self):
        hasAce=False
        total=[0]
        for i in range(len(self.cards)):
            if value(self.cards[i])==1: #if ace
                hasAce=True
            total[0]+=min(value(self.cards[i]),10)
        if hasAce and max(total) <= 11:
            total.append(max(total)+10)
        if min(total)>21: #if bust in blackjack
            total=[0] #set to lowest value
        return total
    def getLBTotal(self):
        subtotal=0
        total = [len(self.cards)]
        for i in range(len(self.cards)):
            subtotal+=min(value(self.cards[i]),10)
        if subtotal>30: #if bust in lowball
            total[0]=0 #set number of cards to lowest value
        total.append(subtotal) #update total to reflect changes
        return total

# begin actual code
game=Game()
deck=Deck()
nplayers=int(input('How many players? '))
#create players
player=[]
for i in range(nplayers):
    print('Player',i+1)
    name=input('What is your name? ')
    player.append(Player(i+1,name))
    player[i].addChips(game.initialChips)
#begin game
print('Game start!')
while True:
    #reset for new hand
    deck.shuffle()
    game.phase='flop'
    #deal cards
    for i in range(len(player)):
        player[i].reset()
        player[i].addCard(deck.draw())
        player[i].addCard(deck.draw())
        print('Cards for',player[i].name)
        print('  ',cardName(player[i].cards[0]))
        print('  ',cardName(player[i].cards[1]))
    #begin rounds
    while 'done' not in game.phase:
        #burn a card
        deck.draw()
        #set active cards
        if 'flop' in game.phase:
            deck.draw() #if on flop, burn another card
            game.activeCards=[True, True, True, False, False]
        elif 'turn' in game.phase:
            game.activeCards=[False, False, False, True, False]
        else: #river
            game.activeCards=[False, False, False, False, True]
        #draw active cards
        for i in range(len(game.activeCards)):
            if game.activeCards[i]:
                game.common[i]=deck.draw()
        #get hits
        for i in range(len(player)):
            if 'flop' in game.phase:
                print(player[i].name,'choose which cards to hit: [flop1] [flop2] [flop3]')
                hits=input(' enter 1 and/or 2 and/or 3 to hit those cards: ')
                player[i].setHits(['1' in hits, '2' in hits, '3' in hits, False, False])
            elif 'turn' in game.phase:
                print(player[i].name,'choose whether to hit card: [turn1]')
                hits=input(' enter 1 to hit that card: ')
                player[i].setHits([False, False, False, '1' in hits, False])
            else: #river
                print(player[i].name,'choose whether to hit card: [river1]')
                hits=input(' enter 1 to hit that card: ')
                player[i].setHits([False, False, False, False, '1' in hits])
        #reveal common card(s)
        for i in range(len(game.activeCards)):
            if game.activeCards[i]:
                print(game.phase,'card is',cardName(game.common[i]))
        #add hit cards to hands
        for i in range(len(player)):
            for j in range(len(game.activeCards)):
                if game.activeCards[j] and player[i].hits[j]:
                    player[i].addCard(game.common[j])
            #get totals
            bjTotal=player[i].getBJTotal()
            lbTotal=player[i].getLBTotal()
            #show blackjack totals
            if min(bjTotal)==0:
                print(player[i].name,'busts at BlackJack!')
            else: #player does not bust
                print(player[i].name,'your BlackJack total(s):',bjTotal)
            #show lowball totals
            if min(lbTotal)==0:
                print(player[i].name,'busts at LowBall!')
            else: #player does not bust
                print(player[i].name,'your LowBall total:',lbTotal)
            
        #change phase
        if 'flop' in game.phase:
            game.phase = 'turn'
        elif 'turn' in game.phase:
            game.phase = 'river'
        else: #river
            game.phase = 'done'
    #all finished with round
    print('  Time to see who won')
    #declare winner
    if 'Holdem High' in game.activeGames:
        print('Holdem High not yet programmed')
    if 'Holdem Low' in game.activeGames:
        print('Holdem Low not yet programmed')
    if 'BlackJack' in game.activeGames:
        bjWinnerName=['']
        bjWinnerTotal=0
        for i in range(len(player)):
            bjTotal=player[i].getBJTotal()
            if max(bjTotal)>bjWinnerTotal: #has highest score outright, which inherently has to be a non-bust
                bjWinnerTotal = max(bjTotal)
                bjWinnerName = [player[i].name]
            elif max(bjTotal)>0 and max(bjTotal)==bjWinnerTotal: #no bust and tied with winner
                bjWinnerName.append(player[i].name)
        print(bjWinnerName,'win(s) at BlackJack!')
    if 'LowBall' in game.activeGames:
        lbWinnerName=['']
        lbWinnerTotals=[0,30]
        for i in range(len(player)):
            lbTotal=player[i].getLBTotal()
            if lbTotal[0]>lbWinnerTotals[0]: #has most cards outright, which inherently has to be a non-bust
                lbWinnerTotals = lbTotal #set both max number of cards and total for those cards
                lbWinnerName = [player[i].name]
            elif lbTotal[0]>0 and lbTotal[0]==lbWinnerTotals[0]: #no bust, same # of cards as winner
                if lbTotal[1]<lbWinnerTotals[1]: #same number of cards but lower total
                    lbWinnerTotals=lbTotal #still win
                    lbWinnerName = [player[i].name] #overwrite all
                elif lbTotal[1]==lbWinnerTotals[1]: #tie for total as well
                    lbWinnerName.append(player[i].name)
        print(lbWinnerName,'win(s) at LowBall!')

    print('round over')
