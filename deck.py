import random

class Card:
    def __init__(self, val, suit):
        self.value = val
        self.suit = suit
        self.card = val + suit

    def show_card(self):
        return self.card

    def show_val(self):
        house = {'T': '10','J':'11','Q':'12','K':'13','A':'14'}
        if self.value in ['T','J','Q','K','A']:
            return house.get(self.value)

        return self.value
    def show_suit(self):
        return self.suit

class Deck:
    def __init__(self):
        self.deck = []
        self.build()
        #make a boolean self

    #build a def to check the deck and rebuild if not full!!!!!

    def build(self):
        for v in ['2','3','4','5','6','7','8','9','J','Q','K','A','T']:
            for s in ['s','c','d','h']:
                self.deck.append(Card(v,s))

    def clear(self):
        self.clear()
        self.build()

    def check_deck(self):
        count = 0
        for i in self.deck:
            #print(i.show())
            count += 1

        return count
    #not needed
    def shuffle(self):
        for i in(len(self.deck)-1, 0, -1):
            r = random.randint(0, 51)
            self.deck[i], self.deck[r] = self.deck[r], self.deck[i]


    def show_deck(self):
        for i in self.deck:
            print(i.show_card())

    def draw_card(self):
        r = random.randint(0,len(self.deck) - 1)
        return self.deck.pop(r)



    def return_card(self):
        self.deck.append(User.sub_hand())

    # function that will add a specific card to hand
    # def cheat_card(self, Card):
    #     return self.deck.pop(self.deck.index(Card))

    # def cheat_card(self, val, suit):
    #     index = 0
    #     # for i in range(self.check_deck() - 1):
    #     #     if self.deck(i) == (val+suit):
    #     #         index = i
    #
    #     User.hand.append(deck.pop(deck.index(val+suit)))





class User:

    def __init__(self, name, balance):
        self.name = name
        self.balance = int (balance)
        self.result = False
        self.hand = []

    def change_result(self, boolean):
        self.result = boolean
    def display_result(self):
        return self.result
    def display_name(self):
        return self.name


    def display_balance(self):
        return self.balance


    def change_balance(self, amount):
        total = self.balance
        total += amount
        self.balance = total
        return self.balance

    def add_hand(self,game):
        self.hand.append(game.draw_card())

    def sub_hand(self):
        val = '' + self.hand.pop().show_card()
        return val

    def show_hand(self):
        orig = ""
        for i in self.hand:
            orig += str(i.show_card()) + ","
        split = orig.split(",")
        split.pop()
        return split

    #function that will add a specific card to hand
    def add_cheat_card(self,val, suit):
        self.hand.append(Card(val,suit))

    def hand_eval(self):
        #eval = {'high_card': 0, 'pair': 0, 'flush': 0, 'straight': 0, 'triple': 0, 'straight-flush': 0}
        if self.straight_flush():
            return 19 + self.high_card()
        elif self.triple():
            return 18 + self.high_card()
        elif self.straight():
            return 17 + self.high_card()
        elif self.flush():
            return 16 + self.high_card()
        elif self.pair():
            return 15 + self.high_card()
        else:
            return self.high_card()

    # check for straight-flush
    def straight_flush(self):
        if self.straight() and self.flush():
            #print("straightflush")
            return True
        return False
    # check for triple
    def triple(self):
        if self.hand[0].show_val() == self.hand[1].show_val() == self.hand[2].show_val():
            #print("triple")
            return True
        return False
    # check for straight
    def straight(self):
        straight = []
        for i in self.hand:
            straight.append(i.show_val())
        straight.sort()
        if int(straight[1]) - 1 == int(straight[0]) and int(straight[1]) + 1 == int(straight[2]):
            #print("straight")
            return True
        return False
    #check for flush
    def flush(self):
        if self.hand[0].show_suit() == self.hand[1].show_suit() == self.hand[2].show_suit():
            #print("flush")
            return True
        return False
    # check for pair
    def pair(self):
        if self.hand[0].show_val() == self.hand[1].show_val() or self.hand[0].show_val() == self.hand[2].show_val() or self.hand[1].show_val() == self.hand[2].show_val():
            #print("pair")
            return True
        return False
    #check for high card
    def high_card(self):
        high_card = []
        house = {10:'T',11:'J',12:'Q',13:'K',14:'A'}
        for i in self.hand:
            high_card.append(int(i.show_val()))
        #print(max(high_card))
        return max(high_card)






