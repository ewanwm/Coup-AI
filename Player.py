from Cards import *
import numpy as np

class Player:
    nPlayers = 0

    def __init__(self, nCards, playerName="", logger=None):
        if playerName == "":
            self.Name = "Player_" + str(Player.nPlayers)
            
        else: 
            self.Name = playerName

        self.logger = logger

        self.nCards = nCards

        self.Id = Player.nPlayers
        Player.nPlayers += 1

        self.reset()

    def reset(self):
        self.Coins = 2 ## start with 2 coins
        self.Cards = []
        self.CardStates = []
        self.isAlive = True
        self.rewardAccum = 0

    ## wrap the logger functions... must be a nicer way of doing this...
    def ERROR(self, *messages): 
        if self.logger != None: self.logger.error("{"+self.Name+"}", *messages)
    def WARN(self, *messages): 
        if self.logger != None: self.logger.warn("{"+self.Name+"}", *messages)
    def INFO(self, *messages): 
        if self.logger != None: self.logger.info("{"+self.Name+"}", *messages)
    def DEBUG(self, *messages): 
        if self.logger != None: self.logger.debug("{"+self.Name+"}", *messages)
    def TRACE(self, *messages): 
        if self.logger != None: self.logger.trace("{"+self.Name+"}", *messages)

    def giveCard(self, cardName):
        if not cardName in cards.keys():
            raise Exception("ERROR: Trying to give unknown card " + str(cardName) + " to player " + self.Name)

        if len(self.Cards) >= self.nCards:
            raise Exception("ERROR: trying to give player " + self.Name + " a card when they already have " + len(self.Cards) + " cards. Max num of cards is set to " + str(self.nCards))

        self.Cards.append(cardName)
        self.CardStates.append("Alive")

    def giveReward(self, reward):
        self.INFO("Giving reward:", reward)
        self.rewardAccum += reward
        self.DEBUG("  Reward after:", self.rewardAccum)

    def claimReward(self):
        ## return the reward for this player and reset it
        self.INFO("Claiming reward:",self.rewardAccum)
        ret = self.rewardAccum
        self.rewardAccum = 0.0
        return ret
    
    def checkReward(self):
        ## check how much reward this player has accumulated
        return self.rewardAccum

    def kill(self):
        self.INFO("AAARGH, I'm dead!")
        self.isAlive = False
        self.giveReward(-30)

    def takeCard(self, cardName):
        for i in range(self.nCards):
            if (self.CardStates[i] == "Alive") & (self.Cards[i] == cardName):
                self.Cards.pop(i)
                self.CardStates.pop(i)
                return
        
        raise Exception("ERROR: trying to take card", cardName, "away from player", self.Name, "but they do not have one that is alive")

    def checkCard(self, cardName):
        for i in range(self.nCards):
            if (self.CardStates[i] == "Alive") & (self.Cards[i] == cardName):
                return True

    def giveCoins(self, nCoins):
        self.Coins += nCoins

    def takeCoins(self, nCoins):
        if self.Coins - nCoins < 0:
            raise Exception("ERROR: trying to take " + str(nCoins) + " from player " + self.Name + " Who only has " + str(self.Coins))
        self.Coins = self.Coins - nCoins
    
    def loseInfluence(self, cardIdx):
        ## kill card with index cardIdx
        self.INFO("Losing influence. Card: ", self.Cards[cardIdx])
        self.cardStates[cardIdx] = "Dead"

        self.giveReward(-10)

    def loseInfluence(self):
        ## kill one of the players cards at random
        if np.all(np.array(self.CardStates) == "Dead"):
            raise Exception("ERROR: trying to make", self.Name, "lose influence but all their cards are already dead: ", self.__str__())
        
        aliveCards = np.where(np.array(self.CardStates) == "Alive")[0]
        cardIdx = np.random.choice(aliveCards)

        self.INFO("Losing influence. Card: ", self.Cards[cardIdx])
        self.CardStates[cardIdx] = "Dead"
        
        self.giveReward(-10)
    
    def __str__(self):
        retStr = "Name: " + self.Name + ", "
        retStr += "N Coins: " + str(self.Coins) + ", "
        retStr += "N Cards: " + str(len(self.Cards)) + ", "
        retStr += "Cards: {"
        for i, card in enumerate(self.Cards):
            retStr += card + ":" + self.CardStates[i][0] + ", "
        retStr += "}"

        return retStr