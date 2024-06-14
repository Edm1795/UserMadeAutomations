# Automation Program
# This program is divided into a TK Window component and a Main Functions Component (Main Functions also in turn loads the pyautogui etc)

# colour picker crtl shift a, Type in colour

from tkinter import *
from ctypes import windll  # used for fixing blurry fonts on win 10 and 11 (also  windll.shcore.SetProcessDpiAwareness(1))
from MainFuncsTestingGround import *
# from MainFuncsUserGuidAuto import *
from os.path import exists


class MainWindow:

    def __init__(self, master, automationObjList,deletedAutomations):

        # Master Window
        self.master = master
        self.master.title('One Click 1.33')
        self.master.geometry("+1400+200")  # position of the window in the screen (200x300) ("-3300+500")
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
        self.createButton = Button(self.frame1, text="Create", width=12, bg="#859AFF",command=lambda: createAutomation(self.automationObjList,mainWin))  # Button for creating a new automation
        self.createButton.pack()



        # Button Lists
        self.automationObjList = automationObjList  # Load file storing each Automation Object
        self.buttonList = []  # Holds Button classes for each automation from the loaded Automations file

        # Deleted Automations (deleted by the use but saved here)
        self.deletedAutomations=deletedAutomations

        # Set up Buttons:
        self.loadButtons()  # Loads the Button classes into the buttonList above from the description list

        frameWidth = 10  # Units are in characters not pixels



        windll.shcore.SetProcessDpiAwareness(1)  # used for fixing blurry fonts on win 10 and 11

    def refreshFrame1(self):

        self.frame1.update()

    def rightClick(self,event,attribute):

        self.m = Menu(self.master, tearoff=0)
        self.m.add_command(label="Delete", command=lambda: deleteItem(attribute, self.deletedAutomations,self.automationObjList,mainWin))
        self.m.add_command(label="Rename", command=lambda: renameItem(attribute,self.automationObjList,mainWin))
        self.m.add_command(label="Paste")
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






    def print1(self):
        print('works')
        self.entry = Entry(self.frame2, width=10)
        self.entry.pack()

def main():
    global mainWin  # Global mainWin so as to access the mainWin from functions which may need to call method
    root = Tk()

    if exists('Automations'):  # Returns True if file exists; if true open file and load into list
        with open('Automations', 'rb') as f:  # use wb mode so if file does not exist, it will create one; use rb if only reading
            automationObjList = pickle.load(f)
            f.close()
            # print('The speedometer list has been loaded from the config file', *speedometerList)
    else:  # If no file exists intialize list as empty
        automationObjList = []

    mainWin = MainWindow(root, automationObjList,deletedAutomations)  # Instantiate TK Window with access to automation object list

    root.mainloop()


main()
