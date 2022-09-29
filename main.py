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
    [sg.Text(player.display_name()), sg.Text(player.display_balance(), key = '-Balance-'), sg.Exit()]
]
#The exit page after the user exit/loses the game.
exit_layout = [
    [sg.Text("Thank You")],
    [sg.Text(player.display_name()+ " For Playing!")]
]
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
    if event == '-Flip-' or event == '-Fold-':
        window['-Hand3-'].update('resources/deck/'+computer.sub_hand()+'.png')
        window['-Hand6-'].update('resources/deck/'+player.sub_hand()+'.png')
        window['-Play-'].update('Play Again!')

        # If they won
        if player.display_result() and event == '-Flip-':
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

    #This will start and countine the game for user
    if event == '-Play-':
        deck = Deck()
        computer.add_hand(deck)
        computer.add_hand(deck)
        computer.add_hand(deck)
        player.add_hand(deck)
        player.add_hand(deck)
        player.add_hand(deck)

        chance = random.randint(1,10)
        print(chance)
        if computer.hand_eval() < player.hand_eval() and chance < 4:
            #player win
            player.change_result(True)
        else:
            #player lose
            player.hand.append(computer.hand.pop())
            player.hand.append(computer.hand.pop())
            player.hand.append(computer.hand.pop())
            computer.hand.append(player.hand.pop(0))
            computer.hand.append(player.hand.pop(0))
            computer.hand.append(player.hand.pop(0))
            player.change_result(False)

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
        window.close()
        window = sg.Window("Poker", exit_layout)
        window.read()

window.close()
