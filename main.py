

# alt shift e runs the single line the cursor is on

# opens a single instance of dayforce for quick check
import pyautogui as ag
import time
import datetime
import pickle




class TaskSet:
    '''
    Class for a single unified set of automated GUI movements and actions
    '''

    def __init__(self,computer):

        '''
        initialize values, mostly coordinates of locations on the screen according to what computer you are running the
        program on. Each screen will display important elements of the website in different areas and so the values
        foe each computer must be seperated
        :param computer: str: 'h' for home computer; 'w' for work computer
        '''

        self.progressDict = {}  # Instantiate dictionary which hold keys and values about state of checks on the screen . Eg: {colour: true}

        if computer == 'h': # Initialize values for your home computer
            self.logo=(688, 592) # coordinates of huge "D" on main screen
            self.loginButt=(1315, 917) # coord. of main Login button on main screen
            self.schedRadButt=(938, 547) # coord of Scheduler radio button on first pop up before entering main program
            self.nextButt=(1048,685) # coord of Next button on scheduler pop up window just above
            self.schedIcon=(1116, 422) # largish Schedules icon on top right of screen
            self.filterIcon=(353, 286) # coord of small Filter icon top left for colour check
            self.filterButt=(373, 286) # coord of filter button
            self.filterInputBar=(553, 332) # coord of bar for choosing which positions to filter out for viewing on schedule
            self.LA = (553, 391)  # vals for work com: (478, 309) # Coords for LA role in drop down filter menu
            self.applyButt=(1553, 380) # coords of Apply button on filter menu
            self.monthlyCal=(990, 240) # coords for opening monthly calendar for choosing day to view on screen

        if computer == 'w': # Initialize values for your work computer
            self.logo = (665, 575)  # coordinates of huge "D" on main screen
            self.loginButt = (1226, 737)  # coord. of main Login button on main screen
            self.schedRadButt = (915, 548)  # coord of Scheduler radio button on first pop up before entering main program
            self.nextButt = (1007, 660)  # coord of Next button on scheduler pop up window just above
            self.schedIcon = (1056, 337)  # largish Schedules icon on top right of screen
            self.filterIcon = (227, 223)  # coord of small Filter icon top left for colour check
            self.filterButt = (246, 223)  # coord of filter button
            self.filterInputBar = (376, 261)  # coord of bar for choosing which positions to filter out for viewing on schedule
            self.LA = (410, 310)  # vals for work com: (478, 309) # Coords for LA role in drop down filter menu
            self.applyButt = (1629, 301)  # coords of Apply button on filter menu
            self.monthlyCal = (1087, 188)  # coords for opening monthly calendar for choosing day to view on screen





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
        :param x: x coordinate of position of colour
        :param y: y coordinate of position of colour
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

def saveFile(dataToSave, filename):
    with open(filename, "wb") as fp:  # Pickling
        pickle.dump(dataToSave, fp)
        fp.close()


def loadFile(filename):
    with open(filename, "rb") as fp:  # Unpickling
        return pickle.load(fp)




def main():
    funcOutlineList=[] # List of descriptions and arguments of what functions are needed for the real functions list
    funcList = [] # The real list of functions used for executing the automations
    checkForElement=CheckForElem()
    taskSet1=TaskSet('h') # instantiate class of methods
    runMainLoop=True # set up while loop control variable
    newOrOldLoop=True



    while newOrOldLoop:

        loadOrSave=input('Press \n1 to load a file\n2 to start a new one\n')
        if loadOrSave=='1':
            print('Loading file.\n')
            funcOutlineList=loadFile("Automations") # Load the saved list of descriptions

            ### Build the Function List (funcList) from the Outline of Functions List (funcOutlineList) ###

            for list in funcOutlineList:  # access the list in the list
                if list[0] == 'taskSet1.moveMouse':
                    funcList.append([taskSet1.moveMouse, list[1],list[2],list[3]])
                if list[0] == 'checkForElement.confirmColour':
                    funcList.append([checkForElement.confirmColour, list[1]])
                if list[0] == 'taskSet1.type':
                    funcList.append([taskSet1.type, list[1],list[21]])

            newOrOldLoop=False

        if loadOrSave=='2':

            ####### Gathering User's Plans for Automation Loop #######

            while runMainLoop: # loop for gathering input from user. Stopping this loop will move out of the user gathering mode and into run mode

                mainRawInput =input('Press\n1 for move mouse and click\n2 to type\n3 to finish and save\n') # prompt user
                if mainRawInput=='1': # if user wants to add mouse moves
                    rawInput=input('Press\n1 to add a colour check for a web element\n2 to simply click mouse (without colour check)\n')
                    if rawInput=='1':

                        print('Place mouse over the top of a stable coloured element of the program or website -- 5 seconds\n')
                        time.sleep(5)
                        posAndCol=checkForElement.getColour() # returns tuple of mouse pos, colour ((x,y),(r,g,b))
                        funcOutlineList.append(['checkForElement.confirmColour', posAndCol])
                        rawInput2 = input('Press\n1 when mouse is in position\n')
                        if rawInput2 == '1':
                            print('Move mouse into position\n')  # prompt user to move mouse into desired position
                            time.sleep(3)  # give 3 seconds to user to move mouse
                            mousePos = ag.position()  # get position of mouse as tuple (x,y)
                            funcOutlineList.append(['taskSet1.moveMouse', mousePos, 0.5,'y'])  # append function call and arguments with delay and click
                            print('Click information gathering complete, thank you.\n')

                    if rawInput=='2':

                        print('Move mouse into position -- 3 seconds\n') # prompt user to move mouse into desired position
                        time.sleep(3) # give 3 seconds to user to move mouse
                        mousePos=ag.position() # get position of mouse as tuple (x,y)
                        funcOutlineList.append(['taskSet1.moveMouse',mousePos,0.5,'y']) # append function call and arguments with delay and click

                if mainRawInput == '2':
                    rawText = input('Type the text you want entered:')  # prompt user to move mouse into desired position
                    enter=input("press 'y' to add enter")
                    if enter == 'y':
                        funcOutlineList.append(['taskSet1.type', rawText,'y'])  # append function call and arguments with delay and click
                    else:
                        funcOutlineList.append(['taskSet1.type', rawText,'n'])  # append function call and arguments with delay and click

                if mainRawInput=='3': # if user wants to complete building the sequence of clicks
                    print('**** File saved.')
                    saveFile(funcOutlineList,"Automations")
                    runMainLoop=False



    ###### Running the User's Set of Automations ######

    # Run the list of function calls with arguments
    print('Running automation\n')
    for list in funcList:  # access the list in the list
        if list[0] == taskSet1.moveMouse:
            list[0](list[1][0],list[1][1],list[2],list[3])  # access each item in the internal list and input arguments
        if list[0] == checkForElement.confirmColour:
            list[0](list[1][0][0],list[1][0][1],(list[1][1])) # [function,((x,y),(r,g,b))]
        if list[0] == taskSet1.type:
            list[0](list[1],list[2]) # [function,((x,y),(r,g,b))]

main()








    #
    # taskSet4 = TaskSet('w')
    # checkForElem = CheckForElem()
    # timeVal=TimeValues('m') # Instantiate times to fast values
    #
    # taskSet4.moveMouse(173, 68, 0.2, 'y')  # click on blank area of browser to focus the browser
    # taskSet4.pressKeys('ctrl', 't')  # open new tab (try to add delay here)
    # taskSet4.type('https://can232.dayforcehcm.com/MyDayforce/Mydayforce.aspx', 'y')  # Go to site (updated website address)
    # # if taskSet4.confirmElement('Company.png','cr') == True: # monitor for when Select Role box displays then select Daily Scheduler (tiny radio button)
    # if checkForElem.confirmColour(taskSet4.get('logo')[0], taskSet4.get('logo')[1], (48, 103, 219)):
    #     taskSet4.moveMouse(1226, 640, timeVal.getFast(), 'y')  # go to autofill user name; Firefox should auto pop this up
    # taskSet4.moveMouse(taskSet4.get('loginButt')[0], taskSet4.get('loginButt')[1], timeVal.getMed(), 'y')  # go to Login
    # if checkForElem.confirmImage('SelectRole.png','c'):  # monitor for when Select Role box displays then select Daily Scheduler (tiny radio button)
    #     taskSet4.moveMouse(taskSet4.get('schedRadButt')[0], taskSet4.get('schedRadButt')[1], timeVal.getFast(),'y')  # select Daily Scheduler (small box before sched loaded) !if this is missed the next function will not be available (shedule button)
    # taskSet4.moveMouse(taskSet4.get('nextButt')[0], taskSet4.get('nextButt')[1], timeVal.getMed(), 'y')  # click next (on small box)
    # if checkForElem.confirmImage('Schedules.png', 'n', 1007, 370, 1113, 397):
    #     taskSet4.moveMouse(taskSet4.get('schedIcon')[0], taskSet4.get('schedIcon')[1], timeVal.getMed(), 'y')  # click schedule (main button to load sched)
    # if checkForElem.confirmColour(taskSet4.get('filterIcon')[0], taskSet4.get('filterIcon')[1], (28, 68, 156)):  # Check for filter button by colour of icon
    #     taskSet4.moveMouse(taskSet4.get('filterButt')[0], taskSet4.get('filterButt')[1], timeVal.getFast(), 'y')  # click Filter button
    # taskSet4.moveMouse(taskSet4.get('filterInputBar')[0], taskSet4.get('filterInputBar')[1], timeVal.getMed(), 'y')  # click filter input bar
    # taskSet4.moveMouse(taskSet4.get('LA')[0], taskSet4.get('LA')[1], timeVal.getMed(), 'y')  # select LA
    # taskSet4.moveMouse(taskSet4.get('applyButt')[0], taskSet4.get('applyButt')[1], timeVal.getFast(), 'y')  # click Apply button
    # taskSet4.moveMouse(taskSet4.get('monthlyCal')[0], taskSet4.get('monthlyCal')[1], timeVal.getMed(), 'y')  # open calendar
    # taskSet4.clickDate() # find the current date on the calendar and click it
    #
    # print(ag.pixelMatchesColor(215, 133, (
    #     56, 00, 00)))  # use eyedroper in Firefox browser options to get colour then convert to rgb


