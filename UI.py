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
    app.manager.load_bot_instance()


    #Values 
    app.userTickerInput = ''
    app.dates = [] # From Bot
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
    
    app.tickerButtonSelected = None
    app.dateSelected=None
    app.optionSelected=None

    #Testing
    app.options = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
    app.buttonLabels = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'NVDA']
    
    
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
    #Check info
    if mouseX > 5 * app.width / 6 and mouseY < app.height / 6:
        app.infoScreen = not app.infoScreen


    #Check if the go buttons are being pressed
    for i in range(3):
        x0, y0, x1, y1 = app.goButtonCorners[i*4:4*(i+1)]
        if mouseX > x0 and mouseX < x1 and mouseY > y0 and mouseY < y1:
            app.goButtonPressed[i] = True
            app.textEntry = False

            if i == 0:
                app.manager.load_bot_instance()
                app.dates = app.manager.get_dates(app.userTickerInput)
                print(app.dates)
                #Call The first part of bot
            elif i == 1:
                if app.dates != None:
                    print(app.dates[app.dateSelected])
                    df = app.manager.get_options_df(app.dates[app.dateSelected])
                    strike_and_iv = app.manager.options_df_to_list(df)
                    app.options = app.manager.get_options_strings(strike_and_iv)

                    print(df)
                #Call the second part of bot

            elif i == 2:
                df = app.manager.get_options_df(app.dates[app.dateSelected])
                strike_and_iv = app.manager.options_df_to_list(df)
                strike = strike_and_iv[app.optionSelected][0]
                iv = strike_and_iv[app.optionSelected][1]

                print(strike, iv)
                #Call the graph function. 

    #Check if the user clicks on the text box
    x0, y0, x1, y1 = app.textboxCorners[0:4]
    if mouseX > x0 and mouseX < x1 and mouseY > y0 and mouseY < y1:
        app.textEntry = True
        app.tickerButtonSelected = None
    else:
        app.textEntry = False  

    #Check Ticker Buttons
    if app.bumper < mouseX < app.width/3 - app.bumper:
        for i in range(5):
            rectTop = 5 * app.height/12 + i*app.height/12
            boxHeight = app.height/12
            if rectTop < mouseY < rectTop + boxHeight:
                app.tickerButtonSelected = i
                app.userTickerInput = app.buttonLabels[i]

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
    drawOval(11 * app.width / 12, app.height/12, app.width/7, app.height/7, fill = None, border = 'black', align = 'center')
    drawLabel('I', 11 * app.width / 12, app.height/12, size = 50, bold = True, font = 'monospace')

def drawGoButton(app): #Draws all 3 buttons
    for i in range(3):
        x0, y0, x1, y1 = app.goButtonCorners[i*4: ((i+1) * 4)]

        if app.goButtonPressed[i] == True:
            buttonColor = 'pink'
        else:
            buttonColor = 'deeppink'
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
    

    boxWidth = app.width/3 - 2 * app.bumper
    boxHeight = app.height/12
    for i in range(5):
        if i == app.tickerButtonSelected:
            color = 'lightgray'
        else:
            color = 'white'
        rectTop = 5 * app.height/12 + i*boxHeight
        drawRect(app.bumper, rectTop, boxWidth, boxHeight, fill = color, border = 'black')
        drawLabel(app.buttonLabels[i], app.width/6, rectTop + boxHeight/2)

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
    info = 'This project was built by a group of freshman 15-112 students from stever house durring the anual Hack-112 hackathon. It uses a combination of web scraping and the dark choles algorithim to preidct \
    information about various stock option calls.'
    drawLabel('About', app.width/2, app.height/6 + 20, size = 20)
    drawLabel('This project was built by a group of freshman 15-112 students from stever house durring the anual Hack-112 hackathon.', app.width/2, app.height/6 + 40, size = 16) 
    drawLabel('It uses a combination of web scraping and the Black-Scholes algorithim to predict information about various stock option calls', app.width/2, app.height/6 + 60, size = 16)

    drawLabel('Instructions', app.width/2, app.height/6 + 100, size = 20)
    drawLabel('1. Enter the ticker for any US Stock. If you cannot think of one use one of the built in button. Press go to retrieve date options.', app.width/2, app.height/6 + 120, size = 16)
    drawLabel('2. Select a date for that stock. Select a date by clicking on it. Scroll through options using the up and down arrows. Press go when you have selected an option.', app.width/2, app.height/6 + 140, size = 16)
    drawLabel('3. Select an option for that day. Selection is the same as for dates. Press go to create graphs.', app.width/2, app.height/6 + 160, size = 16)
 

def redrawAll(app):
    drawTitle(app)

    if app.infoScreen:
        drawInfoScreen(app)
    else:

        
        drawGoButton(app)
        drawTickerSelection(app)
        drawDateSelection(app)
        drawOptionSelection(app)


### Main because cmu graphics cant handle files

def main():
    runApp(width = 900, height = 600)



main()    
