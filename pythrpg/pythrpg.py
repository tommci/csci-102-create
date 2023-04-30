            # BUGS RIGHT NOW:
    # 'Back' button randomly appears when encountering enemy. Sometimes it doesn't appear sometimes it does
    # Stick doesn't go away if it's ignored instead of being picked up

            # NOTES FOR NEXT TIME:
    # There's still some placeholder stuff in enemy encounters (see comments in that area)
    # Attack and guard buttons are mid development (still using print() statements to avoid errors)
    # Want to show enemy health, move player health, during battles
    # Need to give enemies XP values to level up the player (will probably be defined in game.enemies)
    # Probably should make enemy sprites larger since they're their own thing
    # boar2.png is a temporary file, not in use right now

from tkinter import *

import random

# ~~~~~~~~~~~~~ ~~~~~~~~~~~ ~~~~~~~~~~~~~
# ~~~~~~~~~~~~~ DEFINITIONS ~~~~~~~~~~~~~
# ~~~~~~~~~~~~~ ~~~~~~~~~~~ ~~~~~~~~~~~~~

tk = Tk(className=' PythRPG')   # Sets up tkinter, and names the window 'PythRPG' (everything tkinter related refers to 'tk' from here on)
tk.geometry("600x600")          # Sets the size of the window (width x height)

# Sky and Terrain images should be 400x200, items should be 50x50 or larger, enemies should be 150x150

    # Skies: 0 = Sunny, 1 = Cloudy, 2 = Raining
skies = [PhotoImage(file='sun.png'), PhotoImage(file='clouds.png'), PhotoImage(file='rain.png')]
currentsky = 0

    # Terrains: 0 = Grass, 1 = Road
grounds = [PhotoImage(file='grass.png'), PhotoImage(file='road.png')]
currentground = 0

    # World objects: 0 = None, 1 = Generic enemy check, 2 = Stick
objects = ['', '', PhotoImage(file='stick.png')]
worldobject = 0

    # Enemies: 0 = Boar
enemies = [PhotoImage(file='boar.png')]

    # If something is interactable in the enviro, set = 'y' otherwise set = 'n'
interactable = 'n'

def show_enviro(caninteract, incombat):
    menus.splashtext.destroy()
    game.sky.destroy()
    game.ground.destroy()
    game.enemysprite.destroy()
    menus.inventorybutton.destroy()
    menus.interactbutton.destroy()
    menus.movebutton.destroy()

    menus.splashtext = Label(tk, font=('Arial', 9, 'italic'), text=game.situation)
    menus.splashtext.place(relx=0.5, rely=0.86, anchor='s')

    if incombat == 'y':    # Enemy encounter
        game.enemysprite = Label(tk, image=enemies[game.enemy], borderwidth=0)
        game.enemysprite.place(relx=0.5, rely=0.5, anchor='center')

        combat.attackbutton = Button(tk, text='Attack', command=combat.attack)
        combat.attackbutton.place(relx=0.43, rely=0.97, anchor='s')

        combat.guardbutton = Button(tk, text='Guard', command=combat.guard)
        combat.guardbutton.place(relx=0.565, rely=0.97, anchor='s')

    if caninteract == 'y':
        menus.interactbutton = Button(tk, text='Interact', command=interact)
        menus.interactbutton.place(relx=0.5, rely=0.98, anchor='s')

    if incombat != 'y':                                           # None of this stuff appears if in combat
        game.sky = Label(tk, image=skies[currentsky])
        game.sky.place(relx=0.5, rely=0.32, anchor='center')       # Place sky at y 0.32 for 600x600

        game.ground = Label(tk, image=grounds[currentground])
        game.ground.place(relx=0.5, rely=0.65, anchor='center')    # Place ground at y 0.65 for 600x600
        
        menus.inventorybutton = Button(tk, text='Inventory', command=inven.open_inventory)
        menus.inventorybutton.place(relx=0.02, rely=0.98, anchor='sw')

        menus.movebutton = Button(tk, text='Move', command=game.advance)
        menus.movebutton.place(relx=0.98, rely=0.98, anchor='se')
    
    if worldobject > 1:     # Object
        game.object = Label(tk, image=objects[worldobject], borderwidth=0)
        game.object.place(relx=0.5, rely=0.63, anchor='center')


def interact():
    global interactable
    global worldobject
    menus.splashtext.destroy()

    if worldobject == 2:
        menus.splashtext = Label(tk, font=('Arial', 9, 'italic'), text='You pick up the stick off the ground.')
        menus.splashtext.place(relx=0.5, rely=0.86, anchor='s')
        game.object.destroy()
        menus.interactbutton.destroy()

        game.inventory[0].append('Stick')
        game.inventory[1].append('A simple stick. Better than your fists!')
        game.inventory[2].append(2)
        game.inventory[3].append('wep')

        game.situation = 'You picked up the stick off the ground.'
        worldobject = 0
        interactable = 'n'

# ~~~~~~~~~~~~~ ~~~~~~~ ~~~~~~~~~~~~~
# ~~~~~~~~~~~~~ CLASSES ~~~~~~~~~~~~~
# ~~~~~~~~~~~~~ ~~~~~~~ ~~~~~~~~~~~~~

class Gameplay:
    def __init__(self):
        # Inventory format: is List 0 is Item Name, List 1 is Description, List 2 is Damage/Defense (if wep/arm), List 3 is Type
        # Types: wep = weapon, arm = armor
        self.inventory = [[],[],[],[]]
        self.playerlevel = 1
        self.playerhealth = 100
        self.sky = Label(tk)        # Sky graphic
        self.ground = Label(tk)     # Ground graphic
        self.object = Label(tk)     # Object graphics
        # The following list is a list of possible situations to enter:
        # Situations 0 and 1 are pre-determined (intro)
        # Situation 2 is a random enemy
        # Situations 3-4 are weather
        # Situations 5-? involve road
        self.situationlist = ['You awaken in a grassy field on a sunny day.',
                              'As you wander, you come across a stick laying in the field.',
                              'enemy',      # Situation 2 (for reference)
                              'Clouds loom overhead.',
                              'Rain begins to fall from the sky. Your defense has been reduced.',
                              'You come across a road, and are unsure of where it leads.',
                              'The road is a dead end, and leads nowhere.',
                              'The road leads to a small village.']
        self.situation = self.situationlist[0]
        # Enemies format: List 1 is Name, List 2 is Health, List 3 is Damage
        self.enemies = [['Wild Boar', 'Wolf', 'Bear'],
                        [20, 40, 60],
                        [2, 5, 10]]
        # Enemy numbers: 0 is boar, 1 is wolf, 2 is bear
        self.enemy = 0
        self.enemysprite = Label(tk)    # Enemy graphics

    def advance(self):
        global worldobject
        global interactable
        global currentsky
        global currentground

        if self.situation == self.situationlist[0]:     # This is immediately after first screen, leads to stick on ground
            self.situation = self.situationlist[1]
            worldobject = 2
            interactable = 'y'
        else:
            if self.situation == self.situationlist[1]:
                self.object.destroy()
                menus.interactbutton.destroy()
            if random.randint(1, 4) == 1:               # Enemy encounter
                self.situation = self.situationlist[2]
                if random.randint(1, self.playerlevel) == 1:    # Choosing the enemy to appear (1 is boar)
                    self.enemy = 0
                    worldobject = 'y'
                    game.enemy_encounter()
                else:                                           # <---- THIS "ELSE" IS TEMPORARY
                    self.enemy = 1
                    worldobject = 'y'
                    game.enemy_encounter()

            elif random.randint(1,2) == 1:    # If no enemy encounter
                self.situation = self.situationlist[random.randrange(3,6,2)]    # randrange(3,6,2) returns 3 or 5 randomly, this chooses between road and weather change
                if self.situation == self.situationlist[3]:     # Weather change
                    currentsky = 1
                if self.situation == self.situationlist[5]:     # Road
                    currentground = 1

        show_enviro(interactable, worldobject)   # End of advance function

    def enemy_encounter(self):      # DON'T use show_enviro in here, since advance already does it
        self.situation = f'Look out! A {self.enemies[0][self.enemy]} is approaching!'

game = Gameplay()

class Combat:
    def __init__(self):
        self.attackbutton = Button(tk)      # Button that attacks on your turn
        self.guardbutton = Button(tk)       # Button that guards (raises defense) on your turn
        self.continuebutton = Button(tk)    # Button that allows player to continue after battle
        self.enemyhealth = Label(tk)        # Shows enemy health

    def attack(self):
        print()

    def guard(self):
        print()

combat = Combat()

class Inventory:
    def __init__(self):
        self.inventorysetup = ''                # Inventory setup: for assembling the inventory display
        self.equippedweapon = ['Fists', 1]      # Equipped weapon. Index 0 is name, index 1 is attack
        self.equippedarmor = ['Clothes', 1]     # Equipped armor. Index 0 is name, index 1 is defense
        self.inventorydisplay = Label(tk)       # What actually gets displayed in inventory
        self.inventoryselection = Entry(tk)     # Entry box to choose item to interact with in inventory
        self.equipment = Label(tk)              # Displays equipment and its stats (ATK, DEF)
        self.equipbutton = Button(tk)           # Equip item button
        self.dropbutton = Button(tk)            # Drop item button
        self.selection = 0                      # Item # selected using entry box (if a valid input is recieved)

    def open_inventory(self):
        self.inventorysetup = '_______________________________________________________________________\n\n'

        if self.selection != -1:          # If staying in the inventory (after dropping an item) the splashtext isn't deleted since it should say "you dropped item"
            menus.splashtext.destroy()
        self.selection = 0

        if game.inventory == [[],[],[],[]]:
            menus.splashtext = Label(tk, font=('Arial', 9, 'italic'), text='Your inventory is empty.')
            menus.splashtext.place(relx=0.5, rely=0.86, anchor='s')

        else:
            menus.movebutton.destroy()
            menus.inventorybutton.destroy()
            menus.interactbutton.destroy()
            self.equipment.destroy()
            game.sky.destroy()
            game.ground.destroy()

            for i in range(0, len(game.inventory[0])):
                self.inventorysetup += (f'{i+1})   {game.inventory[0][i]}    |        {game.inventory[1][i]}\n'
                                        '_______________________________________________________________________\n\n')

            self.inventorydisplay = Label(tk, text=self.inventorysetup, font=('Arial', 11))
            self.inventorydisplay.place(relx=0.02, rely=0.5, anchor='w')

            self.inventoryselection = Entry(tk, width=2, background='light grey')  
            self.inventoryselection.place(relx=0.5, rely=0.97, anchor='s')          

            self.equipbutton = Button(tk, text='Equip', command=self.equip)
            self.equipbutton.place(relx=0.43, rely=0.97, anchor='s')

            self.dropbutton = Button(tk, text='Drop', command=self.drop)
            self.dropbutton.place(relx=0.565, rely=0.97, anchor='s')

            self.equipment = Label(tk, text=f'WEAPON: {self.equippedweapon[0]}       ARMOR: {self.equippedarmor[0]}\n\nATK: {self.equippedweapon[1]}       DEF: {self.equippedarmor[1]}')
            self.equipment.place(relx=0.5, rely=0.02, anchor='n')

            self.backbutton = Button(tk, text='Back', command=menus.return_to_world)
            self.backbutton.place(relx=0.02, rely=0.98, anchor='sw')

    def equip(self):
        if (self.inventoryselection.get().isdigit() == True) and (int(self.inventoryselection.get()) <= len(game.inventory[0])) and (int(self.inventoryselection.get()) > 0):
            self.selection = int(self.inventoryselection.get()) - 1
            menus.splashtext.destroy()

            # Equip (game.inventory[3] is item type, [0] is weapon name, [2] is attack)
            # Equipping weapon
            if game.inventory[3][self.selection] == 'wep':

                if game.inventory[2][self.selection] == self.equippedweapon[1]:
                    menus.splashtext = Label(tk, font=('Arial', 9, 'italic'), text=f'You have already equipped the {self.equippedweapon[0]}.')
                    menus.splashtext.place(relx=0.5, rely=0.86, anchor='s')

                else:
                    self.equippedweapon = []
                    self.equippedweapon.append(game.inventory[0][self.selection])
                    self.equippedweapon.append(game.inventory[2][self.selection])

                    self.reload_equipment()

                    menus.splashtext = Label(tk, font=('Arial', 9, 'italic'), text=f'You equip the {self.equippedweapon[0]}.')
                    menus.splashtext.place(relx=0.5, rely=0.86, anchor='s')
            # Equipping armor
            elif game.inventory[3][self.selection] == 'arm':

                if game.inventory[2][self.selection] == self.equippedarmor[1]:
                    menus.splashtext = Label(tk, font=('Arial', 9, 'italic'), text=f'You have already equipped the {self.equippedarmor[0]}.')
                    menus.splashtext.place(relx=0.5, rely=0.86, anchor='s')

                else:
                    self.equippedarmor = []
                    self.equippedarmor.append(game.inventory[0][self.selection])
                    self.equippedarmor.append(game.inventory[2][self.selection])

                    self.reload_equipment()

                    menus.splashtext = Label(tk, font=('Arial', 9, 'italic'), text=f'You equip the {self.equippedarmor[0]}.')
                    menus.splashtext.place(relx=0.5, rely=0.86, anchor='s')

        else:   # Invalid input check
            menus.splashtext.destroy()
            menus.splashtext = Label(tk, font=('Arial', 9, 'italic'), text=f'Invalid selection.\nEnter the number corresponding to the item you want to equip.')
            menus.splashtext.place(relx=0.5, rely=0.86, anchor='s')

    def drop(self):
        if (self.inventoryselection.get().isdigit() == True) and (int(self.inventoryselection.get()) <= len(game.inventory[0])) and (int(self.inventoryselection.get()) > 0):
            self.selection = int(self.inventoryselection.get()) - 1
            menus.splashtext.destroy()

            # Below checks if the item being dropped is currently equipped or not
            if (game.inventory[2][self.selection] == self.equippedweapon[1]) or (game.inventory[2][self.selection] == self.equippedarmor[1]):

                if game.inventory[3][self.selection] == 'wep':      # Unequips weapon
                    self.equippedweapon = []
                    self.equippedweapon = ['Fists', 1]

                    self.remove_item()
                    self.reload_equipment()

                elif game.inventory[3][self.selection] == 'arm':      # Unequips armor
                    self.equippedarmor = []
                    self.equippedarmor = ['Clothes', 1]

                    self.remove_item()
                    self.reload_equipment()
            
            else:
                self.remove_item()

        else:   # Invalid input check
            menus.splashtext.destroy()
            menus.splashtext = Label(tk, font=('Arial', 9, 'italic'), text=f'Invalid selection.\nEnter the number corresponding to the item you want to drop.')
            menus.splashtext.place(relx=0.5, rely=0.86, anchor='s')      

    def reload_equipment(self):
        self.equipment.destroy()
        self.equipment = Label(tk, text=f'WEAPON: {self.equippedweapon[0]}       ARMOR: {self.equippedarmor[0]}\n\nATK: {self.equippedweapon[1]}       DEF: {self.equippedarmor[1]}')
        self.equipment.place(relx=0.5, rely=0.02, anchor='n')    

    def remove_item(self):
        menus.splashtext = Label(tk, font=('Arial', 9, 'italic'), text=f'You drop the {game.inventory[0][self.selection]}.')
        menus.splashtext.place(relx=0.5, rely=0.86, anchor='s')

        game.inventory[0].pop(self.selection)
        game.inventory[1].pop(self.selection)
        game.inventory[2].pop(self.selection)
        game.inventory[3].pop(self.selection)

        self.reload_inventory()
    
    def reload_inventory(self):
        self.inventorydisplay.destroy()
        self.equipbutton.destroy()
        self.dropbutton.destroy()
        self.inventoryselection.destroy()
        self.backbutton.destroy()

        if game.inventory == [[],[],[],[]]:
            self.inventorydisplay = Label(tk, text='_______________________________________________________________________\n\nYour inventory is now empty.\n_______________________________________________________________________', font=('Arial', 11))
            self.inventorydisplay.place(relx=0.02, rely=0.5, anchor='w')       # This shows when dropping the last item in inventory)

        else:
            self.selection = -1
            self.open_inventory()

inven = Inventory()

class Interface:
    def __init__(self):
        self.centertext = Label(tk)         # Centered text
        self.startbutton = Button(tk)       # Main menu start button
        self.helpbutton = Button(tk)        # Help menu button in main menu
        self.backbutton = Button(tk)        # General back button (inv, help, etc)
        self.levellabel = Label(tk)         # Level display (top right corner)
        self.healthlabel = Label(tk)        # Health display (top left corner)
        self.inventorybutton = Button(tk)   # Inventory button (bottom left corner)
        self.splashtext = Label(tk)         # Text below the scenery describing the situation
        self.movebutton = Button(tk)        # "Move forward" button
        self.interactbutton = Button(tk)    # Interact button (to interact with objects in world)

    def main_menu(self):            # What the player sees right after running the program
        self.centertext.destroy()
        self.backbutton.destroy()

        menus.centertext = Label(tk, text='Welcome to PythRPG!\nPlease refrain from resizing the window!', font=('Arial', 12))
        menus.centertext.place(relx=0.5, rely=0.5, anchor='center')

        menus.startbutton = Button(tk, text='Start', command=menus.start_game)
        menus.startbutton.place(relx=0.02, rely=0.98, anchor='sw')

        menus.helpbutton = Button(tk, text='Help', command=menus.help_menu)
        menus.helpbutton.place(relx=0.98, rely=0.98, anchor='se')

    def start_game(self):
        self.centertext.destroy()
        self.startbutton.destroy()
        self.helpbutton.destroy()

        self.levellabel = Label(tk, font=('Arial', 12), text=(f'Level: {game.playerlevel}'))
        self.levellabel.place(relx=0.98, rely=0.02, anchor='ne')

        self.healthlabel = Label(tk, font=('Arial', 12), text=(f'Health: {game.playerhealth}'))
        self.healthlabel.place(relx=0.02, rely=0.02, anchor='nw')

        show_enviro('n','n')

    def help_menu(self):
        self.centertext.destroy()
        self.startbutton.destroy()
        self.helpbutton.destroy()

        menus.backbutton = Button(tk, text='Back', command=menus.main_menu)
        menus.backbutton.place(relx=0.5, rely=0.98, anchor='s')

        self.centertext = Label(tk, font=('Arial', 12), text=
                          'How to play:\n\n'
                          'Use the buttons towards the bottom of the screen!\n')
        self.centertext.place(relx=0.5, rely=0.5, anchor='center')

    def return_to_world(self):
        inven.inventorydisplay.destroy()
        inven.inventoryselection.destroy()
        inven.dropbutton.destroy()
        inven.equipbutton.destroy()
        inven.equipment.destroy()

        show_enviro('n','n')

menus = Interface()

# ~~~~~~~~~~~~~ ~~~~~~~~~~~~ ~~~~~~~~~~~~~
# ~~~~~~~~~~~~~ END OF SETUP ~~~~~~~~~~~~~
# ~~~~~~~~~~~~~ ~~~~~~~~~~~~ ~~~~~~~~~~~~~

menus.main_menu()

tk.mainloop()