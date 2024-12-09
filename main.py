import random


# Calculate the value of a hand
def calcHandVal(hand):
    val = 0
    aceCount = 0
    for card in hand:
        if card in ('J', 'Q', 'K'):
            val += 10
        elif card == 'A':
            aceCount += 1
            val += 11
        else:
            val += int(card)
    while val > 21 and aceCount > 0:
        val -= 10
        aceCount -= 1
    return val


# Show hands
def showHands(playerHands, dealerHand, hideDealerCard=True):
    handIndex = 0
    for hand in playerHands:
        print(f"\nYour hand {handIndex + 1 if len(playerHands) > 1 else ''}: {hand} val: {calcHandVal(hand)}")
        handIndex += 1
    if hideDealerCard:
        print(f"Dealer's hand: ['[?]', '{dealerHand[1]}']")
    else:
        print("Dealer's hand:", dealerHand, "val:", calcHandVal(dealerHand))


# Main function
def blackjack(money):
    deck = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'] * 4
    random.shuffle(deck)
    index = 0

    # Get bet
    while True:
        try:
            bet = float(input(f"You have ${money:.2f}. Enter your bet: "))
            if bet <= 0:
                print("Bet amount must be greater than $0. Try again.")
            elif bet > money:
                print("You don't have enough money to make that bet. Try again.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    # Deal hands
    playerHands = [[deck[index], deck[index + 1]]]
    dealerHand = [deck[index + 2], deck[index + 3]]
    index += 4

    # Handle splits
    for _ in range(3):
        newHands = []
        for hand in playerHands:
            if len(hand) == 2 and hand[0] == hand[1] and bet <= (money / 2):
                split = input(f"Your hand {hand} can be split. Split? (yes/no): ").lower()
                if split == 'yes':
                    if money < bet:
                        print("You don't have enough money to split.")
                    else:
                        money -= bet
                        print("Splitting your hand!")
                        newHands.append([hand.pop(0), deck[index]])
                        index += 1
                        hand.append(deck[index])
                        index += 1
        playerHands.extend(newHands)

    # Play hands
    for hand in playerHands:
        print(f"\nPlaying hand:")
        doubleDown = False
        while True:
            showHands([hand], dealerHand, hideDealerCard=True)
            handVal = calcHandVal(hand)
            if handVal > 21:
                break

            choice = input("Do you want to 'hit', 'stand', or 'double down'? ").lower()

            if choice == 'hit':
                hand.append(deck[index])
                index += 1
            elif choice == 'stand':
                break
            elif choice == 'double down':
                if money >= bet * 2:
                    doubleDown = True
                    bet *= 2
                    hand.append(deck[index])
                    index += 1
                    break
                else:
                    print("You don't have enough money to double down!")
            else:
                print("Invalid input. Type 'hit', 'stand', or 'double down'.")

    if doubleDown and calcHandVal(hand) > 21:
        print("You bust after doubling down!")

    if handVal <= 21:
        while calcHandVal(dealerHand) < 17:
            dealerHand.append(deck[index])
            index += 1

    # Show results
    showHands(playerHands, dealerHand, hideDealerCard=False)
    dealerVal = calcHandVal(dealerHand)
    for hand in playerHands:
        handVal = calcHandVal(hand)
        if handVal > 21:
            print("You bust! Dealer wins.")
            money -= bet
            continue
        elif dealerVal > 21 or handVal > dealerVal:
            print("You win this hand!")
            money += bet
        elif handVal == 21 and len(hand) == 2:
            print("You hit BLACKJACK!")
            money += (bet * 1.5)
        elif handVal < dealerVal:
            print("Dealer wins this hand!")
            money -= bet
        else:
            print("This hand is a push!")

    return money


# Running the program
print("Welcome to Blackjack!")
while True:
    try:
        money = int(input("Enter your buy-in amount (minimum $5): "))
        if money < 5 or money > 10000:
            print("Buy-in must be at least $5 or maximum $10,000. Try again.")
        else:
            break
    except ValueError:
        print("Invalid input. Please enter a valid number.")

while money > 0:
    money = blackjack(money)
    print(f"\nYour current money is: ${money:.2f}")
    if money <= 0:
        print("You are broke! Game over.")
        break
    try:
        playAgain = input("Do you want to play again? (yes/no): ").lower()
        if playAgain == 'yes':
            print(f"\nYou are starting the next round. Good luck!")
        elif playAgain == 'no':
            print(f"You are leaving the game with ${money:.2f}. Thanks for playing!")
            break
        else:
            break
    except ValueError:
        print("Invalid input. Please enter yes or no.")
