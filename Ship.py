class Ship:
    """General ship class. 
    :param stats: list of stats passed from loader - [short name, name, hp, shield, attack power]
    :param quick_cannons: dictionary taken from loader appriopriate to the ship type.
    """
    def __init__(self,stats,quick_cannons):
        self.attack_power = stats[4]
        self.max_shield = stats[3]
        self.current_shield = stats[3]
        self.max_hp = stats[2]
        self.current_hp = stats[2]
        self.name = stats[1]
        self.short_name = stats[0]
        self.quick_cannons = quick_cannons


    def __repr__(self):
        return repr(self.name)


    def attack(self, fleet):
        '''Functions that attacks. 
        :param fleet: enemy fleet object
        It takes an object of targeted fleet as an agrument, picks at random the attack target,
        calculates the damage and a chances for another attack. Returns True/False as an indicator whether to attack again
        thanks to quick_cannons.'''
        from random import choice

        target = choice(fleet.ships) #choose a target from enemy fleet

        if self.attack_power < target.max_shield/100: #attack fails if self's attack is < 1/100 of enemy's shield
            return 

        projectile = self.attack_power #copy of attack power to avoid modifying object's stuff
        projectile = projectile - target.current_shield #weaken the projectile by the value of shield

        if target.current_shield - self.attack_power < 0: #compare to attack, projectile was modified
            target.current_shield = 0
        else:
            target.current_shield = target.current_shield - self.attack_power
        
        if projectile > 0:
            target.current_hp = target.current_hp - projectile #damage the ship.

        if target.current_hp/target.max_hp < 0.7:
            exploded = self.lottery(target.current_hp/target.max_hp)
            if exploded:
                target.current_hp = 0
        
        qcannons = self.quick_cannons[target.short_name]

        quick_attack = False

        if qcannons > 1:
            if (self.lottery(1-1/qcannons)):
                quick_attack = True

        return quick_attack


    def lottery(self, chances):
        """Calculates chances
        :param chances: number 0-1."""
        from random import randrange
        draw = randrange(100)
        return draw<(chances*100)

    def stats(self):
        '''Displays stats of a unit.'''
        return "Name: {}, HP: {}/{}, shield: {}/{}".format(self.name, self.current_hp, self.max_hp, self.current_shield, self.max_shield)