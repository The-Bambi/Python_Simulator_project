from appJar import gui
from Loader import *
from Fleet import *

"""Main body of the program.
Quentities of each kind of sheep in a fleet can be either entered manually (only natural numbers)
or loaded from specified text file (with format of an example file). 
Fleets can be also saved to a text file (save format same as an example file).
Simulate! button will start the fight. Reset button sets all ship text fields to 0.
Exit closes the program.

After the simulation, a window with pie chart pops up telling how the battles ended.
Close button closes the pie-chart window, Resimulate runs the simulation again with the same settings.

BUG: due to how PieChart is constructed, I had to set initial victory/draw counts to 0.0000000000001. Zero breaks the whole thing.
"""

loader = Loader()
names = loader.long_names

app = gui("Projekcik")
app.setBg("grey")
app.addLabel("Simulator",column=1,colspan=3)


def loadMenu(option):
   if option == "Fleet 1":
      path = app.openBox("Choose Fleet 1 file...")
      file = open(path,'r')
      for line in file.readlines()[1:]:
         type_quantity = line.split()
         index = loader.short_names.index(type_quantity[0])
         name = loader.long_names[index]
         app.setEntry(name+'1',int(type_quantity[1]))
      file.close()
   if option == "Fleet 2":
      path = app.openBox("Choose Fleet 2 file...")
      file = open(path,'r')
      for line in file.readlines()[1:]:
         type_quantity = line.split()
         index = loader.short_names.index(type_quantity[0])
         name = loader.long_names[index]
         app.setEntry(name+'2',int(type_quantity[1]))
      file.close()

def saveMenu(option):
   if option == "Fleet 1":
      path = app.saveBox("Save fleet 1 params as...")
      file = open(path,'w')
      file.write("skrot ilosc\n")
      for index in range(len(names)):
         file.write(loader.short_names[index]+' '+app.getEntry(names[index]+'1')+'\n')
      file.close()
   if option == "Fleet 2":
      path = app.saveBox("Save fleet 2 params as...")
      file = open(path,'w')
      file.write("skrot ilosc\n")
      for index in range(len(names)):
         file.write(loader.short_names[index]+' '+app.getEntry(names[index]+'2')+'\n')
      file.close()


app.createMenu("Load...")
app.addMenuList("Load...",["Fleet 1","Fleet 2"],loadMenu)

app.createMenu("Save...")
app.addMenuList("Save...",["Fleet 1","Fleet 2"],saveMenu)

app.addHorizontalSeparator(row=1,colspan=3,colour='red')
app.addLabels(["Statki","Flota 1","Flota 2"],2,3)


for row,name in enumerate(names,3):
   app.addLabel(name,None,row=row,column=0,colspan=1)
   app.entry(name+'1',label = False, value = 0, row = row, column = 1)
   app.entry(name+'2',label = False, value = 0, row = row, column = 2)


def press(btn):
   if btn == "Exit":
      app.stop()
   if btn == "Close":
      app.destroySubWindow("Scores")
   if btn == "Reset":
      for x in flt1:
         app.setEntry(x,'0')
      for x in flt2:
         app.setEntry(x,'0')
   if btn == "Simulate!" or btn == "Resimulate":
      fleet1 = []
      fleet2 = []
      for name in names:
         fleet1.append(int(app.getEntry(name+'1')))
         fleet2.append(int(app.getEntry(name+'2')))
         
      simulate(fleet1, fleet2)

app.entry("Rounds/simulation",value=6,label=True,col=2,row=17)
app.entry("Simulations:",value=100,label=True,col=1,row=17)

app.addButtons(["Simulate!","Reset","Exit"],press,colspan=3)

def simulate(flt1, flt2):
   f1victories = 0.0000000000001
   f2victories = 0.0000000000001
   draws = 0.0000000000001

   simulations = int(app.getEntry("Simulations:"))
   rounds = int(app.getEntry("Rounds/simulation"))

   for r in range(simulations):
      fleet1 = Fleet(flt1,loader)
      fleet2 = Fleet(flt2,loader)

      for _ in range(rounds):
         fleet1.fire(fleet2)
         fleet2.fire(fleet1)
         fleet1.sweep()
         fleet2.sweep()
         if fleet1.count() == 0 or fleet2.count() == 0:
            break

      if (fleet1.count() > 0 and fleet2.count() > 0) or (fleet1.count() == 0 and fleet2.count() == 0):
         draws += 1
         continue
      elif fleet1.count() == 0:
         f2victories += 1
         continue
      elif fleet2.count() == 0:
         f1victories += 1
         continue

   #print ('f1: ',f1victories, 'f2:', f2victories, 'd: ',draws)
   try:
      app.destroySubWindow("Scores")
   except:
      pass

   scores_dict = {'Victories of 1st fleet':f1victories,'Victories of 2nd fleet':f2victories,'Draws':draws}
   
   app.startSubWindow("Scores")
   app.addPieChart('Of {} simulations'.format(simulations),scores_dict,colspan=2,rowspan=3)
   app.addButton("Close",press,row=4,column=0)
   app.addButton("Resimulate",press,row=4,column=1)
   app.addLabel("Victories of 1st fleet: "+str(int(f1victories)),row=1,column=3)
   app.addLabel("Victories of 2st fleet: "+str(int(f2victories)),row=2,column=3)
   app.addLabel("Draws: "+str(int(draws)),row=3,column=3)
   app.stopSubWindow()
   app.showSubWindow("Scores")


app.go()
   