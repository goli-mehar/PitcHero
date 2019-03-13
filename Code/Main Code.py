#### InitializeMic and getPitch section retreived and modified from https://gist.github.com/notalentgeek/48aeab398b6b74e3a9134a61b6b79a36

import aubio
import numpy as num
import pyaudio
import sys
import BeatDetection as beat
from buttons import *
import highScore
import string
from random import randint
######## Init Functions
def initializeCourses(data):
    #build possible courses from songs folder
    data.courses = beat.buildCourses("Songs")
    data.levels = {"Easy": 15, "Medium": 10, "Hard": 5}
    data.difficulty = None
    data.pointValues = {"Red": 10, "Yellow": 40, "Green": 100}

def initializeMic(data):
    #Taken and modified from 
    #https://gist.github.com/notalentgeek/48aeab398b6b74e3a9134a61b6b79a36
    
    #Initializing audio objects to be used in getting audio input and 
    #determining pitch
    BUFFER_SIZE             = 2048
    CHANNELS                = 1
    FORMAT                  = pyaudio.paFloat32
    METHOD                  = "default"
    SAMPLE_RATE             = 44100
    HOP_SIZE                = BUFFER_SIZE//2
    PERIOD_SIZE_IN_FRAME    = HOP_SIZE #2048 // 2

    # Initiating PyAudio object.
    data.pA = pyaudio.PyAudio()
    # Open the microphone stream.
    data.mic = data.pA.open(format=FORMAT, channels=CHANNELS,
        rate=SAMPLE_RATE, input=True,
        frames_per_buffer=PERIOD_SIZE_IN_FRAME)

    # Initiating Aubio's pitch detection object.
    data.pDetection = aubio.pitch(METHOD, BUFFER_SIZE,
        HOP_SIZE, SAMPLE_RATE)
    # Set unit.
    data.pDetection.set_unit("Hz")
    # Frequency under -40 dB will considered
    # as a silence.
    data.pDetection.set_silence(-40)
    
def initializeBoard(data):
    #Initializing the map board
    data.mapHeight = data.height
    data.mapX = 0
    data.mapY = 0
    
def initializeAudio(data):
    #initialize the pyaudio object to play song
    song.initializeSong(data)
    
def initializeFormatting(data):
    #iinitialize any formatting or input variables
    data.recordLength = ""
    data.songName = ""
    data.playerName = ""
    data.font = "Verdana"
    data.topMargin = data.height // 6
    data.topAnchor = data.height // 12

###### Start Mode: Primary Screen

def gameName(data, canvas):
    #print the game name
    text = 'PitcHero'
    font = "Fixedsys 36 bold"
    x = data.width // 2
    y = data.height // 3
    y1 = 5*data.height // 12
    
    canvas.create_text(x, y, text = text, font=font, fill = "white")
    canvas.create_text(x, y1, text = "Play with earbuds!", font = "Fixedsys 18 bold", fill = "white")
    
def drawStartScreen(data, canvas):
    #print the start name
    gameName(data, canvas)
    
#### Song Selection Mode (DOne through button file)

### Draw Screen Title
def drawTitle(data, canvas):
    #print the screen name
    if data.mode not in ["Start", "Play"]:
        canvas.create_text(data.width // 2, data.topAnchor, text=data.mode, \
        font=data.font +" 24 bold", fill = "white")
    
#### Input Functions
def isValidInput(char):
    #check if valid input char
    if char not in string.whitespace and char in string.printable:
        return True
    return False
 
def backspace(keysym, word):
    #backspace function
    if keysym == "BackSpace":
        word = word[:-1]
        
    return word
    
def addCharacter(keysym, char, word):
    #add character to input string
    word = backspace(keysym, word)
    if len(word) < 20 and isValidInput(char):
        word = word + char
            
    return word

    
def input(data, char, keysym):
    #build inputs based on given keysym
    if data.mode == "Record":
        if data.buttons["Record"]["Length"][4] == True:
            if char.isdigit() and len(data.recordLength) < 3:
                data.recordLength = data.recordLength + char
            data.recordLength = backspace(keysym, data.recordLength)
                
        elif data.buttons["Record"]["Title"][4] == True:
            data.songName = addCharacter(keysym, char, data.songName)
                
    elif data.mode == "Name":
            data.playerName = addCharacter(keysym, char, data.playerName)
    
#### High Score Mode

def drawHighScoreScreen(data, canvas):
    #draw high scores to screen
    highScore.drawScores(data, canvas)

### Play Mode Functions
def getPitch(data):
    
    #Taken and modified from 
    #https://gist.github.com/notalentgeek/48aeab398b6b74e3a9134a61b6b79a36
    
    #Used to get audio input and determine current volume and pitch
    BUFFER_SIZE             = 2048
    HOP_SIZE                = BUFFER_SIZE//2
    PERIOD_SIZE_IN_FRAME    = HOP_SIZE
    
    # Always listening to the microphone.
    dta = data.mic.read(PERIOD_SIZE_IN_FRAME, exception_on_overflow=False)
    # Convert into number that Aubio understand.
    samples = num.fromstring(dta, dtype=aubio.float_type)
    # Finally get the pitch.
    pitch = data.pDetection(samples)[0]
        
    return pitch
    
def generateColor():
    #generate color for obstacles
    i = randint(0,10)
    if i in range(0,5):
        return "Red"
    elif i in range(5,8):
        return "Yellow"
    else:
        return "Green"
        
def scaleCourse(data, song):
    #scale obstacles to given screen
    
    course = data.courses[song]
    step = data.levels[data.difficulty]
    data.pathTopMargin = data.height // 10
    data.pathBottomMargin = 19*data.height // 24
    data.mapWidth = (2*course[-1][0]) + 100
    xSpace = 2
    ySpace = (data.pathBottomMargin - data.pathTopMargin) // 20
    
    scaledCourse = []
    for i in range(0,len(course), step):
        obstacle = course[i]
        x = 100 + obstacle[0]*xSpace
        y = data.pathTopMargin + obstacle[1]*ySpace
        color = generateColor()
        value = True
        
        scaledCourse += [[x, y, value, color]]
        
    data.course = scaledCourse
    
def drawCourse(data, canvas):
    #draw obstacles
    
    h = data.height // 50
    w = data.width // 50
    
    for obstacle in data.course:
        x, y, value, color = obstacle
        canvas.create_rectangle(x - w - data.mapX, y - h, x + w -  data.mapX, \
        y + h, fill=color , width=0)

def isTouchingCourse(x, y, data):
    #check if path is touching course, increase score if true
    
    h = data.height // 50
    w = data.width // 50
    
    for obstacle in data.course:
        obX, obY, value, color = obstacle
        if x > obX - w and x < obX + w and y > obY - h and y < obY + h \
        and value == True:
            data.score += data.pointValues[color]
            #extra variable to make sure points are added only once per block
            obstacle[2] = False
            
                
def drawPath(data, canvas):
    #Drawing current path of line
    i = 0
    while i+1 < len(data.points):
        
        if data.points[i][0] - data.mapX < -5:
            data.points.pop(i)
            
        x1, y1 = data.points[i]
        x2, y2 = data.points[i+1]

        canvas.create_line(x1 - data.mapX, y1, x2 - data.mapX, y2, fill \
        = "white")
        
        i += 1
        
def newPoint(data):
    #Getting a new point for line based on current pitch
    pitch = getPitch(data)
    
    if pitch != 0:
        if pitch > 200:
            y =  data.y - 10
        else:
            y = data.y + 10
    else:
        y = data.y
    x = data.x
    
    if y > data.pathBottomMargin : y = data.pathBottomMargin
    elif y < data.pathTopMargin: y = data.pathTopMargin
    
    data.x += 5
    data.y = y
    
    isTouchingCourse(x, y, data)
    
    data.points += [(x, y)]
                       
def drawScore(data, canvas):
    #Drawing time left
    x = (data.width//20)
    y = (data.height//20)
    score = "Score: " + str(data.score)
    
    canvas.create_text(x, y, anchor = "nw", text = score, 
    font = data.font + " " + str(int(data.height/30)) + " bold", fill = "white")
    
def drawPlayMode(data, canvas):
    #Draws line path and time left in game play mode
    if type(data.course) == str:
        scaleCourse(data, data.course)
    drawPath(data, canvas)
    drawCourse(data,canvas)
    drawScore(data, canvas)
    
def moveBoard(data):
    #Moving across map
    data.mapX += 1

def gameDone(data):
    #Check if game is done
    if data.x > data.course[-1][0] or (data.quit == True):
        data.mode = "Score"
        song.endSong(data)
        highScore.addScore(data)
        return True
    return False
        
#### Score Screen Mode
def drawCurScore(data, canvas):
    #Draw score screen
    canvas.create_text(data.width // 2, data.height // 2, \
    text=str(data.score), font=data.font + " 24 bold", fill = "white")

        
def drawScoreScreen(data, canvas):
    #Draw score screen
    drawCurScore(data, canvas)
       
#### Instructions Screen

def drawInstructions(data, canvas):
    #Draw game instructions
    info = "Sing higher or lower to control your PitcHero. Who is the best PitcHero?"
    
    canvas.create_text(data.width // 2, 4*data.height // 12, \
    text = info, font=data.font + " 12 bold", fill = "white" )
    
    canvas.create_text(data.width // 2, data.height // 2, \
    text = "Blocks", font=data.font + " 14 bold", fill = "white" )
    
    colors = ["Red", "Yellow", "Green"]
    y = 5*data.height // 8
    w = data.width // 8
    h = data.height // 16
    
    for i in range(3):
        x = data.width//6 + i*(data.width//3)
        
        canvas.create_rectangle(x - w, y - h, x + w, y + h, fill = colors[i])
        canvas.create_text(x, y + 1.5*h, text=data.pointValues[colors[i]],\
        font=data.font + " 12 bold", fill = "white", anchor="n")
        
from tkinter import *

####################################
# customize these functions
####################################

def init(data):
    #Initialize all variables
    data.mode = "Start"
    data.points = [(0, data.height//2)]
    data.y = 0
    data.x = 0
    data.timer = 0
    data.score = 0
    data.quit = False
    data.isRecording = False
    initializeFormatting(data)
    initializeCourses(data)
    initializeMic(data)
    initializeAudio(data)
    initializeBoard(data)
    initializeButtons(data)
    
def mousePressed(event, data):
    #check which button was pressed if mouse is clicked
    if pressingButton(event.x, event.y, data) == "init":
        init(data)
        
def keyPressed(event, data):
    #add given key to input if valid character
    if data.mode == "Record" or data.mode == "Name":
        input(data, event.char, event.keysym)
    elif data.mode == "Play":
        if event.keysym == "q":
            data.quit = True
        
def timerFired(data):
    #while in play mode, play song and  increase timer while moving board 
    # and adding new points to path
    if data.mode == "Play" and gameDone(data) == False:
        if data.timer == 0:
            song.startSong(data)
            
        song.playSong(data)
        
        data.timer += data.timerDelay
            
        if data.timer % 5 == 0:
            newPoint(data)
        if data.timer > 100 and data.timer%5 == 0:
            moveBoard(data)
            
def redrawAll(canvas, data):
    #Redraw screen for given mode
    
    drawButtons(data, canvas)
    drawTitle(data, canvas)
    
    if data.mode == "Start":
        drawStartScreen(data, canvas)
    elif data.mode == "Song Selection":
        pass
    elif data.mode == "Play":
        drawPlayMode(data, canvas)
    elif data.mode == "Score":
        drawScoreScreen(data, canvas)
    elif data.mode == "High Scores":
        drawHighScoreScreen(data, canvas)
    elif data.mode == "Recording":
        drawRecordingScreen(data, canvas)
    elif data.mode == "Instruction":
        drawInstructions(data, canvas)
        
####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    #modified to put timer fired wrapper first
    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
        
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='black', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 1 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(600, 500)