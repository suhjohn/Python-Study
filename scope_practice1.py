champion = "Lux"

def show_global_champion():
    print('show_global_champion : {}'.format(champion))

def change_global_champion():
    champion = "ahri"
    print('before change_global_champion : {}'.format(champion))
    print('after change_global_champion : {}'.format(champion))

print(globals())

show_global_champion()
change_global_champion()
