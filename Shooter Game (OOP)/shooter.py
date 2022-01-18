# Author: Shanie Hsieh

#####################
# Game Initializers #
#####################

class Map:
    """Create a 5x5 map where the battle takes place"""
    map_spots = [(x, y) for x in range (0,5) for y in range(0,5)] #all possible spaces on map

    def __init__(self):
        self.spike = Bomb()
        self._itemlocation = {}
    
    def place_agent(self, agent, location):
        """Updates agent position on the map"""
        self._itemlocation.update({agent: location})

    def get_location(self, agent):
        """Gets the location of specified agent"""
        return self._itemlocation.get(agent)

#################
# Agents & Bomb #
#################

class Agent:
    """Holds agents health and ability"""
    
    def __init__(self, name, location, bm):
        self.name = name
        self.location = location
        self.battle_map = bm
        self.health = 150
        bm.place_agent(self, self.location)
    
    def update_location(self, agent):
        agent.location = self.battle_map.get_location(self)
    
    def __repr__(self):
        return self.name

class Bomb:
    """Holds bomb attributes"""

    def __init__(self, name = "Bomb", location = (4,0)):
        self.name = name
        self.location = location
        self.defuse = 3
        self.is_defused = False 
    
    def __repr__(self):
        return self.name


###########
# Actions #
###########

class Actions:
    """all possible actions are defined here. A player can choose to shoot, move, use ability, or defuse"""        
    
    def shoot(self, target, target_list, bm):
        """A target is hit and loses 50 health. Once target's health is 0, they are removed from their team."""
        target.health -= 50
        if target.health == 0:
            target_list[target_list.index(target)] = None
            del bm._itemlocation[target]
    
    def move(self, agent, location, bm):
        """A player can move an agent in any direction"""
        currlocation = agent.location
        if location == 'up':
            target_spot = (currlocation[0]-1, currlocation[1])
        elif location == 'down': 
            target_spot = (currlocation[0]+1, currlocation[1])
        elif location == 'left': 
            target_spot = (currlocation[0], currlocation[1]-1)
        elif location == 'right': 
            target_spot = (currlocation[0], currlocation[1]+1)
        elif location == 'up left': 
            target_spot = (currlocation[0]-1, currlocation[1]-1)
        elif location == 'up right': 
            target_spot = (currlocation[0]-1, currlocation[1]+1)
        elif location == 'down left': 
            target_spot = (currlocation[0]+1, currlocation[1]-1)
        elif location == 'down right': 
            target_spot = (currlocation[0]+1, currlocation[1]+1)
        bm.place_agent(agent, target_spot)
        agent.update_location(agent)
    
    def defuse(self, bm):
        """A player must defuse the bomb 3 times in order to succesfully win."""
        bm.spike.defuse -= 1
        if bm.spike.defuse == 0:
            bm.spike.is_defused = True


###############
# Game Master #
###############

class GameController:
    """Controls how the game continues on and when the game ends."""

    def __init__(self, battle_map):
        self.battle_map = battle_map
        self.action = Actions()

    def is_game_running(self, attackers, defenders):
        """Checks to see that an outcome has not taken place yet so the game should continue to run"""
        if attackers == [None] * len(attackers):
            print("VICTORY! You have defeated the attackers.")
            return False
        elif defenders == [None] * len(defenders):
            print("DEFEAT! The attackers have defeated your team.")
            return False
        elif self.battle_map.spike.is_defused:
            print("VICTORY! Bomb is defused.")
            return False
        else:
            return True
    
    def next_move_options(self, agent, attackers):
        """ A player can choose to shoot an enemy, move 1 or 2 squares, or defuse the spike
            shoot: this option is only avaiable if the enemy is in the same row or column as the player
            move: a player can choose to move 1 square in any direction (so any of the surrounding squares)
            defuse: this option is only available if a player is on the bomb
        """
        player_options = []
        shoot_targets = self.target_options(agent, attackers)
        move_position = self.move_positions(agent.location)
        if shoot_targets: #checks that there are targets the player can shoot
            player_options.append("shoot")
        if move_position: #checks that there are positions that player can move to
            player_options.append("move")
        if agent.location == self.battle_map.spike.location: #checks that player is on the same spot as the spike in order to defuse
            player_options.append("defuse")
        return player_options
    
    def target_options(self, agent, attlist):
        """Shows potential targets for given agent. Targets can only be in the same row or column"""
        potential_targets = []
        location = self.battle_map.get_location(agent)
        for person in attlist:
            if person != None:
                if person.location[0] == location[0] or person.location[1] == location[1]:
                    potential_targets.append(person)
        return potential_targets

    def move_positions(self, location):
        """Shows potential squares a player can move to. Squares are within the map limits."""
        potential_moves = []
        displayed_moves = []
        if (location[0]-1, location[1]) in Map.map_spots: #checks up
            displayed_moves.append('up')
            potential_moves.append((location[0]-1, location[1]))
        if (location[0]+1, location[1]) in Map.map_spots: #checks down
            displayed_moves.append('down')
            potential_moves.append((location[0]+1, location[1]))
        if (location[0], location[1]-1) in Map.map_spots: #checks left
            displayed_moves.append('left')
            potential_moves.append((location[0], location[1]-1))
        if (location[0], location[1]+1) in Map.map_spots: #checks right
            displayed_moves.append('right')
            potential_moves.append((location[0], location[1]+1))
        if (location[0]-1, location[1]-1) in Map.map_spots: #checks diagonally up-left
            displayed_moves.append('up left')
            potential_moves.append((location[0]-1, location[1]-1))
        if (location[0]-1, location[1]+1) in Map.map_spots: #checks diagonally up-right
            displayed_moves.append('up right')
            potential_moves.append((location[0]-1, location[1]+1))
        if (location[0]+1, location[1]-1) in Map.map_spots: #checks diagonally down-left
            displayed_moves.append('down left')
            potential_moves.append((location[0]+1, location[1]-1))
        if (location[0]+1, location[1]+1) in Map.map_spots: #checks diagonally down-right
            displayed_moves.append('down right')
            potential_moves.append((location[0]+1, location[1]+1))
        for item in potential_moves: #checking to see that if there is an agent on that spot, that spot is no longer a potential move
            if item in self.battle_map._itemlocation.values():
                move_index = potential_moves.index(item)
                potential_moves.remove(item)
                del displayed_moves[move_index]
        return displayed_moves

    def execute_move(self, target_list, agent_input, user_input, second_input = None):
        """Performs the action based on user input"""
        user_input = user_input.lower()
        if user_input == "shoot":
            self.action.shoot(second_input, target_list, self.battle_map)
            # print(agent_input, "shot", second_input)
            return "%s shot %s. %s now has %d health." % (agent_input, second_input, second_input, second_input.health)
        elif user_input == "move":
            self.action.move(agent_input, second_input, self.battle_map)
            return "%s moved %s." % (agent_input, second_input)
        elif user_input == "defuse":
            self.action.defuse(self.battle_map)
            return "The spike has been defused %d/3 times." % (3-self.battle_map.spike.defuse)

    def computer(self, attackers, defenders):
        """Computer can only shoot (doesn't move) so action is taken when there is an agent in the same row or column or if an enemy is on the spike"""
        print("Computer's Turn!")
        defender_location = [(person, person.location) for person in defenders if person != None] 
        
        if self.battle_map.spike.location in defender_location: #shoots enemy on bomb
            for group in defender_location:
                if group[1] == self.battle_map.spike.location:
                    target = group[0]
            self.action.shoot(target, defenders, self.battle_map)
            return "%s has shot the agent defusing the spike." % (attackers[0])
        
        total_moves = self.computer_moves(attackers, defenders)
        if total_moves: #if this list is not empty, the computer will choose the first agent on this list to shoot the first available person
            first_agent = total_moves[0]
            self.action.shoot(first_agent[1][0], defenders, self.battle_map)
            return "%s has shot %s." % (first_agent[0], first_agent[1][0])
        else:
            return "Computer did nothing."
    
    def computer_moves(self, attackers, defenders):
        """Makes a list of tuples showing all possible actions for each attacker"""
        total_moves = []
        for agent in attackers:
            if agent != None:
                possible_targets = self.target_options(agent, defenders)
                if possible_targets:
                    total_moves.append((agent, possible_targets))
        return total_moves
    
    def valid_input(self, valid_list, user_input):
        """checks that the user input is a valid input in the given list"""
        if user_input in valid_list:
            return True
        else:
            return False


############
# Displays #
############

class Display:
    """Shows all visual aspects of the game.
        All methods are static since only 1 display.
    """

    @staticmethod
    def choose_agent(deflist):
        """select an agent to perform an action"""
        print("Select an agent to to perform an action:")
        for agent in deflist:
            if agent != None:
                print(f'\t{agent}')

    @staticmethod
    def show_moves(next_move):
        """shows all possible moves"""
        print("What would you like to do?")
        for move in next_move:
            print(f'\t{move}')

    @staticmethod
    def show_targets(targets):
        """shows all possible moves"""
        print("Who would you like to shoot?")
        for person in targets:
            print(f'\t{person}')

    @staticmethod
    def show_spaces(moves):
        """shows all possible moves"""
        print("Where would you like to move?")
        for move in moves:
            print(f'\t{move}')

    @staticmethod
    def show_map(bm):
        """prints out current map"""
        for x in range(0,5):
            for y in range(0,5):
                if (x,y) in bm._itemlocation.values():
                    for key,value in bm._itemlocation.items():
                        if value == (x,y):
                            print("|",key,"|", end='')
                elif (x,y) == (4,0):
                    print("|bomb |", end='')
                else:
                    print("|     |", end='')
            print("")

    @staticmethod
    def show_agent_stats(defenderlist, attackerlist):
        """shows all agents stats"""
        print("Defenders' Health: ")
        for person in defenderlist:
            if person != None:
                print(f"\t{person} {person.health}/150")
        print("Attackers' Health: ")
        for person in attackerlist:
            if person != None:
                print(f"\t{person} {person.health}/150")

    @staticmethod
    def show_spike_status(bm):
        """shows how close the spike is going be to defused"""
        status = 3 - bm.spike.defuse
        print(f"Spike is {status}/3 defused.")


#command line starts from here
if __name__ == '__main__': 
    #welcome screen, prompts user to type enter to begin playing
    while True:
        print("---------------------------------------------")
        print('')
        print('Welcome to Valorant Range!')
        print('Here we learn to practice defending and focusing on gun play')
        print('The goal is to either eliminate the enemy team before they eliminate you, or to defuse the spike before the enemy team sees you.')
        print('')
        print('You are placed on the upper right side of the map whereas the enemy team is scattered on the left side of the map.')
        print('The spike is all the way at the bottom left of the map.')
        print('You may have the option to shoot, move, or defuse!')
        print("Type 'help' for more information. Othewise, type 'enter' to begin playing!")
        print('')
        print("---------------------------------------------")
        initial_input = input("Type here: ").lower()
        if initial_input == "enter":
            print('')
            print("Good luck! Have Fun!")
            print("---------------------------------------------")
            break
        #help box for user info
        elif initial_input == "help":
            print("---------------------------------------------")
            print('')
            print('You are placed in a 3v3. Your available moves include: ')
            print('')
            print('move -- you can move to any surrounding square, as long as it is not off the map or occupied by another agent')
            print('shoot -- you can shoot an enemy only if there are in the same row or column as you')
            print('defuse -- you can defuse the spike only if a team member is on the same spot as the spike')
            print('')
            print('You are going against the computer who can only shoot in front of them or anyone at the spike')
            print('If at any point, you are lost of what actions you can take, just follow the prompts and they will direct you which moves are available!')
            print("---------------------------------------------")
            continue
        else:
            print("---------------------------------------------")
            print("Please type 'enter' to begin playing.")
            continue

    #agent select and create map with locations set up
    battle_map = Map()
    da1 = Agent('DA1', (0,3), battle_map)
    da2 = Agent('DA2', (0,4), battle_map)
    da3 = Agent('DA3', (1,4), battle_map)
    aa1 = Agent('AA1', (0,0), battle_map)
    aa2 = Agent('AA2', (3,2), battle_map)
    aa3 = Agent('AA3', (4,1), battle_map)
    defenders = [da1, da2, da3]
    attackers = [aa1, aa2, aa3]
    gc = GameController(battle_map)

    #computer and player take turns
    while True:

        #show stats and map
        Display.show_agent_stats(defenders, attackers)
        Display.show_spike_status(battle_map)
        print("---------------------------------------------")
        Display.show_map(battle_map)
        print("---------------------------------------------")

        #player chooses an agent to do an action with
        Display.choose_agent(defenders)
        agent_prompt = input("Who would you like to choose? ").lower()
        if agent_prompt == "surrender":
            print("---------------------------------------------")
            print("DEFEAT")
            break
        elif agent_prompt == "da1":
            agent_prompt = defenders[0]
        elif agent_prompt == "da2":
            agent_prompt = defenders[1]
        elif agent_prompt == "da3":
            agent_prompt = defenders[2]
        elif not gc.valid_input(defenders, agent_prompt):
            print("Not an option! Try again.")
            print("---------------------------------------------")
            continue

        #gets input and executes
        while True: 
            Display.show_moves(gc.next_move_options(agent_prompt, attackers))
            move_prompt = input("Type your response: ").lower()
            if not gc.valid_input(gc.next_move_options(agent_prompt, attackers), move_prompt):
                print("Not an option! Try again.")
                print("---------------------------------------------")
                continue
            elif move_prompt == "shoot":
                while True:
                    Display.show_targets(gc.target_options(agent_prompt, attackers))
                    second_prompt = input("Type your response: ").lower()
                    if second_prompt == "aa1":
                        second_prompt = attackers[0]
                    elif second_prompt == "aa2":
                        second_prompt = attackers[1]
                    elif second_prompt == "aa3":
                        second_prompt = attackers[2]
                    elif not gc.valid_input(gc.target_options(agent_prompt, attackers), second_prompt):
                        print("Not an option! Try again.")
                        print("---------------------------------------------")
                        continue
                    if gc.valid_input(gc.target_options(agent_prompt, attackers), second_prompt):
                        print(gc.execute_move(attackers, agent_prompt, move_prompt, second_prompt))
                        break
                    break
                break
            elif move_prompt == "move":
                while True:
                    Display.show_spaces(gc.move_positions(agent_prompt.location))
                    second_prompt = input("Type your response: ")
                    if not gc.valid_input(gc.move_positions(agent_prompt.location), second_prompt):
                        print("Not an option! Try again.")
                        print("---------------------------------------------")
                        continue
                    else:
                        print("---------------------------------------------")
                        print(gc.execute_move(attackers, agent_prompt, move_prompt, second_prompt))
                    break
                break
            elif move_prompt == "defuse":
                print("---------------------------------------------")
                print(gc.execute_move(attackers, agent_prompt, move_prompt))
                break
            
        print("---------------------------------------------")

        #computer plays, shows results, and updates
        print(gc.computer(attackers, defenders))
        print("---------------------------------------------")

        #if an end-goal is met, game stops running and outputs defeat or victory
        if gc.is_game_running(attackers, defenders) == False:
            break