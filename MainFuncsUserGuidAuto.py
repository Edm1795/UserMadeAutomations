
# The class holding the actual automation information for a single unified set of automations. The name of the automation, the description of each step
# and the ability to create the functions

import pyautogui as ag
import time
import datetime
import pickle

class PYautogui:
    '''
    Class of PY Autogui functions
    '''

    def __init__(self):

        pass


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

    def click(self):
        '''
        Clicks the mouse
        '''
        ag.click()

    def drag(self, horiz, vert, duration, button):

        if button == 'l':
            button = 'left'
        if button == 'r':
            button = 'right'
        ag.dragTo(horiz, vert, button=button, duration=duration)

    def pressKeys(self, holdKey, secondKey):

        '''
        Double key press function: eg, ctrl + a
        Inputs: holdKey: str key to hold down, eg: ctrl or shift
        secondKey:  str second key to press eg, a
        '''
        ag.keyDown(holdKey)  # hold down the shift key
        ag.press(secondKey)  # press the left arrow key
        ag.keyUp(holdKey)

    def type(self, letters, enter='n'):
        '''
        Types keyboard input to the cursor.
        Inputs: letters: a sequence of strings to be typed
        Enter: a str 'y' or 'n', if you want to press the enter key after inputing letters1
        '''
        ag.write(letters)

        if enter == 'y':
            time.sleep(0.5)  # used to add gap between text input and pressing enter
            ag.press('enter')
        if enter =='n':
            return

    def moveMouseNEW(self, time, shift, duration=1):
        # This cool function simple takes the time (time of day eg, 3 pm) and the shift (eg: 1st shift) and
        # duration of mouse move, and the mouse will go to that spot. No more need to specify pixels
        # Vertical pixel difference between shifts: 50px

        shift = shift - 1  # decrement by one to get correct results
        shiftDiff = 52  # pixel distance between shifts (adjust this if mouse is not accurante
        tBase = 524  # base value for time which is 8 am (horizontal axis)
        sBase = 351  # base value for shift which is the top shift showing on screen (vertical axis)

        timeUnit = 30  # number of pixels for a time unit (set at 30 mins;ie 38px = 30 mins of time)

        timeSteps = self.timeSteps(time)  # number of time steps from base (8am) to desired time

        vert = sBase + (
                shift * shiftDiff)  # get shift pixel value multiply base value with number of shifts downwards on screen
        horiz = tBase + (timeSteps * timeUnit)

        ag.moveTo(horiz, vert, duration)

    def eraser(self):
        '''
        select the eraser function from side pane
        inputs: none
        '''
        self.moveMouse(22, 462, 0.5, 'y')  # click eraser selection button

    def otf(self):
        '''
        select the otf activity function from side pane
        inputs: none
        '''
        self.moveMouse(24, 427, 0.5, 'y')  # open activity pane
        self.moveMouse(66, 813, 0.5, 'y')  # select otf from list

    def logProgress(self, action, value):
        '''
        Logs the status of certain steps in the automation process such as finding elements on the screen
        Inputs: Action: string of the name of the action to log, eg element colour
        Value: str (or int) of key. Eg, True, complete
        '''
        action = str(action)
        self.progressDict[action] = value
        print(self.progressDict.items())

    def get(self,value):
        '''
        A master getter method. Input an argument to specify which values you want.
        Returns: tuple(x cor, y cor)
        input: value (str): ex: 'logo'
        return: tuple (x coord,ycoord) for the coords needed for the given parameter. Ex. 'logo' return position of the logo on screen
        '''

        if value == 'logo':
            return self.logo # coordinates of huge "D" on main screen
        if value == 'loginButt':
            return self.loginButt  # coord. of main Login button on main screen
        if value == 'schedRadButt':
            return self.schedRadButt # coord of Scheduler radio button on first pop up before entering main program
        if value == 'nextButt':
            return self.nextButt  # coord of Next button on scheduler pop up window just above
        if value == 'schedIcon':
            return self.schedIcon  # largish Schedules icon on top right of screen
        if value == 'filterIcon':
            return self.filterIcon # coord of small Filter icon top left for colour check
        if value == 'filterButt':
            return self.filterButt # coord of filter button
        if value == 'filterInputBar':
            return self.filterInputBar # coord of bar for choosing which positions to filter out for viewing on schedule
        if value == 'LA':
            return self.LA # vals for work com: (478, 309) # Coords for LA role in drop down filter menu
        if value == 'applyButt':
            return self.applyButt   # coords of Apply button on filter menu
        if value == 'monthlyCal':
            return self.monthlyCal   # coords for opening monthly calendar for choosing day to view on screen


    def clickDate(self):

        '''
        This function gets the current date and then calculates the position of that date on the calendar and clicks it.
        It contains a helper function called week() which gathers the week number a certain date is in, ex week 1, week 2
        '''

        def weekdayConver(curDate):
            '''
            Convert the normal return values of .weekday() to the needed values for this program where Sunday must be 0,
            Monday 1...
            :param curDate: Obj of the current date or any date you choose to input
            :return: int for each day of the week with Sun as 0
            '''

            day = curDate.weekday()  # extract the weekday int from the datetime object

            if day == 6: # Sunday
                return 0 # convert to 0 as Sunday
            if day == 5: # Sat
                return 6
            if day == 4: # Fri
                return 5
            if day == 3:
                return 4
            if day == 2:
                return 3
            if day == 1:
                return 2
            if day == 0:
                return 1

        def week():  # date=curDate.day, year=curDate.year, month=curDate.month
            '''
            This function determines the week number within a month a given date resides. For example which week is Dec.
            14th.
            :param date:  int, current date
            :param year: int current year
            :param month: int current month
            :return: int, the week a given date resides eg: 1,2,3,4,5
            '''
            # Create a date object
            dateObj = datetime.date.today()  # (year, month, date)

            # Calculate the week number within the month
            first_day_of_month = dateObj.replace(day=1)  # Get the first day of the month
            offset = (
                             first_day_of_month.weekday() - 6) % 7  # Calculate the offset for Sunday as the first day of the week
            adjusted_date = first_day_of_month - datetime.timedelta(days=offset)  # Adjust the date to start on a Sunday
            week_number = (dateObj - adjusted_date).days // 7 + 1  # Calculate the week number

            return week_number

        curDate = datetime.date.today()  # get date object for current day; datetime.date.today() gives all three values ymd
        day = weekdayConver(
            curDate)  # extract the weekday from the current date object as an int 0-6 for Mon-Sat. This is done with a helper func.
        # print(day)
        # print(week())
        yDiff = 32  # number of pixels between adjacent rows (eg week 1 - week 2) (work 32, home 37)
        xDiff = 36  # number of pixels between immediately adjacent days of week (eg:mon-tues) (work 36, home 44)
        xDefault = 851  # 36 pixel difference (work 851, home com 857)
        yDefault = 301  # (work 301, home com 381) (x=857, y=378)

        x = xDefault + (day * xDiff)

        if week() == 1:
            y = yDefault  # if needed the first week of the month supply only the yDefault
        else:  # if needing other weeks, subtract 1 and mulitply by the yDiff (pixel difference) week 2 = (2-1)*yDiff
            y = yDefault + ((week() - 1) * yDiff)
        print(x, y)
        self.moveMouse(x, y, 0.5, 'y')


class CheckForElem:

    '''
    Class for checking given elements are present on the screen. For example checks if a certain word is present
    or a certain colour of pixel
    '''

    def __init__(self):
        pass

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

    def confirmColour(self, x, y, colour):

        '''
        Confirms an element is present by matching a colour expected to a colour on the screen
        :param x: x coordinate of pixel to test its colour
        :param y: y coordinate of pixel to test its colour
        :param colour: a tuple (r,g,b) given in parantheses
        :return: True once the colour is detected
        '''

        loop = True
        while loop:
            # use eyedroper in Firefox browser options to get colour then convert to rgb
            if ag.pixelMatchesColor(x, y, colour) == False:  # colour must be sent as tuple (r,g,b)
                continue
            else:
                loop = False
        print('Colour confirmed ')
        time.sleep(0.1)
        return True

    def getColour(self):

        '''
        Gets the colour value of the pixel at the current position of the mouse
        :return: a tuple of two tuples, the mouse position and colour value at that position ((x,y),(r,g,b))
        '''
        mousePos = ag.position() # get position of the mouse (x,y)
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


class  AutomationSet:

    def __init__(self):

        self.name=None # Name of the Automation Set. Eg: Email, Booking, Schedule
        self.briefDescription=None # Brief description of the automation
        self.outlineOfFunctions=[] # List function and arguments in sequence in string form (used for building the real functions)

        # The actual function calls needs to be rebuilt everytime the program is restarted because func references do not remain constant
        # after restarting the program
        self.actualFunctions=[] # List of real functions in sequence built using the outlineOfFuncCalls directly above.

        self.pyAutogui=PYautogui() # Instantiate the PYautogui class which contains all methods for automating
        self.checkForElement=CheckForElem() # Instantiate CheckFor Element class

        # This call actually needs to be later in the process. It is moved to inside the runAutomation() method
        # when the class is first instantiated (during createAutomation) there is not yet a function outline and therefore
        # the actualFunctions will be empty
        # self.buildActualFuncsList() # Build the actual functions. This populates the actualFunctions list with the callable functions

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

    def writeOutlineOfFunctions(self,function):

        '''
        This method accesses the outlineOfFunctions list and appends a string name of the function and any needed arguments
        needed for a list of sequential automations. This list is then used to build the list of real functions. This method is
        used during the createAutomation phase when the user is building their sequence of automations. By thye time they
        have finished all the screen prompts asking for input, this list will be full
        :param str: function and any needed int, or str: arguments (variety of types depending on what is needed:
        :return: none
        '''

        # append a function and any needed arguments to the sequential outline of functions
        self.outlineOfFunctions.append(function)

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

        for list in self.outlineOfFunctions:  # access the list in the list [['function name as string',parameters]]
            if list[0] == 'pyAutogui.moveMouse': # if needing moveMouse, input moveMouse function with parameters
                self.actualFunctions.append([self.pyAutogui.moveMouse, list[1], list[2], list[3]])
            if list[0] == 'checkForElement.confirmColour': # if needing a colour check (element check), input colour check function with parameters
                self.actualFunctions.append([self.checkForElement.confirmColour, list[1]])
            if list[0] == 'pyAutogui.type': # if needing to type characters  input type function
                self.actualFunctions.append([self.pyAutogui.type, list[1], list[2]])
            if list[0] == 'pyAutogui.pressKeys': # if needing to press a key combination (hotkeys)
                self.actualFunctions.append([self.pyAutogui.pressKeys, (list[1][0], list[1][1])]) # arguments come inside a tuple (holdKey,tapKey)
    def runAutomation(self):
        '''
        This method runs the list of automation function calls from the actualFunctions list. It calls the functions
        in order from the list and adds formats the arguments if needed
        :return: none
        '''

        self.buildActualFuncsList()  # Build the actual functions. This populates the actualFunctions list with the callable functions
        ###### Running the User's Set of Automations ######

        # Run the list of function calls with arguments
        print('Running automation\n')
        for list in self.actualFunctions:  # access the list in the list
            if list[0] == self.pyAutogui.moveMouse:
                list[0](list[1][0], list[1][1], list[2],list[3])  # access each item in the internal list and input arguments
            if list[0] == self.checkForElement.confirmColour:
                list[0](list[1][0][0], list[1][0][1], (list[1][1]))  # [function,((x,y),(r,g,b))]
            if list[0] == self.pyAutogui.type:
                list[0](list[1], list[2])  # [function,((x,y),(r,g,b))]
            if list[0] == self.pyAutogui.pressKeys:
                list[0](list[1][0], list[1][1])  # [function,(holdKey,tapKey)]

# List holding all individual automation objects; added in by the createAutomation function
automationObjList=[]

def createAutomation():

    '''
    This function takes the user through a series of prompts in order to set up a new automation.
    The user will need to decide what type of action is needed for each step of their new automation.
    For example does it require a click of the mouse, and does it require confirming if a given button
    is even going to be loaded on the screen. Will text need to be inputted etc.
    :return: none
    inputs: none
    '''

    checkForElement=CheckForElem() # Instantiate a Check for Element Class (contains methods needed for checking colours)
    automationObjList.append(AutomationSet()) # Instantiate an AutomationSet Object

    name = input('Give a short one word name to your automation: ') # Prompt user to give the automation a name which goes onto the button on the TK interface
    automationObjList[-1].setName(name) # set name into the object which will be the last object in the list
    briefDes = input('Give a brief one sentence description of your automation: ') # Also prompt user for a short description
    automationObjList[-1].setBriefDescription(briefDes) # set description in object

    ##########################################################
    ##### Gathering User's Plans for an Automation Loop ######
    ##########################################################
    runMainLoop=True
    while runMainLoop:  # loop for gathering input from user. Stopping this loop will move out of the user gathering mode and into run mode

        mainRawInput = input('Press\n1 for move mouse and click\n2 to type\n3 to press key combination\n4 to finish and save')  # prompt user

        if mainRawInput == '1':  # if user wants to add mouse moves
            rawInput = input('Press\n1 to add a colour check for a web element\n2 to simply click mouse (without colour check)\n')  # mouse only, or with colour check

            if rawInput == '1':  # if adding colour check
                print('Use Main Monitor Only: Place mouse over the top of a stable coloured element of the program or website -- 5 seconds\n')
                time.sleep(5)
                posAndCol = checkForElement.getColour()  # returns tuple of mouse pos, colour ((x,y),(r,g,b)) ## Takes colour from main monitor only
                print('## Colour value acquired ##')
                automationObjList[-1].writeOutlineOfFunctions(['checkForElement.confirmColour', posAndCol])
                rawInput2 = input('Press\nNow move mouse to clicking position and press 1\n')
                if rawInput2 == '1':
                    print('Keep mouse in position -- 3 seconds\n')  # prompt user to move mouse into desired position
                    time.sleep(3)  # give 3 seconds to user to move mouse
                    mousePos = ag.position()  # get position of mouse as tuple (x,y)
                    automationObjList[-1].writeOutlineOfFunctions(['pyAutogui.moveMouse', mousePos, 0.5, 'y'])  # append function call and arguments with delay and click
                    print('Click position information complete, thank you.\n')

            if rawInput == '2':
                print('Move mouse into clicking position -- 3 seconds\n')  # prompt user to move mouse into desired position
                time.sleep(3)  # give 3 seconds to user to move mouse
                mousePos = ag.position()  # get position of mouse as tuple (x,y)
                automationObjList[-1].writeOutlineOfFunctions(['pyAutogui.moveMouse', mousePos, 0.5, 'y'])  # append function call and arguments with delay and click

        if mainRawInput == '2':
            rawText = input('Type the text you want entered: ')  # prompt user to move mouse into desired position
            enter = input("press 'y' to add enter")
            if enter == 'y':
                automationObjList[-1].writeOutlineOfFunctions(['pyAutogui.type', rawText, 'y'])  # append function call and arguments with delay and click
            else:
                automationObjList[-1].writeOutlineOfFunctions(['pyAutogui.type', rawText, 'n'])  # append function call and arguments with delay and click

        if mainRawInput == '3':  # if user wants to add a key combination (aka hotkeys)
            holdKey = input("type abbreviation for the 'hold' key with quotation marks. For example 'ctrl', 'alt','shift': ")
            tapKey = input("type the second key to be tapped. For example 'a', 'z': ")
            automationObjList[-1].writeOutlineOfFunctions(['pyAutogui.pressKeys', (holdKey, tapKey)])


        if mainRawInput == '4':  # if user wants to complete building the sequence of clicks
            print('**** Automation file saved.  All is Complete **** ')
            saveFile(automationObjList, "Automations")
            runMainLoop = False

def saveFile(dataToSave, filename):

    with open(filename, "wb") as fp:  # Pickling
        pickle.dump(dataToSave, fp)
        fp.close()


def loadFile(filename):

    with open(filename, "rb") as fp:  # Unpickling
        return pickle.load(fp)
