# Automation Program
# This program is divided into a TK Window component and a Main Functions Component (Main Functions also in turn loads the pyautogui etc)

# colour picker crtl shift a, Type in colour

from tkinter import *
from ctypes import windll  # used for fixing blurry fonts on win 10 and 11 (also  windll.shcore.SetProcessDpiAwareness(1))
from MainFuncsUserGuidAuto import *
from os.path import exists

class MainWindow:

    def __init__(self, master,automationObjList):

        # Master Window
        self.master = master
        self.master.title('User Created Automations 1.2')
        self.master.geometry("+1200+200")  # position of the window in the screen (200x300) ("-3300+500")
        self.master.geometry("500x400")  # set initial size of the root window (master) (1500x700);
        # if not set, the frames will fill the master window
        # self.master.attributes('-fullscreen', True)
        screenWidth = self.master.winfo_screenwidth()
        screenHeight = self.master.winfo_screenheight()

        self.master.attributes("-topmost", True)

        # Instantiate frames
        self.frame0 = Frame(self.master, bd=5, padx=5, bg='#606266')  # Top long row
        self.frame1 = Frame(self.master, bd=5, padx=5, bg='#2a2b2b')  # Side Column
        self.frame2 = Frame(self.master, bd=5, padx=5, bg='#FFC672')  # Main frame

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
        self.createButton = Button(self.frame1, text="Create", width=12, command=lambda:createAutomation(automationObjList))  # Button for creating a new automation
        self.createButton.pack()

        # Button Lists
        self.automationObjList = automationObjList # Load file storing each Automation Object
        self.buttonList = [] # Holds Button classes for each automation from the loaded Automations file

        # Set up Buttons:
        self.loadButtons() # Loads the Button classes into the buttonList above from the description list

        frameWidth = 10  # Units are in characters not pixels

        windll.shcore.SetProcessDpiAwareness(1)  # used for fixing blurry fonts on win 10 and 11

        #  Entry widgets
        self.entry = Entry(self.frame0, width=10)
        self.entry.pack()

    def loadButtons(self):
        for object in self.automationObjList: # take each Automation object and instantiate a Button
            self.buttonList.append(Button(self.frame1, text=object.getName(), width=12, command=lambda:object.runAutomation()))
        for button in self.buttonList: # for each button pack it
            button.pack()





def main():

    global mainWin  # Global mainWin so as to access the mainWin from functions which may need to call method
    root = Tk()

    if exists('Automations'):  # Returns True if file exists; if true open file and load into list
        with open('Automations', 'rb') as f:  # use wb mode so if file does not exist, it will create one; use rb if only reading
            automationObjList = pickle.load(f)
            f.close()
            # print('The speedometer list has been loaded from the config file', *speedometerList)
    else: # If no file exists intialize list as empty
        automationObjList=[]

    mainWin = MainWindow(root,automationObjList) # Instantiate TK Window with access to automation object list

    root.mainloop()


main()
