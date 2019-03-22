import numpy as np

# Global definitions
NUM_CARDS_IN_A_DECK = 52
NUM_CARDS_IN_A_SUIT = 13
MAX_DECKS = 10


class Card:
    def __init__(self, card_key):
        self.value = (card_key - 1) % NUM_CARDS_IN_A_DECK

        suit_idx = np.floor(self.value / NUM_CARDS_IN_A_SUIT)
        suit_map = {
            0: "Spades",
            1: "Hearts",
            2: "Clubs",
            3: "Diamonds",
        }
        self.suit = suit_map.get(suit_idx, "Error")
        self.value = (self.value % NUM_CARDS_IN_A_SUIT) + 1

    def get_value(self):
        return self.value

    def get_suit(self):
        return self.suit

    def print_card(self):
        if self.value == 1:
            print("Ace of {}".format(self.suit))
        elif self.value == 11:
            print("Jack of {}".format(self.suit))
        elif self.value == 12:
            print("Queen of {}".format(self.suit))
        elif self.value == 13:
            print("King of {}".format(self.suit))
        else:
            print("{} of {}".format(self.value, self.suit))


class BlackjackDeck:
    def __init__(self, num_decks):
        if num_decks > MAX_DECKS:
            print("Number of decks limited to 10 in dealer deck")
            self.deck_size = NUM_CARDS_IN_A_DECK * MAX_DECKS
        else:
            print("Playing with {} decks".format(num_decks))
            self.deck_size = NUM_CARDS_IN_A_DECK * num_decks

        # Create a deck of cards and shuffle it
        self.cards = np.arange(1, self.deck_size)
        np.random.shuffle(self.cards)

    def draw(self):
        idx_to_draw = np.random.randint(0, self.cards.size)
        card_key = self.cards[idx_to_draw]
        self.cards = np.delete(self.cards, idx_to_draw)
        print("Drew a...")
        Card(card_key).print_card()
        print("{} cards remaining in deck".format(self.cards.size))

        return card_key

    # Note that shuffling assumes all cards added back to deck
    def shuffle(self):
        print("Reshuffling the deck")
        self.cards = np.arange(1, self.deck_size)
        np.random.shuffle(self.cards)


class Hand:
    def __init__(self, player_id):
        self.cards = np.array([])
        self.player_id = player_id

    def reshuffle_hand(self):
        self.cards = np.array([])

    def add_card(self, card_key):
        card = Card(card_key)
        print("Adding card to hand:")
        card.print_card()
        self.cards = np.append(self.cards, card)

    def get_player_id(self):
        return self.player_id

    def get_shown_score(self):
        score = 0
        aces = 0
        for card in self.cards:
            val = card.get_value()
            if val == 1:
                aces += 1
            elif val == 11 or val == 12 or val == 13:
                score += 10
            else:
                score += val

        score += aces
        if score > 21:
            print("Player {} busted with score of at least {}".format(self.player_id, score))
        elif score <= 11:
            while score <= 11 and aces > 0:
                score += 10
                aces -= 1

        return score

    def print_shown_cards(self):
        print("Player {} is holding:".format(self.player_id))
        for card in self.cards:
            if card.get_value() == 11:
                print("A Jack of {}".format(card.get_suit()))
            elif card.get_value() == 12:
                print("A Queen of {}".format(card.get_suit()))
            elif card.get_value() == 13:
                print("A King of {}".format(card.get_suit()))
            elif card.get_value() == 1:
                print("An Ace of {}".format(card.get_suit()))
            else:
                print("A {} of {}".format(card.get_value(), card.get_suit()))


class DealerHand(Hand):
    def __init__(self, player_id):
        self.cards = np.array([])
        self.player_id = player_id
        self.hidden_card = np.array([])

    def add_hidden_card(self, card_key):
        self.hidden_card = np.append(self.hidden_card, Card(card_key))

    def get_total_score(self):
        aces = 0
        score = 0
        val = self.hidden_card[0].get_value()
        if val == 1:
            aces += 1
        elif val == 11 or val == 12 or val == 13:
            score += 10
        else:
            score += val

        for card in self.cards:
            val = card.get_value()
            if val == 1:
                aces += 1
            elif val == 11 or val == 12 or val == 13:
                score += 10
            else:
                score += val

        score += aces
        if score > 21:
            print("Dealer busted with score of at least {}".format(score))
        elif score <= 11:
            while score <= 11 and aces > 0:
                score += 10
                aces -= 1

        return score

    def print_hidden_card(self):
        card = self.hidden_card[0]
        if card.get_value() == 11:
            print("Dealer is holding a face down Jack of {}".format(card.get_suit()))
        elif card.get_value() == 12:
            print("Dealer is holding a face down Queen of {}".format(card.get_suit()))
        elif card.get_value() == 13:
            print("Dealer is holding a face down King of {}".format(card.get_suit()))
        elif card.get_value() == 1:
            print("Dealer is holding a face down Ace of {}".format(card.get_suit()))
        else:
            print("Dealer is holding a face down %d of {}".format(card.get_value(), card.get_suit()))


def run_game():
    print("Let's play a new game of blackjack!")

    n_players = int(raw_input("How many players do you want to play with?"))
    n_decks = int(raw_input("How many decks do you want to play with?"))

    print("Shuffling a new deck...")
    deck = BlackjackDeck(n_decks)
    deck.shuffle()

    player_hands = []
    for player in range(0, n_players):
        player_hands.append(Hand(player))

    dealer_hand = DealerHand(n_players + 1)

    # While the player wants to continue playing
    play_the_game = True
    while play_the_game:
        # Start by dealing
        for i in range(0, 2):
            for player in range(0, n_players):
                player_hands[player].reshuffle_hand()
                card_key = deck.draw()
                player_hands[player].add_card(card_key)

        dealer_hand.reshuffle_hand()
        card_key = deck.draw()
        dealer_hand.add_hidden_card(card_key)
        card_key = deck.draw()
        dealer_hand.add_card(card_key)

        player_scores = []
        players_alive = n_players
        for player in range(0, n_players):
            player_scores.append(0)
            print("Starting turn for player {}".format(player))
            player_hands[player].print_shown_cards()
            player_scores[player] = player_hands[player].get_shown_score()
            print("Current score for player {} is {}".format(player, player_scores[player]))

            continue_turn = True
            while continue_turn:
                x = raw_input("Player {}, would you like a hit (y/n)?".format(player))
                if x == 'y':
                    continue_turn = True
                    card_key = deck.draw()
                    player_hands[player].add_card(card_key)
                    player_scores[player] = player_hands[player].get_shown_score()
                    if player_scores[player] <= 21:
                        print("Current score for player {} is {}".format(player, player_scores[player]))
                    else:
                        print("Player busted, ending turn for player {}".format(player))
                        continue_turn = False
                        players_alive -= 1
                else:
                    continue_turn = False

        if players_alive > 0:
            print("Starting dealer's turn")
            print("Dealer reveals hidden card...")
            dealer_hand.print_hidden_card()
            score = dealer_hand.get_total_score()
            print("Current score for dealer is {}".format(score))
            while score < 17:
                print("Score is less than 17.  Dealer hit.")
                card_key = deck.draw()
                dealer_hand.add_card(card_key)
                score = dealer_hand.get_total_score()
            if score > 21:
                print("Dealer busted!")
            else:
                print("Dealer score is {}".format(score))
                for player in range(0, n_players):
                    print("Player {} score: {}".format(player, player_scores[player]))

        x = raw_input("Would you like to keep playing? (y/n)")
        if x == 'y':
            play_the_game = True
        else:
            play_the_game = False


if __name__ == '__main__':
    run_game()