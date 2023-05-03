# Thomas McInnes
# CSCI 102 Section B
# Create Project: PythRPG      

            # BUGS RIGHT NOW:

            # NOTES FOR NEXT TIME:

from tkinter import *
import random

# ~~~~~~~~~~~~~ ~~~~~~~~~~~ ~~~~~~~~~~~~~
# ~~~~~~~~~~~~~ DEFINITIONS ~~~~~~~~~~~~~
# ~~~~~~~~~~~~~ ~~~~~~~~~~~ ~~~~~~~~~~~~~

tk = Tk(className=' PythRPG')   # Sets up tkinter, and names the window 'PythRPG' (everything tkinter related refers to 'tk' from here on)
tk.geometry("600x600")          # Sets the size of the window (width x height)

# Backgrounds should be 400x400, enemies should be 300x300

    # BGs: 0 = Grassy field, 1 = Field without stick, 2 = Field with stick, 3 = Road, 4 = Second Road, 5 = Village, 6 = Second Village, 7 = Mountains
backgrounds = [PhotoImage(file='grassy.png'), PhotoImage(file='grassy2.png'), PhotoImage(file='stick.png'), 
               PhotoImage(file='road.png'), PhotoImage(file='road2.png'), PhotoImage(file='village.png'), 
               PhotoImage(file='village2.png'), PhotoImage(file='mountains.png')]
currentbg = 0

menubackground = PhotoImage(file='menu.png')

    # Enemies: 0 = Boar, 1 = Wolf, 2 = Bear
enemies = [PhotoImage(file='boar.png'), PhotoImage(file='wolf.png'), PhotoImage(file='bear.png')]
enemyhealthvalue = 0

    # If something is interactable in the enviro, set = 'y' otherwise set = 'n'
interactable = 'n'

def show_enviro(caninteract, incombat): # if incombat == -1, true, if incombat == 0, no object and not in combat
    global enemyhealthvalue

    menus.splashtext.destroy()
    game.bg.destroy()
    game.enemysprite.destroy()
    menus.inventorybutton.destroy()
    menus.interactbutton.destroy()
    menus.movebutton.destroy()
    combat.continuebutton.destroy()
    combat.droplabel.destroy()

    menus.splashtext = Label(tk, font=('Arial', 9, 'italic'), text=game.situation)
    menus.splashtext.place(relx=0.5, rely=0.9, anchor='s')

    if incombat == -1:    # Enemy encounter (setup)

        combat.combatsplashes = []      # Updating the combat splash text per fight
        combat.combatsplashes = [f'Look out! A {game.enemies[0][game.enemy]} is approaching!',
                                 f'The {game.enemies[0][game.enemy]} is just standing there... menacingly!',
                                 f"Doesn't seem like this {game.enemies[0][game.enemy]} wants to be friends..."]
        
        game.enemysprite = Label(tk, image=enemies[game.enemy], borderwidth=0)
        game.enemysprite.place(relx=0.5, rely=0.5, anchor='center')

        enemyhealthvalue = game.enemies[1][game.enemy]
        combat.player_turn()    # Pushes player to combat loop

    if caninteract == 'y':  # Shows interact button
        menus.interactbutton = Button(tk, text='Interact', command=interact)
        menus.interactbutton.place(relx=0.5, rely=0.98, anchor='s')

    if incombat != -1:                  # None of this stuff appears if in combat
        game.bg = Label(tk, image=backgrounds[currentbg])
        game.bg.place(relx=0.5, rely=0.5, anchor='center')
        
        menus.inventorybutton = Button(tk, text='Inventory', command=inven.open_inventory)
        menus.inventorybutton.place(relx=0.02, rely=0.98, anchor='sw')

        menus.movebutton = Button(tk, text='Move', command=game.advance)
        menus.movebutton.place(relx=0.98, rely=0.98, anchor='se')

def interact():
    global interactable
    global worldobject
    global currentbg
    menus.splashtext.destroy()

    if worldobject == 2:
        menus.splashtext = Label(tk, font=('Arial', 9, 'italic'), text='You pick up the stick off the ground.')
        menus.splashtext.place(relx=0.5, rely=0.9, anchor='s')

        currentbg = 1   # Removes stick from graphic
        game.bg.destroy()
        game.bg = Label(tk, image=backgrounds[currentbg])
        game.bg.place(relx=0.5, rely=0.5, anchor='center')

        menus.interactbutton.destroy()

        game.inventory[0].append('Stick')
        game.inventory[1].append('A simple stick. Better than your fists!')
        game.inventory[2].append(4)
        game.inventory[3].append('wep')

        game.situation = 'You picked up the stick off the ground.'
        worldobject = 0
        interactable = 'n'

# ~~~~~~~~~~~~~ ~~~~~~~ ~~~~~~~~~~~~~
# ~~~~~~~~~~~~~ CLASSES ~~~~~~~~~~~~~
# ~~~~~~~~~~~~~ ~~~~~~~ ~~~~~~~~~~~~~

class Gameplay:
    def __init__(self):
        # Inventory format: List 0 is Item Name, List 1 is Description, List 2 is Damage/Defense/Heal, List 3 is Type
        # Types: wep = weapon, arm = armor, use = usable item (potions)
        self.inventory = [[],[],[],[]]
        self.playerlevel = 1        # Player level
        self.playerhealth = 100     # Current player health
        self.xptolevelup = 5        # Amount of XP needed to level up
        self.currentxp = 0          # Current player XP
        self.bg = Label(tk)         # Background graphic
        # Below is a list of situations that the player cycles through. 0 is the intro, 1 is the stick, 0 and 1 are NOT random
        self.situationlist = ['You awaken to the feeling of warm sunlight on your face. Opening your eyes, you find yourself\nin the middle of a vast field of grass.',
                              'As you wander the field, you come across a hearty-looking stick laying on the ground.',
                              'enemy',      # Situation 2 (for reference)
                              'You find a road... who knows where it leads?', # 3
                              'The seemingly hopeful road leads nowhere, and you find yourself still in a grassy field.', # 4
                              'The road leads to a busy village, full of buildings and people walking about.', # 5
                              'After following the road, you eventually exit the village and re-enter the wilderness.', # 6
                              'After walking for some time, you spot some mountains in the distance.',  # 7
                              'Further exploration leads to more empty fields of grass.', # 8
                              'You marvel at the sheer size of this grassy field as you wander.', # 9
                              'After defeating your foe, you pause to gather your surroundings.'] # 10
        self.situation = self.situationlist[0]
        # Enemies format: List 0 is Name, List 1 is Health, List 2 is Damage, List 3 is XP worth
        self.enemies = [['Wild Boar', 'Wolf', 'Bear'],
                        [25, 40, 55],   # Usual values: 25, 45, 55 (HEALTH) (For bugfixing purposes)
                        [8, 15, 28],   # 8, 20, 35 (DAMAGE)
                        [5, 10, 15]]    # 5, 10, 15 (XP)
        # Enemy numbers: 0 is boar, 1 is wolf, 2 is bear
        self.enemy = 0
        self.enemysprite = Label(tk)    # Enemy graphics

    def advance(self):
        global worldobject
        global interactable
        global currentbg

        if self.situation == self.situationlist[0]:         # This is immediately after first screen, leads to stick on ground
            self.situation = self.situationlist[1]
            worldobject = 2
            currentbg = 2
            interactable = 'y'

        else:
            if self.situation == self.situationlist[1]:     # Gets rid of the stick if user ignores it
                menus.interactbutton.destroy()
                worldobject = 0
                interactable = 'n'

            # Start of regular gameplay loop

            if self.situation == self.situationlist[2]:     # After getting out of a fight (same as if no fight)
                self.situation = self.situationlist[10]     # Situation 10 is the 'gather your surroundings' thing that lets you check your inventory and stuff
                worldobject = 0

            elif self.situation == self.situationlist[3]:   # Situation 3 is the road
                if random.randint(1, 2) == 1:               # This choooses between the road ending or the road leading to the village
                    self.situation = self.situationlist[4]
                    currentbg = random.randint(0,1)         # Road ends
                else:
                    self.situation = self.situationlist[5]
                    currentbg = random.randint(5,6)         # Road leads to village
            
            elif self.situation == self.situationlist[5]:   # This is if the road led to the village, this one leads back to the wilderness
                self.situation = self.situationlist[6]
                currentbg = random.randint(0,1)

            elif random.randint(1, 2) == 1:   # Enemy encounter (only happens if not on road 'arc')
                self.situation = self.situationlist[2]
                if self.playerlevel <= 3:
                    self.enemy = random.randint(0, self.playerlevel - 1)    # Picks an enemy (0 is boar, 1 is wolf, etc)
                else:                                                       # You can't get into a fight with an enemy that your level is below
                    self.enemy = random.randint(0, 2)
                worldobject = -1    # Worldobject of -1 means enemy encounter

            else:   # If not getting out of fight, not on road arc, and no enemy appears, the player can either run into the road or continue wandering the wilderness
                if random.randint(1,3) == 1:
                    self.situation = self.situationlist[3]  # Starts the 'road arc'
                    currentbg = random.randint(3,4)
                elif (random.randint(1,2) == 1) and (currentbg != 7):
                    self.situation = self.situationlist[7]  # Mountains
                    currentbg = 7
                else:  # More grassy fields
                    if currentbg == 1:
                        currentbg = 0
                        self.situation = self.situationlist[8]
                    else:
                        currentbg = 1
                        self.situation = self.situationlist[9]

        show_enviro(interactable, worldobject)   # End of advance function

game = Gameplay()

class Combat:
    def __init__(self):
        self.attackbutton = Button(tk)      # Button that attacks on your turn
        self.guardbutton = Button(tk)       # Button that guards (raises defense) on your turn
        self.continuebutton = Button(tk)    # Button that allows player to continue after battle
        self.enemyhealth = Label(tk)        # Shows enemy health
        self.attackdamage = 0               # The amount of damage you deal in an attack
        self.enemyattack = 0                # The amount of damage an enemy deals to you in an attack
        self.damageindicator = Label(tk)    # Text damage indicator for how much damage is dealt
        self.combatsplashes = []            # Splash text in-between attacks/guards (this is updated in show_enviro)
        self.guardmult = 1                  # Multiplier that accumulates and increases attack damage
        # Loot table: list 0 is item name, list 1 is rarity (0 - 100) (higher number = less rare)
        # Loot table: list 2 is item description, list 3 is item use value (dmg, def, heal), list 4 is item type (wep, arm, use)
        # Winning a battle will give a chance to drop every item in the loot table, as long as there's room in the inventory.
        self.loottable = [['Leather Cape', 'Dragon Armor', "Jamiroquai's Hat", 'Small Health Potion', 'Medium Health Potion', 'Large Health Potion', 'Rusty Sword', 'Claymore', 'Murasama'],
                          [50, 30, 5, 60, 40, 10, 50, 30, 3],   # RARITIES
                          ['A somewhat battered leather cape.', 'Armor forged from dragon scales.', 'You could rearrange furniture in this hat!',
                           'A potion that heals 10 health.', 'A potion that heals 25 health.', 'A potion that heals 50 health!',
                           'A pretty beat up and old sword.', 'A large, heavy sword.', 'Memories broken, the truth goes unspoken...'],
                          [6, 12, 30, 10, 20, 50, 8, 15, 40],   # POWER
                          ['arm', 'arm', 'arm', 'use', 'use', 'use', 'wep', 'wep', 'wep']]
        self.drops = ''                     # String that holds all the drops recieved after a battle
        self.droplabel = Label(tk)          # tkinter label that displays drop information
        self.enemieskilled = 0              # Amount of enemies the player has defeated

    def player_turn(self):
        self.enemyhealth.destroy()
        menus.splashtext.destroy()
        
        menus.splashtext = Label(tk, font=('Arial', 10, 'italic'), text=self.combatsplashes[random.randint(0,2)])
        menus.splashtext.place(relx=0.5, rely=0.86, anchor='s')

        self.attackbutton = Button(tk, text='Attack', command=combat.attack)
        self.attackbutton.place(relx=0.43, rely=0.97, anchor='s')

        self.guardbutton = Button(tk, text='Guard', command=combat.guard)
        self.guardbutton.place(relx=0.565, rely=0.97, anchor='s')

        self.enemyhealth = Label(tk, fg='#782020', font=('Arial', 12), text=f'{game.enemies[0][game.enemy]} Health: {enemyhealthvalue}')
        self.enemyhealth.place(relx=0.5, rely=0.2, anchor='n')

    def enemy_turn(self):
        menus.splashtext.destroy()
        self.damageindicator.destroy()

        self.enemyattack = int(((game.enemies[2][game.enemy] + int((game.playerlevel - 1) * 2) + (random.randint(-1, 1))) - inven.equippedarmor[1]) // self.guardmult)
        if self.enemyattack <= 0:
            self.enemyattack = random.randint(1,2)

        menus.splashtext = Label(tk, font=('Arial', 10, 'italic'), text=f'You got hit for         damage!')
        menus.splashtext.place(relx=0.5, rely=0.86, anchor='s')

        self.damageindicator = Label(tk, font=('Arial', 14, 'bold'), fg='#a83232', text=self.enemyattack)
        self.damageindicator.place(relx=0.525, rely=0.864, anchor='s')

        game.playerhealth -= self.enemyattack
        if game.playerhealth <= 0:
            menus.healthlabel.destroy()
            menus.healthlabel = Label(tk, fg='#782020', font=('Arial', 12, 'bold'), text=(f'Health: 0'))
            menus.healthlabel.place(relx=0.02, rely=0.02, anchor='nw')

            tk.after(1500, lambda: self.die())
        else:
            menus.healthlabel.destroy()
            menus.healthlabel = Label(tk, fg='#782020', font=('Arial', 12, 'bold'), text=(f'Health: {game.playerhealth}'))
            menus.healthlabel.place(relx=0.02, rely=0.02, anchor='nw')
            
            tk.after(1500, lambda: self.player_turn())

    def win(self):
        game.enemysprite.destroy()
        self.damageindicator.destroy()
        menus.splashtext.destroy()
        self.enemyhealth.destroy()

        game.currentxp += game.enemies[3][game.enemy]
        if game.currentxp >= game.xptolevelup:
            while game.currentxp >= game.xptolevelup:
                game.playerlevel += 1
                game.currentxp = game.currentxp - game.xptolevelup
                game.xptolevelup += 5

            menus.levellabel.destroy()
            menus.levellabel = Label(tk, fg='#204678', font=('Arial', 12, 'bold'), text=(f'Level: {game.playerlevel}'))
            menus.levellabel.place(relx=0.98, rely=0.02, anchor='ne')

            menus.splashtext = Label(tk, fg='#0d3b18', font=('Arial', 15, 'bold'), text=f'You won!\nYou got {game.enemies[3][game.enemy]} XP!\n\nYou leveled up!')
            menus.splashtext.place(relx=0.5, rely=0.12, anchor='n')
        else:
            menus.splashtext = Label(tk, fg='#0d3b18', font=('Arial', 15, 'bold'), text=f'You won!\nYou got {game.enemies[3][game.enemy]} XP!')
            menus.splashtext.place(relx=0.5, rely=0.12, anchor='n')

        self.drops = ''
        for i in range(0, len(self.loottable[0])):
            if random.randint(1, 105) <= self.loottable[1][i]:
                if (len(game.inventory[0]) < 8):
                    self.drops += f'You recieved {self.loottable[0][i]}!\n'
                    game.inventory[0].append(self.loottable[0][i])
                    game.inventory[1].append(self.loottable[2][i])
                    game.inventory[2].append(self.loottable[3][i])
                    game.inventory[3].append(self.loottable[4][i])
                else:
                    self.drops += 'Your inventory is full.'
                    break
        if self.drops == '':    # Checks to see if the enemy didn't drop anything so the player doesn't get a blank menu
            self.drops += "The enemy didn't drop anything."
        
        self.droplabel = Label(tk, font=('Arial', 10, 'bold'), text=self.drops)
        self.droplabel.place(relx=0.5, rely=0.6, anchor='center')

        game.situation = game.situationlist[2]      # Sets game situation to 'enemy' to tell the code to not throw another enemy at the player right away
        self.continuebutton = Button(tk, text='Continue', command=game.advance)
        self.continuebutton.place(relx=0.5, rely=0.95, anchor='s')

        self.enemieskilled += 1

    def die(self):
        game.enemysprite.destroy()
        self.damageindicator.destroy()
        menus.splashtext.destroy()
        self.enemyhealth.destroy()
        menus.healthlabel.destroy()
        menus.levellabel.destroy()

        menus.centertext = Label(tk, fg=('#521010'), text='You died.', font=('Arial', 20, 'bold'))
        menus.centertext.place(relx=0.5, rely=0.5, anchor='center')

        menus.splashtext = Label(tk, font=('Arial', 12, 'italic'), text=f'You reached level {game.playerlevel}.\nYou defeated {self.enemieskilled} enemies.')
        menus.splashtext.place(relx=0.5, rely=0.7, anchor='s')

        menus.quitbutton = Button(tk, text='Quit', command=tk.destroy)
        menus.quitbutton.place(relx=0.5, rely=0.97, anchor='s')

    def attack(self):
        global enemyhealthvalue
        menus.splashtext.destroy()
        self.damageindicator.destroy()

        if random.randint(1, 25) == 1:
            menus.splashtext = Label(tk, font=('Arial', 10, 'italic'), text=f'Your attack missed!')
            menus.splashtext.place(relx=0.5, rely=0.86, anchor='s')

        else:
            if random.randint(1, 5) == 1:       # Critical hit check (doubles damage)
                self.attackdamage = int(((inven.equippedweapon[1] + random.randint(2, 5)) * 2) * self.guardmult) + (game.playerlevel - 1)

                self.damageindicator = Label(tk, font=('Arial', 14, 'bold'), fg='#fc7e3a', text=f'CRIT! {self.attackdamage} damage!')
                self.damageindicator.place(relx=0.505, rely=0.864, anchor='s')
            else:
                self.attackdamage = int((inven.equippedweapon[1] + random.randint(0, 1)) * self.guardmult) + (game.playerlevel - 1)  # Regular hit
                menus.splashtext = Label(tk, font=('Arial', 10, 'italic'), text=f'You dealt        damage!')
                menus.splashtext.place(relx=0.5, rely=0.86, anchor='s')

                self.damageindicator = Label(tk, font=('Arial', 14, 'bold'), fg='#fc7e3a', text=self.attackdamage)
                self.damageindicator.place(relx=0.505, rely=0.864, anchor='s')
            
            self.guardmult = 1

            enemyhealthvalue -= self.attackdamage
            if enemyhealthvalue < 0:
                enemyhealthvalue = 0

            self.enemyhealth.destroy()
            self.enemyhealth = Label(tk, fg='#782020', font=('Arial', 12), text=f'{game.enemies[0][game.enemy]} Health: {enemyhealthvalue}')
            self.enemyhealth.place(relx=0.5, rely=0.2, anchor='n')

        self.attackbutton.destroy()
        self.guardbutton.destroy()

        if enemyhealthvalue <= 0:   # Check if enemy died from the last attack
            tk.after(1500, lambda: self.win())  # .after format: tk.after(time(ms), lambda: function())
        else:
            tk.after(1500, lambda: self.enemy_turn())   # If the enemy has health above 0, it's the enemies turn

    def guard(self):
        menus.splashtext.destroy()
        self.damageindicator.destroy()

        menus.splashtext = Label(tk, font=('Arial', 10, 'italic'), text=f'You guard, increasing your defense for this turn and bolstering your next attack!')
        menus.splashtext.place(relx=0.5, rely=0.86, anchor='s')

        self.guardmult += 0.5

        self.attackbutton.destroy()
        self.guardbutton.destroy()

        tk.after(2000, lambda: self.enemy_turn())   # Not possible to do damage on a guard so enemy gets its turn by default

combat = Combat()

class Inventory:
    def __init__(self):
        self.inventorysetup = ''                # Inventory setup: for assembling the inventory display
        self.equippedweapon = ['Fists', 1]      # Equipped weapon. Index 0 is name, index 1 is attack dmg
        self.equippedarmor = ['Clothes', 1]     # Equipped armor. Index 0 is name, index 1 is defense value
        self.inventorydisplay = Label(tk)       # What actually gets displayed in inventory
        self.inventoryselection = Entry(tk)     # Entry box to choose item to interact with in inventory
        self.equipment = Label(tk)              # Displays equipment and its stats (ATK, DEF)
        self.equipbutton = Button(tk)           # Equip item button
        self.dropbutton = Button(tk)            # Drop item button
        self.selection = 0                      # Item # selected using entry box (if a valid input is recieved)
        self.selectedname = ''                  # Name of item selected to drop

    def open_inventory(self):
        self.inventorysetup = '_______________________________________________________________________\n\n'

        if self.selection != -1:          # If staying in the inventory (after dropping an item) the splashtext isn't deleted since it should say "you dropped item"
            menus.splashtext.destroy()
        self.selection = 0

        if game.inventory == [[],[],[],[]]:
            menus.splashtext = Label(tk, font=('Arial', 9, 'italic'), text='Your inventory is empty.')
            menus.splashtext.place(relx=0.5, rely=0.9, anchor='s')

        else:
            menus.movebutton.destroy()
            menus.inventorybutton.destroy()
            menus.interactbutton.destroy()
            self.equipment.destroy()
            game.bg.destroy()

            for i in range(0, len(game.inventory[0])):  # Loop that builds the inventory
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

            inven.equipment = Label(tk, text=f'WEAPON: {inven.equippedweapon[0]}       ARMOR: {inven.equippedarmor[0]}\n\nATK: {inven.equippedweapon[1]}       DEF: {inven.equippedarmor[1]}')
            inven.equipment.place(relx=0.5, rely=0.02, anchor='n')

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
                    menus.splashtext.place(relx=0.5, rely=0.9, anchor='s')

                else:
                    self.equippedweapon = []
                    self.equippedweapon.append(game.inventory[0][self.selection])
                    self.equippedweapon.append(game.inventory[2][self.selection])

                    self.reload_equipment()

                    menus.splashtext = Label(tk, font=('Arial', 9, 'italic'), text=f'You equip the {self.equippedweapon[0]}.')
                    menus.splashtext.place(relx=0.5, rely=0.9, anchor='s')
            # Equipping armor
            elif game.inventory[3][self.selection] == 'arm':

                if game.inventory[2][self.selection] == self.equippedarmor[1]:
                    menus.splashtext = Label(tk, font=('Arial', 9, 'italic'), text=f'You have already equipped the {self.equippedarmor[0]}.')
                    menus.splashtext.place(relx=0.5, rely=0.9, anchor='s')

                else:
                    self.equippedarmor = []
                    self.equippedarmor.append(game.inventory[0][self.selection])
                    self.equippedarmor.append(game.inventory[2][self.selection])

                    self.reload_equipment()

                    menus.splashtext = Label(tk, font=('Arial', 9, 'italic'), text=f'You equip the {self.equippedarmor[0]}.')
                    menus.splashtext.place(relx=0.5, rely=0.9, anchor='s')
            # Using an item
            elif game.inventory[3][self.selection] == 'use':

                game.playerhealth += game.inventory[2][self.selection]
                if game.playerhealth > 100:
                    game.playerhealth = 100

                menus.healthlabel.destroy()
                menus.healthlabel = Label(tk, fg='#782020', font=('Arial', 12, 'bold'), text=(f'Health: {game.playerhealth}'))
                menus.healthlabel.place(relx=0.02, rely=0.02, anchor='nw')

                menus.splashtext = Label(tk, font=('Arial', 9, 'italic'), text=f'You drink the {game.inventory[0][self.selection]}, healing {game.inventory[2][self.selection]} health.')
                menus.splashtext.place(relx=0.5, rely=0.9, anchor='s')

                game.inventory[0].pop(self.selection)
                game.inventory[1].pop(self.selection)
                game.inventory[2].pop(self.selection)
                game.inventory[3].pop(self.selection)

                self.reload_inventory()

        else:   # Invalid input check
            menus.splashtext.destroy()
            menus.splashtext = Label(tk, font=('Arial', 9, 'italic'), text=f'Invalid selection.\nEnter the number corresponding to the item you want to equip.')
            menus.splashtext.place(relx=0.5, rely=0.9, anchor='s')

    def drop(self):
        if (self.inventoryselection.get().isdigit() == True) and (int(self.inventoryselection.get()) <= len(game.inventory[0])) and (int(self.inventoryselection.get()) > 0):
            self.selection = int(self.inventoryselection.get()) - 1
            menus.splashtext.destroy()

            self.remove_item()

        else:   # Invalid input check
            menus.splashtext.destroy()
            menus.splashtext = Label(tk, font=('Arial', 9, 'italic'), text=f'Invalid selection.\nEnter the number corresponding to the item you want to drop.')
            menus.splashtext.place(relx=0.5, rely=0.9, anchor='s')      

    def reload_equipment(self):
        self.equipment.destroy()
        self.equipment = Label(tk, text=f'WEAPON: {self.equippedweapon[0]}       ARMOR: {self.equippedarmor[0]}\n\nATK: {self.equippedweapon[1]}       DEF: {self.equippedarmor[1]}')
        self.equipment.place(relx=0.5, rely=0.02, anchor='n')    

    def remove_item(self):
        menus.splashtext = Label(tk, font=('Arial', 9, 'italic'), text=f'You drop the {game.inventory[0][self.selection]}.')
        menus.splashtext.place(relx=0.5, rely=0.9, anchor='s')

        self.selectedname = game.inventory[0][self.selection]

        game.inventory[0].pop(self.selection)
        game.inventory[1].pop(self.selection)
        game.inventory[2].pop(self.selection)
        game.inventory[3].pop(self.selection)
        # The following checks that if what you're dropping is equipped and if it's the last one of its kind in your inventory
        if (self.selectedname == self.equippedweapon[0]) or (self.selectedname == self.equippedarmor[0]):
            if self.selectedname not in game.inventory[0]:
                if (len(game.inventory[3]) == 0) or (game.inventory[3][self.selection] == 'wep'):      # Unequips weapon if it's the only one of the same type in your inventory
                    self.equippedweapon = []
                    self.equippedweapon = ['Fists', 1]

                    self.reload_equipment()

                elif (len(game.inventory[3]) == 0) or (game.inventory[3][self.selection] == 'arm'):      # Unequips armor if same as above
                    self.equippedarmor = []
                    self.equippedarmor = ['Clothes', 1]

                    self.reload_equipment()

        self.selectedname = ''
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

            self.backbutton = Button(tk, text='Back', command=menus.return_to_world)
            self.backbutton.place(relx=0.02, rely=0.98, anchor='sw')

        else:
            self.selection = -1
            self.open_inventory()

inven = Inventory()

class Interface:
    def __init__(self):
        self.centertext = Label(tk)         # Centered text
        self.backgroundimage = Label(tk)    # Image in background
        self.startbutton = Button(tk)       # Main menu start button
        self.helpbutton = Button(tk)        # Help menu button in main menu
        self.infobutton = Button(tk)        # Information button in main menu
        self.backbutton = Button(tk)        # General back button (inv, help, etc)
        self.levellabel = Label(tk)         # Level display (top right corner)
        self.healthlabel = Label(tk)        # Health display (top left corner)
        self.inventorybutton = Button(tk)   # Inventory button (bottom left corner)
        self.splashtext = Label(tk)         # Text below the scenery describing the situation
        self.movebutton = Button(tk)        # "Move forward" button
        self.interactbutton = Button(tk)    # Interact button (to interact with objects in world)
        self.quitbutton = Button(tk)        # Button that appears when you die that closes the game

    def main_menu(self):            # What the player sees right after running the program
        self.centertext.destroy()
        self.backbutton.destroy()
        self.splashtext.destroy()
        self.backgroundimage.destroy()

        menus.backgroundimage = Label(tk, image=menubackground, borderwidth=0)
        menus.backgroundimage.place(relx=0.5, rely=0.5, anchor='center')

        menus.centertext = Label(tk, text='PythRPG', font=('Helvetica', 18, 'bold'))
        menus.centertext.place(relx=0.5, rely=0.1, anchor='n')

        menus.splashtext = Label(tk, text='by Thomas McInnes\nCreated for CSCI 102', font=('Arial', 10, 'italic'))
        menus.splashtext.place(relx=0.5, rely=0.17, anchor='n')

        menus.startbutton = Button(tk, text='Start', command=menus.start_game)
        menus.startbutton.place(relx=0.5, rely=0.9, anchor='s')

        menus.helpbutton = Button(tk, text='Help', command=menus.help_menu)
        menus.helpbutton.place(relx=0.9, rely=0.9, anchor='se')

        menus.infobutton = Button(tk, text='Info', command=menus.info)
        menus.infobutton.place(relx=0.15, rely=0.9, anchor='se')

    def start_game(self):       # When the player presses 'play'
        self.centertext.destroy()
        self.startbutton.destroy()
        self.backgroundimage.destroy()
        self.splashtext.destroy()
        self.infobutton.destroy()
        self.helpbutton.destroy()

        self.levellabel = Label(tk, fg='#204678', font=('Arial', 12, 'bold'), text=(f'Level: {game.playerlevel}'))
        self.levellabel.place(relx=0.98, rely=0.02, anchor='ne')

        self.healthlabel = Label(tk, fg='#782020', font=('Arial', 12, 'bold'), text=(f'Health: {game.playerhealth}'))
        self.healthlabel.place(relx=0.02, rely=0.02, anchor='nw')

        inven.equipment = Label(tk, text=f'WEAPON: {inven.equippedweapon[0]}       ARMOR: {inven.equippedarmor[0]}\n\nATK: {inven.equippedweapon[1]}       DEF: {inven.equippedarmor[1]}')
        inven.equipment.place(relx=0.5, rely=0.02, anchor='n')

        show_enviro('n','n')

    def help_menu(self):        # When the player presses 'help' on menu
        self.centertext.destroy()
        self.startbutton.destroy()
        self.splashtext.destroy()
        self.infobutton.destroy()
        self.helpbutton.destroy()

        menus.backbutton = Button(tk, text='Back', command=menus.main_menu)
        menus.backbutton.place(relx=0.5, rely=0.9, anchor='s')

        self.centertext = Label(tk, font=('Arial', 10), text=
                          'PythRPG is a simple RPG-style game: Fight enemies to level up and get cool gear!\n\n\n'
                          'Use the buttons towards the bottom of the screen to navigate.\n'
                          'The "Move" button will advance you through a randomly generated world.\n'
                          'The "Inventory" button will allow you to open your inventory (if you have items!)\n\n'
                          'Within the inventory, you may equip or drop items using the buttons and entry box.\n'
                          'Enter the number of the item you wish to interact with in the box, then select a button.\n'
                          'Your inventory storage is limited to 8 items maximum.\n\n'
                          'You may randomly encounter an enemy while on your adventure!\n'
                          'Within battle, press the attack button to attack!\n'
                          'You may also guard, which boosts your defense and bolsters your next attack!\n'
                          'Upon defeating an enemy, any items you recieve will be added to your inventory.\n'
                          'In battle, if your health goes below 1, you lose!')
        self.centertext.place(relx=0.5, rely=0.5, anchor='center')

    def return_to_world(self):  # When the player presses the back button in general
        inven.inventorydisplay.destroy()
        inven.inventoryselection.destroy()
        inven.dropbutton.destroy()
        inven.equipbutton.destroy()
        inven.backbutton.destroy()

        show_enviro('n','n')
    
    def info(self):
        self.centertext.destroy()
        self.startbutton.destroy()
        self.splashtext.destroy()
        self.infobutton.destroy()
        self.helpbutton.destroy()

        menus.backbutton = Button(tk, text='Back', command=menus.main_menu)
        menus.backbutton.place(relx=0.5, rely=0.9, anchor='s')

        self.centertext = Label(tk, font=('Arial', 10), text=
                          'PythRPG was created within Python, primarily using the tkinter library.\n'
                          'All image assets were AI generated using playgroundai.com\nusing Stable Diffusion v1.5 and Playground v1 models.\n\n\n'
                          'Item Dictionary:')
        self.centertext.place(relx=0.5, rely=0.2, anchor='n')

        self.splashtext = Label(tk, font=('Arial', 8), justify='left', text=
                          'Stick)                   Type: Weapon | A basic stick.\n'
                          'Rusty Sword)      Type: Weapon | A rusty sword that must have seen many battles.\n'
                          'Claymore)            Type: Weapon | A greatsword of Scottish origin. Heavy but strong!\n'
                          'Murasama)          Type: Weapon | A red high-frequency blade once wielded by Jetstream Sam.\n'
                          'Leather Cape)     Type: Armor    | A simple cape.\n'
                          'Dragon Armor)    Type: Armor    | Strong armor forged from dragon scales!\n'
                          "Jamiroquai's Hat) Type: Armor    | Worn by Jamiroquai in his music video for Virtual Insanity.")
        self.splashtext.place(relx=0.5, rely=0.5, anchor='center')

menus = Interface()

# ~~~~~~~~~~~~~ ~~~~~~~~~~~~ ~~~~~~~~~~~~~
# ~~~~~~~~~~~~~ END OF SETUP ~~~~~~~~~~~~~
# ~~~~~~~~~~~~~ ~~~~~~~~~~~~ ~~~~~~~~~~~~~

menus.main_menu()

tk.mainloop()