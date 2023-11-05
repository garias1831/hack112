from cmu_graphics import *
import string
from webscraper.bot import BotManager

### Controller

def getLocations(app):
    app.bumper = 10
    buttonTop = 5 * app.height / 6 + app.bumper
    buttonBottom = app.height - app.bumper
    app.goButtonCorners = [app.bumper, buttonTop, app.width/3 - app.bumper, buttonBottom, 
                        app.bumper + app.width/3, buttonTop, 2 * app.width/ 3 - app.bumper, buttonBottom, 
                        app.bumper + 2 * app.width/3, buttonTop, app.width - app.bumper, buttonBottom]
    app.textboxCorners = [app.bumper, app.bumper + app.height/6, app.width/3 - app.bumper, app.height / 3 - app.bumper]



def onAppStart(app):

    getLocations(app)

    #Webscrapin'
    app.manager = BotManager()


    #Values 
    app.userTickerInput = ''
    app.dateList = [] # From Bot
    app.userDateInput = ''
    app.optionsDF = [] # From Bot 2
    app.userOptionInput = ''
    
    

    #States:
    app.goButtonPressed = [False, False, False]
    app.textEntry = False
    app.infoScreen = False
    app.isDateSelected=False
    app.isOptionSelected=False

    
    app.dateIndex=10
    app.optionIndex=10
    
    app.dateSelected=None
    app.optionSelected=None

    #Testing
    app.options = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
    app.dates=['November 12, 2023', 'December 17, 2023', 'January 5, 2023', 
               'February 2, 2024', 'October 18, 2025', 'October 22, 2024', 
               'May 27, 2026', 'August 1, 2024', 'May 22, 2026', 'June 26, 2023', 
                'December 8, 2023', 1, 2, 3, 4]
    

def onStep(app):
    getLocations(app)

def onKeyPress(app, key):
    if app.textEntry == True:
        if key.isalpha() and len(key) == 1: 
            app.userTickerInput += key.upper()
        elif key == 'backspace':
            app.userTickerInput = app.userTickerInput[0:-1]


    if (key=='down') and (app.dateIndex<len(app.dates)):
        app.dateIndex+=1
        app.optionIndex +=1
    elif (key=='up') and (app.dateIndex>10):
        app.dateIndex-=1
        app.optionIndex -= 1


def onMousePress(app, mouseX, mouseY):
    #Check if the go buttons are being pressed
    for i in range(3):
        x0, y0, x1, y1 = app.goButtonCorners[i*4:4*(i+1)]
        if mouseX > x0 and mouseX < x1 and mouseY > y0 and mouseY < y1:
            app.goButtonPressed[i] = True
            app.textEntry = False

            if i == 0:

                app.dateList = app.manager.get_dates(app.userTickerInput)
                print(app.dateList)
                #Call The first part of bot
            elif i == 1:
                pass
                #Call the second part of bot
            elif i == 2:
                pass
                #Call the graph function. 

    #Check if the user clicks on the text box
    x0, y0, x1, y1 = app.textboxCorners[0:4]
    if mouseX > x0 and mouseX < x1 and mouseY > y0 and mouseY < y1:
        app.textEntry = True
    else:
        app.textEntry = False   

    #Date List
    if app.width/2-app.width/8 <= mouseX <= app.width/2+app.width/8:
        for i in range(10):
            if ((app.height*(((2*i)+1)/30))+(app.height/6) - app.height/30
                <= mouseY <= (app.height*(((2*i)+1)/30))+(app.height/6) + 
                app.height/30):
                app.isDateSelected=True
                app.dateSelected=i

    #Option List
    if app.width/2-app.width/8 + app.width/3 <= mouseX <= app.width/2+app.width/8 + app.width/3:
        for i in range(10):
            if ((app.height*(((2*i)+1)/30))+(app.height/6) - app.height/30
                <= mouseY <= (app.height*(((2*i)+1)/30))+(app.height/6) + 
                app.height/30):

                app.isOptionSelected=True
                app.optionSelected=i

    



def onMouseRelease(app, mouseX, mouseY):
    app.goButtonPressed = [False, False, False]
    



### View
def drawTitle(app):
    drawLabel('Quant 112', app.width/2, app.height/12, size = 50)
    drawLabel('Select a top 100 stock from the drop-down menu or type your own', app.bumper, app.bumper, align = 'left')

def drawGoButton(app): #Draws all 3 buttons
    for i in range(3):
        x0, y0, x1, y1 = app.goButtonCorners[i*4: ((i+1) * 4)]

        if app.goButtonPressed[i] == True:
            buttonColor = 'lightGreen'
        else:
            buttonColor = 'green'
        drawRect(x0, y0, x1 - x0, y1-y0, fill = buttonColor, border = 'black')
        drawLabel('Go!', x0 + (x1-x0)/2, y0 + (y1-y0)/2)

def drawTextBox(app): #Draws the Box for text entry
    if app.textEntry == True:
        buttonColor = 'lightgrey'
    else:
        buttonColor = 'white'

    x0, y0, x1, y1 = app.textboxCorners[0:4]
    drawRect(x0, y0, x1-x0, y1-y0, fill = buttonColor, border = 'black')
    drawLabel(app.userTickerInput, x0 + app.bumper, y0 + (y1 - y0) / 2, align = 'left', size = 15)
    
    if app.textEntry == False and app.userTickerInput == '':
        drawLabel('Click here to enter a Ticker', x0 + app.bumper, y0 + (y1 - y0) / 2, align = 'left')

def drawTickerSelection(app):
    drawTextBox(app)

    drawLabel("Or choose one of the following:", app.width/6, app.height * 9 / 24)
    buttonLabels = ['APPL', 'MSFT', 'GOOG', 'AMZN', 'NVDA']

    # boxWidth = app.width/3 - 2 * app.bumper
    # boxHeight = app.height/6 - 2 * app.bumper
    # for i in range(5):
    #     rectTop = 5 * app.height/12 + i*boxHeight
    #     drawRect(app.bumper, rectTop, boxWidth, boxHeight, fill = None, border = 'black')
    #     drawLabel(buttonLabels[i], app.width/6, rectTop + app.height / 12)


def drawDateSelection(app):
    if (app.dateIndex <= len(app.dates)) and (len(app.dates)<=10):
        dates = app.dates
    else:
        dates = app.dates[(app.dateIndex-10):app.dateIndex]

    #entries
    for i in range(10):
        if i == app.dateSelected:
            color = 'lightgray'
        else:
            color = 'white'

        rectLeft = app.width/3 + app.bumper
        rectWidth = app.width/3 - app.bumper*2
        rectTop = (app.height*(((2*i))/30)) + (app.height/6) + app.bumper
        rectHeight = app.height/15
        drawRect(rectLeft, rectTop, rectWidth, rectHeight, fill=color, border='black')

        if i <= len(dates)-1:
            message = dates[i]
            drawLabel(f'{message}', app.width/2, 
                      rectTop + rectHeight/2)

def drawOptionSelection(app):
    if (app.optionIndex <= len(app.options)) and (len(app.options)<=10):
        options = app.options
    else:
        options = app.options[(app.optionIndex-10):app.optionIndex]

    #entries
    for i in range(10):
        if i == app.optionSelected:
            color = 'lightgray'
        else:
            color = 'white'

        rectLeft = app.width/3 * 2 + app.bumper
        rectWidth = app.width/3 - app.bumper*2
        rectTop = (app.height*(((2*i))/30)) + (app.height/6) + app.bumper
        rectHeight = app.height/15
        drawRect(rectLeft, rectTop, rectWidth, rectHeight, fill=color, border='black')

        if i <= len(options)-1:
            message = options[i]
            drawLabel(f'{message}', app.width/6 * 5, 
                      rectTop + rectHeight/2)

def drawInfoScreen(app):
    pass

def redrawAll(app):

    drawLine(0, app.height/3, 100, app.height/3)
    drawLine(0, app.height/2, 100, app.height/2)
    drawLine(0, 2 * app.height/3, 100, 2 * app.height/3)
    drawLine(0, 5 * app.height/6, 100, 5 * app.height/6)


    if app.infoScreen:
        drawInfoScreen(app)
    else:

        drawTitle(app)
        drawGoButton(app)
        drawTickerSelection(app)
        drawDateSelection(app)
        drawOptionSelection(app)


### Main because cmu graphics cant handle files

def main():
    runApp()

#width = 900, height = 600

main()    
