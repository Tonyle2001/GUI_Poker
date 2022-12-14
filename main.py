import PySimpleGUI as sg
import random
from deck import User
from deck import Deck

#The intial page for the user to enter their name and playing amount.
index_layout = [
    [sg.Text("Enter Username:",size =(18, 1)),sg.InputText(key = '-username-')],
    [sg.Text("Enter Amount To Play:",size =(18, 1)), sg.InputText(key = '-balance-')],
    [sg.Submit(),sg.Cancel()]
]

window = sg.Window("Poker", index_layout)
computer = User("Computer", 0)

#This while loop will open and prompt the user for their name and balance
while True:
    event, values = window.read()
    if event == "Cancel" or event == sg.WIN_CLOSED:
        window.close()

    if event == "Submit":
        name2 = values["-username-"]
        balance = values["-balance-"]
        player = User(name2, balance)
        window.close()
        break

#The bet amount that will be displayed for both computer and player
money = 100

#The game page of what the playing table will look like.
game_layout = [
     [sg.Text(computer.display_name())],
    [sg.Image('resources/card_back.png', key = '-Hand1-'), sg.Image('resources/card_back.png', key = '-Hand2-'), sg.Image('resources/card_back.png', key = '-Hand3-')],
    [sg.Text("Bet Amount: $100", key = '-Bet2-'), sg.Text("", key = '-Match-')],
    [sg.Text("Bet Amount: $100", key = '-Bet1-'), sg.Text("", key = '-Bet-')],
    [sg.Button("Flip", key = '-Flip-'),sg.Button("Raise", key = '-Raise-'),sg.Text( "$" + str(money), key = '-Money-'),sg.Button("+", key = '-Plus-'),sg.Button("-", key = '-Minus-')],
    [sg.Button('Play!', key = '-Play-'),sg.Button('Fold', key = '-Fold-'),sg.Text("", key = '-Results-')],
    [sg.Image('resources/card_back.png', key = '-Hand4-'), sg.Image('resources/card_back.png', key = '-Hand5-'), sg.Image('resources/card_back.png', key = '-Hand6-')],
    [sg.Text(player.display_name() + " $"), sg.Text(player.display_balance(), key = '-Balance-'), sg.Exit()]
]
# #The exit page after the user exit/loses the game.
# exit_layout = [
#     [sg.Text("Thank You")],
#     [sg.Text(player.display_name()+ " For Playing!")],
#     [sg.Text("Your Ending Balance: $"+ str(player.display_balance()))]
# ]
# Create the window
window = sg.Window("Poker", game_layout, size = (400,400))

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "Cancel" or event == sg.WIN_CLOSED:
        break


    #These will control the inc and dec of the raise amount
    if event == '-Plus-':
        money += 100
        window['-Money-'].update("$" + str(money))
    if event == '-Minus-' and money != 0:
        money -= 100
        window['-Money-'].update("$" + str(money))



    #When they click raise, game will decide who won
    if event == '-Raise-':
        #switch the last card for the computer and player
        if False == computer.display_result():
            window['-Hand3-'].update('resources/deck/' + player.sub_hand() + '.png')
            window['-Hand6-'].update('resources/deck/' + computer.sub_hand() + '.png')
            window['-Play-'].update('Play Again!')
        else:
            window['-Hand3-'].update('resources/deck/' + computer.sub_hand() + '.png')
            window['-Hand6-'].update('resources/deck/' + player.sub_hand() + '.png')
            window['-Play-'].update('Play Again!')

        window['-Match-'].update("I Match You!")
        window['-Bet-'].update("I Raise You!")
        window['-Bet1-'].update("Bet Amount: $" + str(money))
        window['-Bet2-'].update("Bet Amount: $"+ str(money))
        #If they won
        if player.display_result():
            window['-Balance-'].update(player.change_balance(money))
            window['-Results-'].update("You won!")
            money = 100
            window['-Money-'].update("$100")

        #If they lost
        else:
            window['-Balance-'].update(player.change_balance(-1*money))
            window['-Results-'].update("You Lost!")
            money = 100
            window['-Money-'].update("$100")

    # When they click flip, game will decide who won
    if event == '-Flip-':
        #switch the last card for the computer and player
        if False == computer.display_result():
            window['-Hand3-'].update('resources/deck/' + player.sub_hand() + '.png')
            window['-Hand6-'].update('resources/deck/' + computer.sub_hand() + '.png')
            window['-Play-'].update('Play Again!')
        else:
            window['-Hand3-'].update('resources/deck/'+computer.sub_hand()+'.png')
            window['-Hand6-'].update('resources/deck/'+player.sub_hand()+'.png')
            window['-Play-'].update('Play Again!')

        # If they won
        if player.display_result():
            window['-Balance-'].update(player.change_balance(money))
            window['-Results-'].update("You won!")
            money = 100
            window['-Money-'].update("$100")

        # If they lost
        else:
            window['-Balance-'].update(player.change_balance(-1 * money))
            window['-Results-'].update("You Lost!")
            money = 100
            window['-Money-'].update("$100")
    #if they fold, they will just lose $100
    if event == '-Fold-':
        window['-Hand3-'].update('resources/deck/' + computer.sub_hand() + '.png')
        window['-Hand6-'].update('resources/deck/' + player.sub_hand() + '.png')
        window['-Play-'].update('Play Again!')

        window['-Balance-'].update(player.change_balance(-1 * money))
        window['-Results-'].update("You Gave Up!")
        money = 100
        window['-Money-'].update("$100")

    #This will start and countine the game for user
    if event == '-Play-':
        deck = Deck()
        deck.shuffle()
        deck.shuffle()

        #clears the hand of the players before starting a new round
        computer.clear_hand()
        player.clear_hand()

        #Add 3 new cards for each player
        computer.add_hand(deck)
        computer.add_hand(deck)
        computer.add_hand(deck)
        player.add_hand(deck)
        player.add_hand(deck)
        player.add_hand(deck)

        #Using the evaluator functions made in the User class to determine who wins
        p_points = player.hand_eval()
        c_points = computer.hand_eval()
        #Cheating algorithm to make the player less probable of winning
        chance = random.randint(1,10)
        print(chance)
        #DEBUGGING CODE
        # print("Before = Player hand: "+ str(player.hand_eval()) + str(player.show_hand()))
        # print("Before = Computer hand: " +str(computer.hand_eval()) + str(computer.show_hand()))
        #This while loop will determine ties
        spot = 1
        while c_points == p_points and spot > -1 :
            c_points += computer.tie_break(spot)
            p_points += player.tie_break(spot)
            spot -=1

        if c_points < p_points and chance < 5:
            #player win
            player.change_result(True)
            computer.change_result(True)
        elif c_points > p_points:
            computer.change_result(True)
            player.change_result(False)
        else:
            window['-Hand1-'].update('resources/deck/' + player.sub_hand() + '.png')
            window['-Hand2-'].update('resources/deck/' + player.sub_hand() + '.png')
            window['-Hand3-'].update('resources/card_back.png')
            window['-Hand4-'].update('resources/deck/' + computer.sub_hand() + '.png')
            window['-Hand5-'].update('resources/deck/' + computer.sub_hand() + '.png')
            window['-Hand6-'].update('resources/card_back.png')

            computer.change_result(False)
            player.change_result(False)



        if computer.display_result():
            window['-Hand1-'].update('resources/deck/'+computer.sub_hand()+'.png')
            window['-Hand2-'].update('resources/deck/'+computer.sub_hand()+'.png')
            window['-Hand3-'].update('resources/card_back.png')
            window['-Hand4-'].update('resources/deck/'+player.sub_hand()+'.png')
            window['-Hand5-'].update('resources/deck/'+player.sub_hand()+'.png')
            window['-Hand6-'].update('resources/card_back.png')

        window['-Results-'].update("")

        window['-Match-'].update("")
        window['-Bet-'].update("")
        window['-Bet1-'].update("Bet Amount: $100")
        window['-Bet2-'].update("Bet Amount: $100")

    if event == "Exit" or player.display_balance() <= 0:
        # The exit page after the user exit/loses the game.
        exit_layout = [
            [sg.Text("Thank You")],
            [sg.Text(player.display_name() + " For Playing!")],
            [sg.Text("Your Ending Balance: $" + str(player.display_balance()))]
        ]
        window.close()
        window = sg.Window("Poker", exit_layout)
        window.read()

window.close()
