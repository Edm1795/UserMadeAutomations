### Note: import pillow version 10.2.0 on the pycharm editor rather than the latest version, otherwise there is no compatibility. Pillow is used by pyautogui

# The class holding the actual automation information for a single unified set of automations. The name of the automation, the description of each step
# and the ability to create the functions

##### Adding New Functions Instructions ######

### There are mulitiple steps to adding a new function

# 1. make the button in the TK module by copying the pattern set by any of the other buttons
# 2. add the needed function from the official PYautogui module by looking it up online and put this into the PYautogui class in this code here
# 3. add the correct line to writeOutlineofFunctions (a standalone function in this file)
# 4. add a "add.... function to the standalone functions in this file
# 5. add a func. to the build actual functions list in AutomationSet class
# 6. add to a call to the runActualFuncsList in the AutomationSet class


import pyautogui as ag
import time
import os
import datetime
import pickle
import logging
from os.path import exists
import yaml
import webcolors

# List holding all individual automation objects; used by createAutomation function
automationObjList=[] # List of the class AutomationSet
deletedAutomations=[]

print('at orif module',len(automationObjList))
print(id(automationObjList))

# Load Configurations from config YAML file same as used for interface but this module will only use relevant ones for this module
if exists('AutoConfig.yaml'):  # Returns True if file exists; if true open file and load into variable
    with open('AutoConfig.yaml', 'r') as f:
        config = yaml.safe_load(f) # loads all settings into a python dictionary. (wxample in a class, self.name = config["name"])
        f.close()

else:  # If no file exists initialize values to defaults
    print("### the config file was not found, default values have been loaded instead ###")

    # Config values inside dictionary with default values (loads after closing messagebox)
    config = {"winPosHorVer":"+2+118","winSizeHorVert":"1800x45","mainFrameCol":"#FFC642","initWinPosHorVert":"+1600+200","initWinSizeHorVert" : "250x400","largeWinPosHorVert":"1400x200","largeWinSizeHorVert":"500x400","colTolerance":"20"}




class Logger:

    '''
    A class for logging all actions taken by the PYautogui and CheckForElem class
    '''

    def __init__(self):

        logging.basicConfig(filename='AutomationLog.txt',level=logging.INFO,format='%(asctime)s - %(message)s')

    def log(self, message):

        logging.info(message)

logger=Logger() # instantiate logger globally after defining the class, then use this object inside any class needed

class PYautogui:

    '''
    Class of PY Autogui functions
    '''

    def __init__(self,logger):

        self.logger=logger


    def moveMouse(self, horiz, vert, time, click):
        '''
        Inputs: int: horizontal and vertical position where the mouse must end up
        Time: int: mount of time to take to get pointer to its position
        click: a str value of 'y' if a click is desired at final position
        '''

        ag.moveTo(horiz, vert, duration=time)

        if click == 'y':
            ag.click()
        else:
            pass

        self.logger.log(f'Moving mouse to: {horiz}, {vert} time: {time}')

    def click(self):
        '''
        Clicks the mouse
        '''
        ag.click()

        self.logger.log(f'Mouse clicked')

    def drag(self, horiz, vert, duration, button):

        if button == 'l':
            button = 'left'
        if button == 'r':
            button = 'right'
        ag.dragTo(horiz, vert, button=button, duration=duration)

        self.logger.log(f'Mouse dragged: {horiz}, {vert} ,{button}, time: {time}')

    def backspace(self,numOfPresses):

        ag.press('backspace',presses=int(numOfPresses))

        self.logger.log(f'Key pressed:    backspace, pressed: {numOfPresses} times')


    def pressKeys(self, holdKey, secondKey):

        '''
        Double key press function: eg, ctrl + a
        Inputs: holdKey: str key to hold down, eg: ctrl or shift
        secondKey:  str second key to press eg, a
        '''
        ag.keyDown(holdKey)  # hold down the shift key
        ag.press(secondKey)  # press the left arrow key
        ag.keyUp(holdKey)

        self.logger.log(f'Keys pressed:    {holdKey}, {secondKey}')

    def pressThreeKeys(self, holdKey, secondHoldKey, thirdKey):
        '''
        Triple key press function: eg: ctrl + shit + a
        Inputs: holdKey: str key to hold down, eg: ctrl or shift
        secondHoldKey:  str second key to press eg, shift
        thirdKey: same as secondHoldKey
        '''
        print('three keys initiated')
        ag.hotkey(holdKey, secondHoldKey, thirdKey)

        self.logger.log(f'Keys pressed:    {holdKey}, {secondHoldKey},{thirdKey}')

    def type(self, letters, enter='n'):
        '''
        Types keyboard input to the cursor. It also checks if the text sent in is a password or not by checking for
        the 'pass' prefix to the inputted text

        Inputs: letters: a sequence of strings to be typed
        Enter: a str 'y' or 'n', if you want to press the enter key after inputing letters
        '''
        if letters[:4]=='pass':
            textWithoutPass=letters[4:]
            ag.write(textWithoutPass)
        else:
            ag.write(letters)

        if enter == 'y':
            time.sleep(0.5)  # used to add gap between text input and pressing enter
            ag.press('enter')
        if enter =='n':
            pass

        if letters[:4]=='pass':
            self.logger.log(f'text typed:      {'password entered'}, enter pressed: {enter}')
        else:
            self.logger.log(f'text typed:      {letters}, enter pressed: {enter}')

    def openFile(self,filePath,fileName):
        '''
        This uses the os module to open files. From the prompts to the user, this gets the file path and file name
        which are then used by os to open the file
        :param filePath: str of file path eg: C:/Documents
        :param fileName: str of file name and extension eg: dates.doc, list.pdf
        :return: none
        '''
        filePathandName=filePath+fileName
        os.startfile(filePathandName)

        self.logger.log(f'File Opened:      {fileName}, Path:  {filePath}')

class CheckForElem:

    '''
    Class for checking given elements are present on the screen. For example checks if a certain word is present
    or a certain colour of pixel
    '''

    def __init__(self,logger,colTolerance):

        self.logger=logger
        self.colTolerance=colTolerance #int value of the amount of colour tolerance desired when matching colours. Often set to about 20 for each rgb portion

    def confirmImage(self, image, sector, topLeftx=0, topLefty=0, bottomRightx=0, bottomRighty=0):

        '''
        Confirms if a given element is present on the screen.
        input: image: str of image to search for in the screen ('image.png')
        inputs: sector: str defining which sector of screen to search for desired element
            Exact values of box to check for element (if not using a general sector of the screen
        output: True if and when the element (the image sent in) is found
        '''

        if sector == 'c':  # Centre Section: set screenshot region for small box in centre of the screen
            regValues = (756, 410, 400, 400)
        if sector == 'cr': # Screenshot for centre right
            regValues = (1000, 380, 500, 500)
        if sector == 'n':  # If no sector is used, load in exact values of box to check for element
            regValues = (topLeftx, topLefty, bottomRightx, bottomRighty)

        loop = True
        while loop:

            if ag.locateOnScreen(image, region=regValues) == None:
                continue
            else:
                loop = False

        return True

    def getClosestColorName(self,rgbTuple):
        minDistance = float("inf")
        closestName = None

        for name in webcolors.names():
            rgbReference = webcolors.name_to_rgb(name)

            rd = (rgbReference[0] - rgbTuple[0]) ** 2
            gd = (rgbReference[1] - rgbTuple[1]) ** 2
            bd = (rgbReference[2] - rgbTuple[2]) ** 2

            distance = rd + gd + bd

            if distance < minDistance:
                minDistance = distance
                closestName = name

        return closestName
    def confirmColour(self, x, y, colour):

        '''
        Confirms an element is present by matching a colour expected to a colour on the screen
        :param x: x coordinate of pixel to test its colour
        :param y: y coordinate of pixel to test its colour
        :param colour: a tuple (r,g,b) given in parantheses
        :return: True once the colour is detected
        '''

        # This is now set at the instantiation of the CheckForElem from the config file class above and can be called anytime; self.colTolerance
        # tolVal=60 # value of colour tolerance for each base colour r,g,b (Eg: If red should be 100, but in fact is 200, still confirms as true) \


        loop = True

        while loop:

            current = ag.pixel(x, y)

            match = all(abs(current[i] - colour[i]) <= self.colTolerance for i in range(3)) # check that all 3 r.g.b match the needed colour within a range of tolerance

            if match: #if match (True) stop loop
                loop = False
            else: # if match (False) delay then continue loop
                time.sleep(0.01)

        print("Colour confirmed")
        print("Target:", colour)
        print("Found:", current)

        colourName=self.getClosestColorName(colour)
        currentColName=self.getClosestColorName(current)

        self.logger.log(f'Colour confirmed. (Checking for this colour value: {colour}, ({colourName}) at {x}, {y}. Colour found: {current} ({currentColName}). Tolerance value: {self.colTolerance})')

        time.sleep(0.1)
        return True

    def getColour(self):

        '''
        Gets the colour value of the pixel at the current position of the mouse
        :return: a tuple of two tuples, the mouse position and colour value at that position ((x,y),(r,g,b))
        '''
        mousePos = ag.position() # get position of the mouse (x,y)
        return (mousePos,ag.pixel(mousePos[0],mousePos[1])) # return the pixel value for the given mousePos ((x,y),(r,g,b))

    def getColourDelayed(self):

        '''
        Gets the colour value of the pixel at the current position of the mouse and delays between getting the coordinates
        and getting the colour; this allows acquiring the correct colour for elements that change colour when hovering over them
        with the mouse. You can get the coordinates, then move the mouse, then get the colour.
        :return: a tuple of two tuples, the mouse position and colour value at that position ((x,y),(r,g,b))
        '''
        mousePos = ag.position() # get position of the mouse (x,y)
        print('Mouse position acquired.')
        print('Move the mouse off of the element - 3 seconds')
        time.sleep(3)
        print(mousePos,ag.pixel(mousePos[0],mousePos[1]))
        return (mousePos,ag.pixel(mousePos[0],mousePos[1])) # return the pixel value for the given mousePos ((x,y),(r,g,b))

class TimeValues:
    '''
    A class which holds a variety of time values to use for moving the mouse accross the screen.
    This standardizes the timings for automation and allows for easy alteration of timings across
    the whole program. Upon instantiation you can choose a speed range such as 'f' for fast where all
    values are set to shorter (and thus faster) timings.

    Note: Values have to be calibrated carefully so as to be quick but also not too fast otherwise websites can't handle the speed.

    Inputs: str: 'f' gives all fastest values; 'm' gives medium values; 's' gives slow values
    '''

    def __init__(self, speed):
        if speed == 'f':
            self.fast = 0.1
            self.med = 0.2
            self.slow = 0.3
        if speed == 'm':
            self.fast = 0.2
            self.med = 0.3
            self.slow = 0.5

    def getFast(self):
        return self.fast

    def getMed(self):
        return self.med

    def getSlow(self):
        return self.slow


class AutomationSet:

    '''
    Objects of this class are the crux of the program. These objects contain all of the automation movements and actions created by the
    createAutomation function. It also builds the real code for each automation, and runs that code.
    '''

    def __init__(self,logger):

        self.logger=logger

        self.name=None # Name of the Automation Set. Eg: Email, Booking, Schedule
        self.briefDescription=None # Brief description of the automation
        self.outlineOfFunctions=[] # List of functions and arguments in sequence in string form (used for building the real functions)

        # The actual function calls needs to be rebuilt everytime the program is restarted because func references do not remain constant
        # after restarting the program
        self.actualFunctions=[] # List of real functions in sequence built using the outlineOfFuncCalls directly above.

        # self.logger = Logger() # Instantiate the logger and send into the PYautogui class

        self.pyAutogui=PYautogui(self.logger) # Instantiate the PYautogui class which contains all methods for automating
        self.checkForElement=CheckForElem(self.logger,config["colTolerance"]) # Instantiate CheckFor Element class; access the config dict to get coltolerance value

        # Colour of button on interface as hex str
        self.buttonColour=''


    def setName(self,name):
        '''
        Single word name given to the automation which becomes the title of the button on screen and given by the user.
        :param name: str: one word which can fit inside the button
        '''

        self.name=name

    def setBriefDescription(self,description):

        self.briefDescription=description

    def getName(self):

        return self.name

    def setColour(self,colour):
        '''
        Set colour of button on interface
        :param colour: str of hex '#000000'
        '''

        self.buttonColour=colour

    def getColour(self):

        try:
            return self.buttonColour
        except:
            pass

    def showOutlineOfFunctions(self):

        return automationObjList


    def writeOutlineOfFunctions(self,function):

        '''
        This method accesses the outlineOfFunctions list and appends a string name of the function and any needed arguments
        needed for a list of sequential automations. This list is then used to build the list of real functions. This method is
        used during the createAutomation phase when the user is building their sequence of automations. By thye time they
        have finished all the screen prompts asking for input, this list will be full

        :param str: function and any needed int, or str: arguments (variety of types depending on what is needed:
        Structure of List: A list of lists, where each inner list is one independent move:
        [['pyAutogui.moveMouse', Point(x=-327, y=67), 0.5, 'y'], ['pyAutogui.moveMouse', Point(x=-94, y=20), 0.5, 'y']]
        '''

        # append a function and any needed arguments to the sequential outline of functions
        self.outlineOfFunctions.append(function)

    def getOutlineOfFunctions(self):

        return self.outlineOfFunctions

    def buildActualFuncsList(self):

        '''
        This very important method uses the outlineOfFuncCalls list (which is saved to an external file) to build
        the actualFunctions list of both the function calls and any necessary arguments. It is called upon starting
        the program so that all function calls will have an updated reference in memory. Note this list can not be used
        for calling the functions because the arguments are not formatted yet. the RunAutomation method does the actual
        calling.
        :return: none
        Inputs: none
        '''

        ### Build the Function List (actualFuncCalls) from the Outline of Functions List (outlineOfFuncCallst) ###
        if len(self.actualFunctions)==0:

            for itemList in self.outlineOfFunctions:  # access the itemList in the itemList [['function name as string',parameters]]
                if itemList[0] == 'pyAutogui.moveMouse':  # if needing moveMouse, input moveMouse function with parameters
                    self.actualFunctions.append([self.pyAutogui.moveMouse, itemList[1], itemList[2], itemList[3]])
                elif itemList[0] == 'checkForElement.confirmColour':  # if needing a colour check (element check), input colour check function with parameters
                    self.actualFunctions.append([self.checkForElement.confirmColour, itemList[1]])
                elif itemList[0] == 'pyAutogui.type':  # if needing to type characters  input type function
                    self.actualFunctions.append([self.pyAutogui.type, itemList[1], itemList[2]])
                elif itemList[0] == 'pyAutogui.pressKeys':  # if needing to press a key combination (hotkeys)
                    self.actualFunctions.append([self.pyAutogui.pressKeys, (itemList[1][0], itemList[1][1])])  # arguments come inside a tuple (holdKey,tapKey)
                elif itemList[0] == 'pyAutogui.pressThreeKeys':  # if needing to open a file
                    self.actualFunctions.append([self.pyAutogui.pressThreeKeys, (itemList[1][0], itemList[1][1], itemList[1][2])])  # args are a tuple of three values (hold key, secondkey, third key)
                elif itemList[0] == 'pyAutogui.openFile':  # if needing to open a file
                    self.actualFunctions.append([self.pyAutogui.openFile, (itemList[1][0], itemList[1][1])])  # arguments are filepath and filename
                elif itemList[0] == 'pyAutogui.backspace':  # if needing to open a file
                    self.actualFunctions.append([self.pyAutogui.backspace, (itemList[1])])  # arguments are number of presses on backspace key

    def runAutomation(self):
        '''
        This method is called by the buttons on the interface and it runs the list of automation function calls from the actualFunctions list.
        It calls the functions in order from the list and adds formats the arguments if needed
        :return: none
        '''

        self.buildActualFuncsList()  # Build the actual functions. This populates the actualFunctions list with the callable functions
        ###### Running the User's Set of Automations ######

        # Run the list of function calls with arguments
        print('Running automation\n')

        self.logger.log("===========================================================")
        self.logger.log("#### Initiating Automation for " + self.getName() + " ####") # Log the name of the automation before all of the actual functions


        for itemList in self.actualFunctions:  # access the list in the list
            if itemList[0] == self.pyAutogui.moveMouse:
                itemList[0](itemList[1][0], itemList[1][1], itemList[2],itemList[3])  # access each item in the internal list and input arguments
            elif itemList[0] == self.checkForElement.confirmColour:
                itemList[0](itemList[1][0][0], itemList[1][0][1], (itemList[1][1]))  # [function,((x,y),(r,g,b))]
            elif itemList[0] == self.pyAutogui.type:
                itemList[0](itemList[1], itemList[2])  # [function,((x,y),(r,g,b))]
            elif itemList[0] == self.pyAutogui.pressKeys:
                itemList[0](itemList[1][0], itemList[1][1])  # [function,(holdKey,tapKey)]
            elif itemList[0] == self.pyAutogui.pressThreeKeys:
                itemList[0](itemList[1][0], itemList[1][1], itemList[1][2])  # [function,(holdKey,secondKey,thirdkey)]
            elif itemList[0] == self.pyAutogui.openFile:
                itemList[0](itemList[1][0], itemList[1][1])  # [function,(fileName,filePath)]
            elif itemList[0] == self.pyAutogui.backspace:  # [function,(numOfPresses)]
                itemList[0](itemList[1])



def addColourCheckClick(automationObjList):

    checkForElement = CheckForElem(logger,config["colTolerance"])  # Instantiate a Check for Element Class (contains methods needed for checking colours)
    #automationObjList.append(AutomationSet(logger))  # Instantiate an AutomationSet Object

    print('Place mouse over top of coloured element - 4 seconds')

    time.sleep(4)

    posAndCol = checkForElement.getColourDelayed()

    print('## Colour value acquired ##') #

    automationObjList[-1].writeOutlineOfFunctions(['checkForElement.confirmColour', posAndCol])

    print('Move mouse to click position -- 3 seconds')

    time.sleep(3)

    mousePos = ag.position()

    automationObjList[-1].writeOutlineOfFunctions(['pyAutogui.moveMouse', mousePos, 0.5, 'y'])

    print('Click-position information complete.')

def addSimpleClick(automationObjList):

    print('Move mouse to click position - 4 seconds')

    time.sleep(4)

    mousePos = ag.position()

    automationObjList[-1].writeOutlineOfFunctions(['pyAutogui.moveMouse', mousePos, 0.5, 'y'])

    print('Mouse click position acquired.')


def addTyping(automationObjList, rawText, enter):

    if enter == 'y':

        automationObjList[-1].writeOutlineOfFunctions(['pyAutogui.type', rawText, 'y'])

    else:

        automationObjList[-1].writeOutlineOfFunctions(['pyAutogui.type', rawText, 'n'])


def addPassword(automationObjList, rawText, enter):

    if enter == 'y':

        automationObjList[-1].writeOutlineOfFunctions(['pyAutogui.type', 'pass'+rawText, 'y'])

    else:

        automationObjList[-1].writeOutlineOfFunctions(['pyAutogui.type', 'pass'+rawText, 'n'])

def addKeyCombination(automationObjList, holdKey, tapKey):

    automationObjList[-1].writeOutlineOfFunctions(['pyAutogui.pressKeys', (holdKey, tapKey)])

def addThreeKeyCombination(automationObjList, holdKey, secondHoldKey, thirdKey):

    automationObjList[-1].writeOutlineOfFunctions(['pyAutogui.pressThreeKeys', (holdKey, secondHoldKey, thirdKey)])

def addBackspace(automationObjList,numOfPresses):


    automationObjList[-1].writeOutlineOfFunctions(['pyAutogui.backspace', numOfPresses])


def addOpenFile(automationObjList, filePath, fileName):

    '''
    Opens a file on the computer by its path and file name, includes a validation check whether or not the user
    has included a backslash at the end of the path
    :param automationObjList:
    :param filePath: given by the user prompt, file path only, not including filename
    :param fileName: comeplete filename with dot extension
    '''
    backslash = chr(92) # get a clean string of backslash chr because backslash is also an escape character
    if filePath[-1] != backslash: # if no backslash present in last position:
        filePath=filePath+backslash # add a backslash to the very end
    else: # if backslash is present do not add anything
        pass

    automationObjList[-1].writeOutlineOfFunctions(['pyAutogui.openFile', (filePath, fileName)])


def finishAutomation(automationObjList, mainWin):

    print('**** Automation file saved. All is Complete *')

    saveFile(automationObjList, "Automations")

    mainWin.clearButtons()

    mainWin.loadButtons()

def saveFile(dataToSave, filename):

    with open(filename, "wb") as fp:  # Pickling
        pickle.dump(dataToSave, fp)
        fp.close()

def deleteItem(attribute,deletedAutomations,automationObjList,mainWin):
    print('delete item accessed')
    print('attribute is:',attribute)
    c=0
    for object in automationObjList:
        if object.getName()==attribute or object.getName()==None: # if automation was not given a name, its name will be None
            deletedAutomations=automationObjList.pop(c)
            print("Button deleted")
            saveFile(automationObjList, "Automations")
            mainWin.clearButtons()
            mainWin.loadButtons()
        else:
            c+=1

def renameItem(attribute,automationObjList,mainWin,name):


    for object in automationObjList:
        if object.getName()==attribute:
            object.setName(name)
            saveFile(automationObjList, "Automations")
            mainWin.clearButtons()
            mainWin.loadButtons()

def setButtonColour(attribute,automationObjList,mainWin,colour):

    for object in automationObjList:
        if object.getName()==attribute:
            object.setColour(colour)
            saveFile(automationObjList, "Automations")
            mainWin.clearButtons()
            mainWin.loadButtons()





# def loadFile(filename): # No longer used here. This was moved to the TK Main function to load all neccessary data before starting the program
#
#     with open(filename, "rb") as fp:  # Unpickling
#         return pickle.load(fp)
