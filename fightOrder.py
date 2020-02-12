#!/usr/local/bin/python3

import sys


class Game():

    def __init__(self):
        self.actors = {
            
        }

        self.acting = list()

        self.running = False
        self.changed = False

        self.round = 0

    def formatNames(self, names):
        
        if len(names) < 1:
            return "EMPTY"
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
            print("Please enter an Integer!")
            result = self.inputInteger(text)
        return result

    def changeActor(self):
        for x in self.actors:
            print(x)
        print("\n\n\n")
        done = False
        while not done:
            inp = input("Who do you want to change?\n")
            print(inp)
            newInit = input("Enter new Initiative.\n")
            try:
                val = int(newInit)
                self.actors[inp] = val
                done = True
            except Exception as e:
                print(e)
        return

    def addActor(self):
        inp = input("Enter name of new Actor! Leave Blank to abort.\n")

        if inp.lstrip() == "":
            return
        else:
            name = inp
            value = self.inputInteger("Enter Initiative of {}\n".format(name))
            self.actors[name] = value

    def removeActor(self):
        self.showStats()
        inp = input("Who do you want to remove? Leave Blank to abort\n")
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
        if len (self.actors) < 1:
            print ("No Actors! Please Add Actors before you start!")
            return
        self.round += 1
        acting = list()
        changed = False
        for x in self.actors:
            if self.round % self.actors[x] == 0:
                changed = True
                print (self.actors[x])
                acting.append(x)
        self.acting = acting.copy()       
        if not changed:
            self.nextRound()

    def resetGame(self):
        print ("Resetting Gamestate. Please Confirm!\n")
        if self.confirmInput():
            self.round = 0
        else:
            print ("Aborting!")
            return

    def confirmInput(self):
        inp = input ("Are you sure? Y/N?\n")
        if inp.lower() == "y":
            return True
        elif inp.lower() == "n":
            return False
        else:
            print("Invalid Input! Try Again!\n\n\n")
            return self.confirmInput()
    
    
    def run(self):
        while self.running:
            inp = input("At Round {}\n\nIt's {}'s Turn\n\n\nWhat do you want to do?\n\n 1.) To Continue enter N\n 2.) To Change Stats enter C\n 3.) To remove someone enter R\n 4.) To add someone enter A\n 5.) To see the stats enter S   \n\n 6.) to reset the game enter RESET\n\n\n\n ".format(self.round,self.formatNames(self.acting)))

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
                print("Invalid Input\n\n\n")


game = Game()
game.running = True
game.run()
