# Automation Program
# This program is divided into a TK Window component and a Main Functions Component (Main Functions also in turn loads the pyautogui etc)

# colour picker crtl shift a, Type in colour

from tkinter import *
from tkinter import simpledialog
from ctypes import windll  # used for fixing blurry fonts on win 10 and 11 (also  windll.shcore.SetProcessDpiAwareness(1))
# from MainFuncsTestingGround import *
from MainFuncsUserGuidAuto import *
from os.path import exists
import sys
import yaml

class PrintLogger:
    def __init__(self, textbox):
        self.textbox = textbox

    def write(self, text):

        # remove line breaks
        text = text.replace('\n', '') # strip new lines from the print() function calls so that they go onto one line in interface (print automatically adds a /n)

        # ignore blank writes
        if text == '':
            return

        # clear old contents
        self.textbox.delete("1.0", "end")
        # insert latest message
        self.textbox.insert("end", text)

        # keep only one line
        #self.textbox.delete("1.80", "end")

        self.textbox.update_idletasks()

    def flush(self):
        pass

class MainWindow:

    def __init__(self, master, automationObjList,deletedAutomations,config):

        # Master Window
        self.master = master
        self.master.title('One Click 2.6')

        # Initial window size (compact view, not showing extra buttons)
        self.initWinPosHorVert = config["initWinPosHorVert"]
        self.initWinSizeHorVert = config["initWinSizeHorVert"]

        # large window size for making room for extra buttons
        self.largeWinPosHorVert = config["largeWinPosHorVert"]
        self.largeWinSizeHorVert = config["largeWinSizeHorVert"]

        self.master.geometry(self.initWinPosHorVert)  # intial position of the window in the screen (200x300) ("-3300+500")
        self.master.geometry(self.initWinSizeHorVert)  # initial size of the root window (master) (1500x700);

        # if not set, the frames will fill the master window
        # self.master.attributes('-fullscreen', True)
        screenWidth = self.master.winfo_screenwidth()
        screenHeight = self.master.winfo_screenheight()

        self.master.attributes("-topmost", True)

        # Instantiate frames
        self.frame0 = Frame(self.master, bd=5, padx=5, bg='#606266')  # Top long row
        self.frame1 = Frame(self.master, bd=5, padx=5, bg='#2a2b2b')  # Side Column for buttons to run automations
        self.frame2 = Frame(self.master, bd=5, padx=5, bg='#FFC672')  # Main frame used for creating automations
        self.frame3 = Frame(self.master, bd=5, padx=5, bg='#FFC692')  # Bottom frame for posting messages

        # Place frames
        self.frame0.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.frame1.grid(row=1, column=0, columnspan=1, sticky="nsew")
        self.frame2.grid(row=1, column=1, columnspan=1, sticky="nsew")
        self.frame3.grid(row=2, column=0, columnspan=2, sticky="nsew")

        # configure weighting of frames
        self.master.grid_columnconfigure(0, weight=1)  # First int refers to column numberAllows frames to expand as master window expands; weight tells how much of the columns it takes
        self.master.grid_columnconfigure(1, weight=7)  # weight gives 3 times as much column as the other columns
        self.master.grid_rowconfigure(1, weight=1)  # rowconfigure states: first row takes 1 parts of space
        self.master.grid_rowconfigure(2, minsize=30)

        self.frame1.grid_propagate(0)  # When adding widgets maintain weighting of frames
        self.frame2.grid_propagate(0)

        # Default Buttons
        self.createButton = Button(self.frame1, text="Create", width=12, bg="#859AFF", command=lambda: self.createAutomationInterface(self.automationObjList))  # Button for creating a new automation
        self.createButton.pack()

        # this is used to get the exact default button colour regardless of platform progam is run on, hence this button is not packed to screen
        self.colourCheckButton=Button(self.frame1, text="", width=12)
        self.defaultButtonColour=self.colourCheckButton['bg']

        self.textbox = Text(self.frame3, height=1, width=80)
        self.textbox.pack(fill='both', expand=True)

        #self.textbox.insert("end", "Hello textbox")

        # redirect print statements

        sys.stdout = PrintLogger(self.textbox)


        # Button Lists
        self.automationObjList = automationObjList  # Load file storing each Automation Object
        self.buttonList = []  # Holds Button classes for each automation from the loaded Automatins file

        # Deleted Automations (deleted by the use but saved here)
        self.deletedAutomations=deletedAutomations

        # Set up Buttons:
        self.loadButtons()  # Loads the Button classes into the buttonList above from the description list

        frameWidth = 10  # Units are in characters not pixels

        windll.shcore.SetProcessDpiAwareness(1)  # used for fixing blurry fonts on win 10 and 11

    def createAutomationInterface(self, automationObjList):

        '''
        This method loads the buttons needed for building a user generated automation. First it checks if the screen has any buttons
        remaining from a previous creation session and removes them, then it creates the new AutomationSet object, then prompts for the
        name of the new Automation, then finally loads the buttons for the user to build each part of an automation.
        :param automationObjList:
        :return:
        '''

        # buttons from a previous creation of an automation are still up, clear them first so as not to have duplicates
        if self.frame2.winfo_children():

            for widget in self.frame2.winfo_children():
                widget.destroy()

        # instantiate new AutomationSet object first
        automationObjList.append(AutomationSet(logger))

        # Prompt for name of automation before showing the buttons on the screen so that first we get the name, then following that, the actions
        name = simpledialog.askstring("Automation Name", "Give a short one word name to your automation:")
        automationObjList[-1].setName(name)

        self.master.geometry("+1400+200")
        self.master.geometry("500x400") # resize window larger to make room for extra buttons

        Button(self.frame2, text='Add Colour Check + Click', width=30, command=lambda: addColourCheckClick(automationObjList)).pack(pady=3)

        Button(self.frame2, text='Add Simple Click', width=30, command=lambda: addSimpleClick(automationObjList)).pack(pady=3)

        Button(self.frame2, text='Type Text', width=30, command=lambda: addTyping(automationObjList,simpledialog.askstring("Enter Text", "Enter any text desired:"), simpledialog.askstring("Tap Enter", "type 'y' to press enter:"))).pack(pady=3)

        # This button calls the addKeyCombo funcs imported from mainFuncs which needs two args from the user
        Button(self.frame2, text='Add Key Combination', width=30, command=lambda: addKeyCombination(automationObjList, simpledialog.askstring("Hold Key", "type abbreviation for hold key:"), simpledialog.askstring("Tap Key", "type second key:"))).pack(pady=3)

        Button(self.frame2, text='Backspace', width=30, command=lambda: addBackspace(automationObjList,simpledialog.askstring("Press Backspace", "enter number of presses"))).pack(pady=3)

        Button(self.frame2, text='Open File', width=30, command=lambda: addOpenFile(automationObjList,simpledialog.askstring("File Path Only", "Copy and paste file path here"), simpledialog.askstring("File Name and Extension", "Type in exact file name with extension"))).pack(pady=3)

        Button(self.frame2, text='Finish And Save', bg="light green",width=30,command=lambda: self.finishAutomationInterface(automationObjList)).pack(pady=3)

        if name is None:
            return

    def finishAutomationInterface(self, automationObjList):

        'This function bundles two functions into one. It finishes the automation by calling finish, and then clears the frame. Other handy things can allso be added'

        finishAutomation(automationObjList, self)

        if self.frame2.winfo_children():

            for widget in self.frame2.winfo_children():
                widget.destroy()

        # reset interface to its initial size and position
        self.master.geometry(self.initWinPosHorVert)
        self.master.geometry(self.initWinSizeHorVert)


    def refreshFrame1(self):

        self.frame1.update()

    def rightClick(self,event,attribute):

        self.m = Menu(self.master, tearoff=0)
        self.m.add_command(label="Delete", command=lambda: deleteItem(attribute, self.deletedAutomations,self.automationObjList,mainWin))
        self.m.add_command(label="Rename", command=lambda: renameItem(attribute,self.automationObjList,mainWin))
        self.m.add_command(label="Colour", command=lambda: setButtonColour(attribute,self.automationObjList,mainWin))
        self.m.add_command(label="Reload")
        self.m.add_separator()
        self.m.add_command(label="Rename")

        self.m.post(event.x_root, event.y_root)


    def frame(self):
        self.frame2.destroy()

    def clearButtons(self):

        for button in self.buttonList:
            button.destroy()
    def loadButtons(self):

        if self.buttonList != None:
            self.buttonList.clear()

        for object in self.automationObjList:  # take each Automation object and instantiate a Button
            if object.getColour()=='': # if user has not set any colour, get default colour (line below)
                colour=self.defaultButtonColour # acquire dfault colour as set for the system you are running on
            else:
                colour=object.getColour() # if user has set a colour, get that colour
            try: # Try instantiating the button with colour given above, if error arises due to problematic input from user go to except
                self.buttonList.append(Button(self.frame1, text=object.getName(), width=12, bg=colour, command=object.runAutomation))
            except: # If colour is problematic (ie a colour that does not exist) just create button without a colour (defualt colour)
                self.buttonList.append(Button(self.frame1, text=object.getName(), width=12, command=object.runAutomation))

        for button in self.buttonList:  # for each button pack it
            button.pack()
            button.bind("<Button-3>", lambda event, a=button["text"]: self.rightClick(event, a))

    def on_win_request(self,promptText):

        def clearFrames(event):

            self.frame2.destroy()


            # for widget in self.frame2.winfo_children():
            #     widget.destroy()


        label = Label(self.frame2, text=promptText, font=('Ebrima 14'), wraplength=250)  # Label(top, text="Add New Item", font=('Mistral 18 bold')).place(x=150, y=80)

        # Grid Labels
        label.grid(row=1, column=1)  # "New Value",   Note: .grid cannot be placed as a single line code: Label(...).grid(..) as the .grid will actually return None to the program and casue an error

        entry = Entry(self.frame2, width='10')
        entry.grid(row=1, column=2)
        x=entry.get()

        label.update()
        # self.master.update()
        entry.focus_set()
        entry.bind("<Return>", clearFrames)
        # automationEntry.bind('<Return>', self.print1)
        # Process the return key press with parameters
        # executed only when "dialog" is destroyed
        self.frame2.wait_window() # without this the program forges on ahead to the return call which returns nothing
        print("Mini-event loop finished!")
        return x



def main():
    global mainWin  # Global mainWin so as to access the mainWin from functions which may need to call method
    root = Tk()

    if exists('Automations'):  # Returns True if file exists; if true open file and load into list
        with open('Automations', 'rb') as f:  # use wb mode so if file does not exist, it will create one; use rb if only reading
            automationObjList = pickle.load(f)
            f.close()

    else:  # If no file exists intialize list as empty
        automationObjList = []

    # Load Configurations from config YAML file
    if exists('AutoConfig.yaml'):  # Returns True if file exists; if true open file and load into variable
        with open('AutoConfig.yaml', 'r') as f:
            config = yaml.safe_load(f) # loads all settings into a python dictionary. (wxample in a class, self.name = config["name"])
            f.close()

    else:  # If no file exists initialize values to defaults
        print("### the config file was not found, default values have been loaded instead ###")

        winPosHorVer = "+2+118"
        winSizeHorVert = "1800x45"
        mainFrameCol = '#FFC642'

        # Post message to screen if configuration file could not be found
        message('Message', 'The configuration file could not be found, and so the program is loaded with default settings.')

    mainWin = MainWindow(root, automationObjList,deletedAutomations, config)  # Instantiate TK Window with access to automation object list

    root.mainloop()


main()
