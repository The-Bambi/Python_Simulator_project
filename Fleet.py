from Ship import *

class Fleet:
    """Fleet objects. Loads fleet setup from a list of specifically ordered numbers that represent order of ships from Loader class.
    As an initial arguments, takes a list of numbers of ships and loader object."""
    def __init__(self, a_list=None, loader = None):
        self.loader = loader
        ships_stats = self.loader.data
        self.ships = []
        if a_list is not None:
            names = self.loader.short_names
            for index, quantity in enumerate(a_list):
                ship_name = names[index]
                stats = ships_stats[ship_name]
                if int(quantity) == 0:
                    continue
                else:
                    for _ in range(quantity):
                       self.ships.append( Ship(stats, self.loader.quick_cannons[ship_name]) )
        else:
            raise("Error in input data")



    def _create(self, ship_name):
        """Add a ship to the ship list.
        :param ship_name: ship name to get from laoder."""
        self.ships.append(Ship(self.loader.data[ship_name], self.loader.quick_cannons[ship_name]))
        return

    def sweep(self):
        """Function that removes destroyed ships from the fleet and refills the shield of the rest. Creates a temporary list of ships 
        which is filled with non-destroyed ships, and then swaps it with the main ship list. Called for each fleet at the end of the turn."""
        temp_list_of_ships = []
        for index,ship in enumerate(self.ships):
            if ship.current_hp >= 0:
                ship.current_shield = ship.max_shield
                temp_list_of_ships.append(ship)
        self.ships = temp_list_of_ships
        return

    def _status(self):
        """Function that returns a dictionary of quantities of each kind of ship from the fleet."""
        current_count = {i:0 for i in self.loader.data.keys()}
        for ship in self.ships:
            current_count[ship.short_name]+=1
        return current_count

    def count(self):
        """Function returns how many ships is there in the fleet."""
        return len(self.ships)

    def fire(self,fleet):
        """Function responsible for attacking enemy fleet. It takes the enemy fleet object as an argument.
        Creates an empty list that will be filled with ships that will attack again due to quick cannons.
        First it iterates over the main list of ships. Then it while the other list is not empty, it iterates over that
        and puts the lucky ships to "yet another attack" list. Another_attack and yet_another_attack are swapped at the end. """
        another_attack = []
        for ship in self.ships:
            if ship.attack(fleet):
                another_attack.append(ship)
        while another_attack != []:
            yet_another_attack = []
            for ship in another_attack:
                if ship.attack(fleet):
                    yet_another_attack.append(ship)
            another_attack = yet_another_attack
        return
