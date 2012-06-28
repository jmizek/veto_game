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
#return toAdd where toAdd has all values list3[i] for which (list1[i] and list2[i]) evaluates as true
def andList(list1,list2,list3):
    if len(list1) != len(list2) or len(list1) != len(list3):
        print('error: Lists are of unequal length')
        return
    toAdd=[]
    for i in range(len(list1)):
        if list1[i] and list2[i]:
            toAdd.append(list3[i])
    return toAdd
#return the entries in list1 that are not in list 2
def diffList(list1,list2):
    difference=[]
    for i in range(len(list1)):
        if list1[i] not in list2:
            difference.append(list1[i])
    return difference
#return winner for BJ given a list of the totals
def BJWinner(totals):
    return ###TODO

#><><><><><><><#
#  game class  #
#><><><><><><><#
class Game: # all common stuff goes here
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
        self.resetVetos()
    def resetActiveGames(self):
        self.activeGames=['Holdem High','Holdem Low','BlackJack','LowBall']
    def resetVetos(self):
        self.vetos=[]
        for all in self.activeGames: #[Holdem High,Holdem Low,BlackJack,LowBall]
            self.vetos.append(0)
    def castVeto(self, vote):
        if vote<0 or vote>=len(self.activeGames):
            print('error: vote is out of bounds',vote)
            return
        vetos[self.activeGames.index(vote)]+=1 #needs fixing almost assuredly
    def resolveVotes(self):
        topGames=[]
        topVetos=0
        for i in range(len(self.activeGames)):
            if self.vetos[i]>topVetos:
                topVetos=self.vetos[i]
                topGames=[self.activeGames[i]]
            elif self.vetos[i]==topVetos:
                topGames.append(self.activeGames[i])
        if topGames == self.activeGames: #might need to fix
            return 'No game'
        else:
            self.activeGames=diffList(self.activeGames,topGames)
            return topGames
    

#><><><><><><><#
#  deck class  #
#><><><><><><><#
class Deck:
    def __init__(self):
        self.shuffle()
    def shuffle(self):
        self.pile=[] #must completely rebuild deck
        #first add all the cards to the deck
        for i in range(101,402,100): #101, 201, 301, 401
            self.pile[0:0]=range(i, i+13, 1) #101-113, 201-213, 301-313, 401-413
        #now randomly reorder them
        self.pile=random.sample(self.pile,52) 
    def draw(self):
        return self.pile.pop()
    
#><><><><><><><#
# player class #
#><><><><><><><#
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
            return False
        else:
            self.chips-=minusChips
            return True
    def fold(self):
        self.gamesIn=[]
    def reset(self):
        self.hits=[False,False,False,False,False] #flop flop flop turn river
        self.cards=[] #own own [flop flop flop turn river]
        self.gamesIn=['Holdem High','Holdem Low','BlackJack','LowBall']
    def isIn(self,activeGames):
        #first order of business is to update games player is still in based on active games
        newGamesIn=[]
        for i in range(len(self.gamesIn)):
            if self.gamesIn[i] in activeGames:
                newGamesIn.append(self.gamesIn[i])
        self.gamesIn=newGamesIn
        return len(self.gamesIn)>0 #return true if still in any games
    def addCards(self,newCards):
        self.cards.extend(newCards)
    def numberCards(self):
        return len(self.cards)
    def setHits(self,hitList):
        for i in range(len(self.hits)):
            #set hit for entry i if either already hit OR specify hit  
            self.hits[i]=self.hits[i] or hitList[i]
    def getBJTotal(self):
        hasAce=False
        totals=[0]
        for i in range(len(self.cards)):
            if value(self.cards[i])==1: #if ace
                hasAce=True
            totals[0]+=min(value(self.cards[i]),10)
        if hasAce and totals[0] <= 11:
            totals.append(totals[0]+10)
        if min(totals)>21: #if bust in blackjack
            totals=[0] #set to lowest value
            self.gamesIn=diffList(self.gamesIn,['BlackJack']) #and remove BJ from list
        return totals
    def getLBTotal(self):
        subtotal=0
        total = [len(self.cards)]
        for i in range(len(self.cards)):
            subtotal+=min(value(self.cards[i]),10)
        if subtotal>30: #if bust in lowball
            total[0]=0 #set number of cards to lowest value
            self.gamesIn=diffList(self.gamesIn,['LowBall']) #and remove LB from list
        total.append(subtotal) #update total to reflect changes
        return total
    def getHoldemTotal(self,commonCards):
        #create variable to house both own cards and all common cards
        allCards=self.cards[0:1]+commonCards
        total=[]
        
        

##################################################################
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
        player[i].addCards([deck.draw(),deck.draw()])
        print('Cards for',player[i].name)
        print('  ',cardName(player[i].cards[0]))
        print('  ',cardName(player[i].cards[1]))
    ##TEMP CODE
    #game.activeGames=diffList(game.activeGames,['Holdem High','Holdem Low'])
    ##/TEMP CODE
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
        #get hits for each player
        for i in range(len(player)):
            ##TEMP CODE
            #print('Active games are: ',game.activeGames)
            #print('Games player is in: ',player[i].gamesIn)
            ##/TEMP CODE
            #if the player is not in any active games besides holdem hi/lo, then skip player
            if not player[i].isIn(diffList(game.activeGames,['Holdem High','Holdem Low'])):
                break
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
        for i in range(len(player)):
            #add hit cards to hands
            player[i].addCards(andList(game.activeCards,player[i].hits,game.common))
            #get totals for each player
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

    print('Hand over')
    if 'y' not in input(' Play another hand? y/n: '):
        break
