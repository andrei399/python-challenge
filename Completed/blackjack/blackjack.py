import random
from colorama import init
init()
from colorama import Fore, Style

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9,
          'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
    def __str__(self):
        return self.rank + ' of ' + self.suit

class Deck:
    def __init__(self):
        self.all_cards = []
        for suit in suits:
            for rank in ranks:
                self.all_cards.append(Card(suit, rank))
    def shuffle(self):
        if len(self.all_cards) > 0:
            random.shuffle(self.all_cards)
        else:
            print('The deck has been emptied, getting a new deck and shuffling it.')
            for suit in suits:
                for rank in ranks:
                    self.all_cards.append(Card(suit, rank))
            random.shuffle(self.all_cards)

    def deal_one(self):
        return self.all_cards.pop()

class Player:
    def __init__(self, name, card1, card2):
        self.name = name
        self.player_cards = [card1.rank , card2.rank]
        if card1.rank == 'Ace' and card2.rank == 'Ace':
            self.player_cards = ['Ace1', 'Ace1']
            self.card_score = 2
        else: self.card_score = card1.value + card2.value
        self.money = 500
        self.money = int(self.money)
        self.score = [0, 0, 0]
    def bet(self, amount):
        if self.money < amount:
            #Only happens when you go ALL-IN
            self.money = 0
        else:
            self.money -= amount
        self.money = int(self.money)
        print(f"You placed a bet of: ${int(amount)}")
    def win(self, amount):
        self.money = self.money + 2*amount
        self.money = int(self.money)
        self.money = int(self.money)
        self.score[0] += 1
        print(Fore.GREEN + f"You won! Your balance is now: ${self.money}" + Fore.WHITE)
    def lose(self):
        self.score[2] += 1
        print(Fore.RED + f"You lost :(. Your balance is now: ${self.money}" + Fore.WHITE)
    def draw(self, amount):
        self.money += amount
        self.money = int(self.money)
        self.score[1] += 1
        print(Fore.PURPLE + f"You drew! Your balance is now: ${self.money}" + Fore.WHITE)
    def hit(self, card):
        if self.card_score + card.value > 21 and 'Ace' in self.player_cards:
            self.card_score = self.card_score - 10 + card.value
            self.player_cards.remove('Ace')
            self.player_cards.append('Ace1')
        else:
            self.card_score += card.value
            self.player_cards.append(card.rank)
    def print_cards(self):
        printed_cards = ''
        for card in self.player_cards:
            if card != 'Ace1': printed_cards += ', ' + card
            else: printed_cards += ', ' + 'Ace'
        printed_cards = printed_cards[2:]
        print(f"{self.name} currently has these cards: {printed_cards}. {self.name}'s score is " + Fore.CYAN + f"{self.card_score}" + Fore.WHITE)
    def new_start(self, card1, card2):
        self.player_cards = [card1.rank , card2.rank]
        self.card_score = card1.value + card2.value

    def __str__(self):
        return f"{self.name} currently has " + Fore.GREEN + f"{self.score[0]} wins" + Fore.YELLOW + f", {self.score[1]} draws," + Fore.RED + f" {self.score[2]} loses!" + Fore.WHITE


def main():
    winnings = 500
    the_deck = Deck()
    the_deck.shuffle()
    player = Player(name = 'Andrei', card1 = the_deck.deal_one(), card2 = the_deck.deal_one())
    dealer = Player(name = 'Dealer', card1 = the_deck.deal_one(), card2 = the_deck.deal_one())
    while player.money > 0:
        allin = False
        if player.money > winnings: winnings = player.money
        player.print_cards()
        print("The dealer's card is: ", dealer.player_cards[0])
        bet = input("How much do you want to bet? ")
        if bet == 'leave':
            print('Alright, I hope you enjoyed your stay!')
            if player.money < 500: print(Fore.RED + f"You left the casino with a ${500 - player.money} loss." + Fore.WHITE)
            elif player.money == 500: print("You left the casino breaking even")
            elif player.money != winnings: print(Fore.GREEN + f"You left the casino with ${player.money - 500} in winnings" + Fore.RED + ", but you lost ${winnings - player.money} due to greed" + Fore.WHITE)
            else: print(Fore.GREEN + f"You left the casino with ${player.money} winning ${winnings - 500}!" + Fore.WHITE)
            break
        elif bet == 'balance':
            print(Fore.MAGENTA + f"You currently have ${player.money}" + Fore.WHITE)
            continue
        elif bet.isnumeric():
            bet = int(bet)
            if bet == player.money:
                allin = True
                print(Fore.YELLOW + "YOU WENT ALL IN! I like it, I'll give you 1.1x your bet amount because I like your balls." + Fore.WHITE)
                bet = player.money*1.1
        else:
            print (Fore.RED + "Sorry, I didn't understand you." + Fore.RED)
            continue
        if bet > player.money and allin == False:
            print(f"You don't have enough money to bet ${bet}, your balance is: ${player.money}, because of this mistake you now have to go all-in!")
            bet = player.money
        player.bet(bet)
        while player.card_score <= 21:
            hit_or_stand = input("Do you want to hit or stand? ")
            if hit_or_stand == 'hit':
                player.hit(the_deck.deal_one())
                player.print_cards()
            elif hit_or_stand == 'stand':
                break
            else:
                print('Sorry I did not understand! Please repeat')
        if player.card_score > 21:
            dealer.print_cards()
            player.lose()
        else:
            while dealer.card_score <= player.card_score and dealer.card_score < 21:
                dealer.hit(the_deck.deal_one())
                dealer.print_cards()
            if dealer.card_score > 21:
                if player.card_score == 21 and len(player.player_cards) == 2:
                    player.win(bet*1.5)
                    print(Fore.GREEN + "\033[1m" + Style.BRIGHT + "Damn, you won a natural! That means you get 1.5 times the money you bet!" + "\033[0;0m" + Style.RESET_ALL)
                else:
                    player.win(bet)
            elif dealer.card_score == player.card_score:
                player.draw(bet)
            else:
                player.lose()
        player.new_start(card1 = the_deck.deal_one(), card2 = the_deck.deal_one())
        dealer.new_start(card1 = the_deck.deal_one(), card2 = the_deck.deal_one())
        print(player)
        if winnings >= 100000:
            print(Fore.GREEN + "\033[1m" + Style.BRIGHT + 'You left the casino bankrupt from all the winnings' + "\033[0;0m" + Style.RESET_ALL)
            break
    if player.money == 0:
        if winnings != 500: print(Fore.RED + f'You left the casino losing $500 and another ${winnings - 500} in winnings.' + Fore.WHITE)
        else: print(Fore.RED + f'You left the casino losing $500' + Fore.WHITE)
    exit(0)


if __name__ == '__main__':
    main()
