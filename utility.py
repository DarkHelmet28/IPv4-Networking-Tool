import os
from termcolor import colored

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def textYellow(text):
    return colored(text, "yellow")

def textYellowBold(text):
    return colored(text, "yellow", attrs=["bold"])