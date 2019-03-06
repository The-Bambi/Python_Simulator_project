class Loader:
    """Class that reads and holds stats of ships, dictionary of dictionaries of quick cannons data,
    and can pass useful stuff like names of all ships."""
    def __init__(self):
        file = open('ships','r')
        self.data = {}
        self.short_names = []
        self.long_names = []
        for index,line in enumerate(file.readlines()[1:]):
            ship_stats = line.split()
            self.data[ship_stats[0]] = [ship_stats[0], ship_stats[1]]+[int(x) for x in ship_stats[2:]]
            self.short_names.append(ship_stats[0])
            self.long_names.append(ship_stats[1])
        file.close()

        file = open('quick_cannons','r')
        self.quick_cannons = {}
        versus = file.readline().split()[1:]
        for line in file.readlines():
            line = line.split()
            line = [line[0]]+[int(x) for x in line[1:]]
            self.quick_cannons[line[0]] = dict(zip(versus,line[1:]))
        file.close()