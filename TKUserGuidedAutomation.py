 # colour picker crtl shift a, Type in colour

from tkinter import *
from ctypes import windll  # used for fixing blurry fonts on win 10 and 11 (also  windll.shcore.SetProcessDpiAwareness(1))



class MainWindow:

    def __init__(self, master):

        # Master Window
        self.master = master
        self.master.title('User Guided Automations. 0.0')
        self.master.geometry("+150+500")  # position of the window in the screen (200x300) ("-3300+500")
        self.master.geometry("500x400")  # set initial size of the root window (master) (1500x700);
        # if not set, the frames will fill the master window
        # self.master.attributes('-fullscreen', True)
        screenWidth = self.master.winfo_screenwidth()
        screenHeight = self.master.winfo_screenheight()

        self.master.attributes("-topmost", True)

        # Instantiate frames
        self.frame0 = Frame(self.master, bd=5, padx=5, bg='#606266')  # Top long row
        self.frame1 = Frame(self.master, bd=5, padx=5, bg='#2a2b2b')  # Side Column
        self.frame2 = Frame(self.master, bd=5, padx=5, bg='#7E050C')  # Main frame

        # Place frames
        self.frame0.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.frame1.grid(row=1, column=0, columnspan=1, sticky="nsew")
        self.frame2.grid(row=1, column=1, columnspan=1, sticky="nsew")

        # configure weighting of frames
        self.master.grid_columnconfigure(0, weight=1)  # First int refers to column numberAllows frames to expand as master window expands; weight tells how much of the columns it takes
        self.master.grid_columnconfigure(1, weight=7)  # weight gives 3 times as much column as the other columns
        self.master.grid_rowconfigure(1, weight=1)  # rowconfigure states: first row takes 1 parts of space

        self.frame1.grid_propagate(0)  # When adding widgets maintain weighting of frames
        self.frame2.grid_propagate(0)

        # Default Buttons
        self.createButton = Button(self.frame1, text="Create", width=12, command=lambda:createAutomation()) # Button for creating a new automation
        self.createButton.pack()
        self.button1 =      Button(self.frame1, text="Schedule", width=12, command=lambda: self.schedule('schedule button'))
        # Button Lists
        self.descrList=[['a'],['b']]
        self.buttonList=[]

        # Set up Buttons:
        self.loadButtons()

        # sundries
        self.counter=0 # counter used for determining state of toggle switch used in transparency button

        frameWidth = 10  # Units are in characters not pixels

        windll.shcore.SetProcessDpiAwareness(1)  # used for fixing blurry fonts on win 10 and 11


        #  Entry widgets
        self.entry = Entry(self.frame0, width=10)
        self.entry.pack()



        self.button1 = Button(self.frame1, text="Schedule", width=12, command=lambda: self.schedule('schedule button'))
        self.button1.pack()

        self.button2 = Button(self.frame1, text="Screen Shot", width=12, command=self.setCount)
        self.button2.pack()


    def loadButtons(self):
        for description in self.descrList:
            self.buttonList.append(Button(self.frame1, text=description[0], width=12,command=lambda:self.schedule('This button works.')))
        for button in self.buttonList:
            button.pack()


    def schedule(self,text):
        print(text)

    def setCount(self):
        pass

def createAutomation():
    '''
    This function takes the user through a series of prompts in order to set up a new automation.
    The user will need to decide what type of action is needed for each step of their new automation.
    For example does it require a click of the mouse, and does it require confirming if a given button
    is even going to be loaded on the screen. Will text need to be inputed etc.
    :return: none
    inputs: none
    '''

    ##########################################################
    ##### Gathering User's Plans for an Automation Loop ######
    ##########################################################

    runMainLoop = True

    while runMainLoop:  # loop for gathering input from user. Stopping this loop will move out of the user gathering mode and into run mode

        mainRawInput = input('Press\n1 for move mouse and click\n2 to type\n3 to finish and save\n')  # prompt user

        if mainRawInput == '1':  # if user wants to add mouse moves
            rawInput = input('Press\n1 to add a colour check for a web element\n2 to simply click mouse (without colour check)\n')  # mouse only, or with colour check

            if rawInput == '1':  # if adding colour check
                print('Use Main Monitor Only: Place mouse over the top of a stable coloured element of the program or website -- 5 seconds\n')
                time.sleep(5)
                posAndCol = checkForElement.getColour()  # returns tuple of mouse pos, colour ((x,y),(r,g,b)) ## Takes colour from main monitor only
                print('## Colour value acquired ##')
                funcOutlineList.append(['checkForElement.confirmColour', posAndCol])
                rawInput2 = input('Press\nNow move mouse to clicking position and press 1\n')
                if rawInput2 == '1':
                    print(
                        'Keep mouse in position -- 3 seconds\n')  # prompt user to move mouse into desired position
                    time.sleep(3)  # give 3 seconds to user to move mouse
                    mousePos = ag.position()  # get position of mouse as tuple (x,y)
                    funcOutlineList.append(['taskSet1.moveMouse', mousePos, 0.5,
                                            'y'])  # append function call and arguments with delay and click
                    print('Click position information complete, thank you.\n')

            if rawInput == '2':
                print(
                    'Move mouse into clicking position -- 3 seconds\n')  # prompt user to move mouse into desired position
                time.sleep(3)  # give 3 seconds to user to move mouse
                mousePos = ag.position()  # get position of mouse as tuple (x,y)
                funcOutlineList.append(['taskSet1.moveMouse', mousePos, 0.5,
                                        'y'])  # append function call and arguments with delay and click

        if mainRawInput == '2':
            rawText = input('Type the text you want entered:')  # prompt user to move mouse into desired position
            enter = input("press 'y' to add enter")
            if enter == 'y':
                funcOutlineList.append(
                    ['taskSet1.type', rawText, 'y'])  # append function call and arguments with delay and click
            else:
                funcOutlineList.append(
                    ['taskSet1.type', rawText, 'n'])  # append function call and arguments with delay and click

        if mainRawInput == '3':  # if user wants to complete building the sequence of clicks
            print('**** Automation file saved.  All is Complete')
            saveFile(funcOutlineList, "Automations")
            runMainLoop = False

def main():
    global mainWin  # Global mainWin so as to access the mainWin from functions which may need to call method
    root = Tk()
    mainWin = MainWindow(root)

    root.mainloop()


main()
