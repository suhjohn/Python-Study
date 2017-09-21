from functions import play_game, buy_item
from friends import send_message

def turn_on():
    print('= Turn on game =')

    while True:
        choice = input('what would you like to do?\n')
        if choice=='0':
            break
        elif choice=='1':
            buy_item()
        elif choice=='2':
            play_game()
        elif choice=='3':
            send_message()
        else:
            print('Choice not exist')

        print('------------------------')
    print('=Turn off game=')

if __name__=="__main__":
    turn_on()
