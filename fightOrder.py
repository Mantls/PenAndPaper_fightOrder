#!/usr/local/bin/python3

import sys
import os


class Game():

    def __init__(self):
        self.actors = dict()
        self.acting = list()

        self.running = False
        self.changed = False

        self.round = 0

    def prepareWarmstart(self):
        dirname = os.path.dirname(os.path.abspath(__file__))
        print ("Writing warmstart config to: {}".format(dirname + "/.warmstartConfig"))
        with open(dirname + "/.warmstartConfig","w") as f:
            string = ""
            for actor in self.actors:
                val = self.actors[actor]
                string += "{},{}\n".format(actor, val)
            f.write(string)

    def readWarmStart(self):
        try:
            with open((os.path.dirname(os.path.abspath(__file__)) + "/.warmstartConfig"),"r") as f:
                for line in f:
                    if not line.rstrip() == "":
                        split = line.rstrip().split(",")
                        actor = split[0]
                        val = int (split[1])
                        self.actors[actor] = val
            print("Loaded WarmstartConfig with the following actors!\n")
            self.showStats()
        except Exception as e:
            print(e)


    def formatNames(self, names):

        if len(names) < 1:
            return "Nobody"
        if len(names) == 1:
            return names[0]
        else:
            result = ""
            for index, val in enumerate(names):
                if index > 0:
                    result += " "
                if index == len(names) - 1:
                    result += "and "
                result += val
                if index > 0 and index < (len(names) - 1):
                    result += ","
            return result

    def inputInteger(self, text):
        try:
            result = int(input(text))
        except ValueError:
            print("Please enter an integer!")
            result = self.inputInteger(text)
        return result

    def changeActor(self):
        for x in self.actors:
            print(x)
        print("\n\n\n")
        done = False
        while not done:
            inp = input("Who do you want to change? Leave blank to abort\n")
            if inp.lstrip() == "":
                break
            if inp not in self.actors:
                print ("{} is not an actor. Please enter a valid actor or add the actor first!".format(inp))
                continue
            newInit = input("Enter new initiative for {}.\n".format(inp))
            try:
                val = int(newInit)
                self.actors[inp] = val
                done = True
            except Exception as e:
                print(e)
        return

    def addActor(self):
        inp = input("Enter name of new actor! Leave blank to abort.\n")

        
        if inp.lstrip() == "":
            return
        
        if inp in self.actors:
            print("{} is alread an actor! Try again!".format(inp))
            self.addActor()
        else:
            name = inp
            value = self.inputInteger("Enter initiative of {}\n".format(name))
            self.actors[name] = value

    def removeActor(self):
        self.showStats()
        inp = input("Who do you want to remove? Leave blank to abort\n")
        if inp.lstrip() == "":
            return
        try:
            self.actors.pop(inp)
        except KeyError:
            print("Invalid Input! Please try again!\n")
            self.removeActor()

    def showStats(self):
        print("Actor / Initiative")
        print("---------------")
        for x in self.actors:
            print("{}: {}".format(x, self.actors[x]))
        print("---------------")
        print("\n\n\n\n\n")

    def nextRound(self):
        if len(self.actors) < 1:
            print("No actors! Please add actors before you start!")
            return
        self.round += 1
        acting = list()
        changed = False
        for x in self.actors:
            if self.round % self.actors[x] == 0:
                changed = True
                print(self.actors[x])
                acting.append(x)
        self.acting = acting.copy()
        if not changed:
            self.nextRound()

    def resetGame(self):
        print("Resetting Gamestate. Please confirm!\n")
        if self.confirmInput():
            self.round = 0
        else:
            print("Aborting!")
            return

    def confirmInput(self):
        inp = input("Are you sure? Y/N?\n")
        if inp.lower() == "y":
            return True
        elif inp.lower() == "n":
            return False
        else:
            print("Invalid input! Try again!\n\n\n")
            return self.confirmInput()

    def run(self):
        while self.running:
            inp = input("At Round {}\n\nIt's {}'s Turn\n\n\nWhat do you want to do?\n\n 1.) To continue enter N\n 2.) To change stats enter C\n 3.) To remove someone enter R\n 4.) To add someone enter A\n 5.) To show the stats enter S   \n\n 6.) to reset the game enter RESET\n\n\n\n ".format(
                self.round, self.formatNames(self.acting)))

            if inp.lower() == "n":
                self.nextRound()
            elif inp.lower() == "c":
                self.changeActor()
            elif inp.lower() == "r":
                self.removeActor()
            elif inp.lower() == "a":
                self.addActor()
            elif inp.lower() == "s":
                self.showStats()
            elif inp.lower() == "reset":
                self.resetGame()
            else:
                print("Invalid input\n\n\n")


game = Game()
game.running = True
try: 
    if sys.argv[1] == "-w":
        print ("Reading /.warmstartConfig")
        game.readWarmStart()
    game.run()
except KeyboardInterrupt:
    print("\nPerforming shutdown")
    game.prepareWarmstart()
    print("Goodbye!")