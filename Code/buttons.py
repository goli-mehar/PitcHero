import song
import record

###### Initialize Buttons

def roundUp(n):
    #corrected round function to always round up
    if n%1 > 0:
        return int(n // 1 + 1)
    else:
        return int(n // 1)
        
def startButtons(data):
    #initialize button coordinates for start mode
    startButtons = {"Play": [], "High Scores": [], "Record": []}
    
    x, y, h, w = data.width // 2, 7*data.height // 12, data.height // 24, data.width // 10
    startButtons["Play"] = [x - w, x + w, y - h, y + h]
    
    y = 8*data.height // 12
    startButtons["Record"] = [x - w, x + w, y - h, y + h]
    
    y = 9*data.height // 12
    startButtons["High Scores"] = [x - w, x + w, y - h, y + h]
    
    return startButtons
    
def songButtons(data):
    #initialize button coordinates for song selection mode
    songButtons = {}
    songI = 0
    songs = list(data.courses.keys())
    
    #number of rows needed for 5 cols
    cols = 5
    rows = roundUp(len(songs) / 5)
    
    #determining margins of buttons
    topMargin = data.topMargin
    leftMargin = data.width//10
    
    #center position for each button
    xShift = data.width // 5
    yShift = (data.height - topMargin) // (rows + 1)
    
    #size of each button
    width = data.width // 12
    height = (data.height - topMargin) // (2*(rows + 2))
    
    for i in range(rows):
        if songI >= len(songs):
            break
                
        for j in range(cols):
            if songI >= len(songs):
                break
                
            x = leftMargin + j*xShift
            y = topMargin + height + i*yShift
            song = songs[songI]
            
            songButtons[song] = [x - width, x + width, y - height, y + height]
            
            songI += 1
    return songButtons
    
def highScoreButtons(data):
    #initialize button coordinates for high scores mode
    
    highScoreButtons = {"Replay": [],}
    
    x, y, h, w = data.width // 2, 10*data.height // 12, data.height // 24, \
    data.width // 10
    highScoreButtons["Replay"] = [x - w, x + w, y - h, y + h]
    
    return highScoreButtons
    
def scorePlayButtons(data):
    #initialize button coordinates for score/play mode
    
    playButtons = {"Replay": [], "High Scores": []}
    
    x, y, h, w = data.width // 4, 10*data.height // 12, data.height // 24, \
    data.width // 10
    playButtons["Replay"] = [x - w, x + w, y - h, y + h]
    
    x = 3*data.width // 4
    playButtons["High Scores"] = [x - w, x + w, y - h, y + h]
    
    return playButtons
    
def nameButtons(data):
    #initialize button coordinates for name mode
    
    nameButtons = {"Play": [], "Player": []}
    
    x, y, h, w = data.width // 2, 3*data.height // 6, data.height // 24,\
     data.width // 10
    nameButtons["Player"] = [x - w, x + w, y - h, y + h]
    
    x, y, h, w = data.width // 2, 5*data.height // 6, data.height // 24, \
    data.width // 10
    nameButtons["Play"] = [x - w, x + w, y - h, y + h]
    
    return nameButtons
    
def difficultyButtons(data):
    #initialize button coordinates for difficulty mode
    
    difficultyButtons = {}
    
    xSpace = data.width // (len(data.levels) + 1)
    w = data.width // (2*(len(data.levels) + 2))
    y = data.height // 2
    h = data.height // 16
    
    levels = list(data.levels.keys())
    for i in range(len(levels)):
        
        x = xSpace*(i+1)
        difficultyButtons[levels[i]] = [x - w, x + w, y - h, y + h]
    
    return difficultyButtons
    
def recordButtons(data):
    #initialize button coordinates for record mode
    
    recordButtons = {"Play": [], "High Scores": [], "Length": [], "Title": [], "Record": []}
    
    x, y, h, w = data.width // 4, 2*data.height // 12, data.height // 24, data.width // 10
    recordButtons["Play"] = [x - w, x + w, y - h, y + h]
    
    x = 3*data.width // 4
    recordButtons["High Scores"] = [x - w, x + w, y - h, y + h]
    
    x, y = data.width // 2, data.height // 2
    recordButtons["Length"] = [x - w, x + w, y - h, y + h, False]
    
    x, y = data.width // 2, y + data.height // 9
    recordButtons["Title"] = [x - w, x + w, y - h, y + h, False]
    
    y = 5*data.height // 6
    recordButtons["Record"] = [x - w, x + w, y - h, y + h]
    
    return recordButtons
    
def infoButtons(data):
    #initialize button coordinates for instructions mode
    
    infoButtons = {"Play": []}
    
    x, y, h, w = data.width // 2, 10*data.height // 12, data.height // 24, \
    data.width // 10
    infoButtons["Play"] = [x - w, x + w, y - h, y + h]
    
    return infoButtons
    
def initializeButtons(data):
    #initialize button coordinates for all modes
    
    data.buttons = dict()

    data.buttons["Start"] = startButtons(data)
    data.buttons["Song Selection"] = songButtons(data)
    data.buttons["High Scores"] = highScoreButtons(data)
    data.buttons["Play"] = scorePlayButtons(data)
    data.buttons["Score"] = scorePlayButtons(data)
    data.buttons["Instruction"] = infoButtons(data)
    data.buttons["Record"] = recordButtons(data)
    data.buttons["Name"] = nameButtons(data)
    data.buttons["Difficulty"] = difficultyButtons(data)
    
###### Draw Function
    
def drawButtons(data, canvas):
    #Draw buttons to screen
    
    if data.mode in data.buttons:
        curButtons = data.buttons[data.mode]
    else:
        return None
        
    for button in curButtons:
        name = button
        if data.mode == "Song Selection": name = name[:-4]
        x1, x2, y1, y2 = curButtons[button][0:4]
        x = (x2 - x1) // 2 + x1
        y = (y2 - y1) // 2 + y1
        
        canvas.create_rectangle(x1, y1, x2, y2)
        
        if button == "Length" or button == "Title":
            if curButtons[button][4] == True:
                color = "Yellow"
            else:
                color = "White"
            canvas.create_rectangle(x1, y1, x2, y2, fill = color)
            if button == "Length":
                canvas.create_text(x, y1, text=name, font=data.font +" 10", anchor = "s", fill = "white")
                canvas.create_text(x, y, text=data.recordLength, font=data.font +" 10")
            elif button == "Title":
                canvas.create_text(x, y1, text=name, font=data.font +" 10", anchor = "s", fill = "white")
                canvas.create_text(x, y, text=data.songName, font=data.font +" 10")
        elif button == "Player":
            canvas.create_rectangle(x1, y1, x2, y2, fill = "White")
            canvas.create_text(x, y1, text=name, font=data.font +" 10", anchor = "s", fill = "white")
            canvas.create_text(x, y, text=data.playerName, font=data.font +" 10")
        else:
            canvas.create_text(x, y, text=name, font=data.font +" 14", fill = "white")
    
        
##### Button Functionality
def pressingButton(x, y, data):
    #Based on mode and button pressed, performs an intended functions
    curButtons = data.buttons[data.mode]
    
    if data.mode == "Start":
        if isTouchingButton(x, y, curButtons["Play"]):
            data.mode = "Song Selection"
        elif isTouchingButton(x, y, curButtons["High Scores"]):
            data.mode = "High Scores"
        elif isTouchingButton(x, y, curButtons["Record"]):
            data.mode = "Record"
            
    elif data.mode == "Song Selection":
        for songName in curButtons:
            if isTouchingButton(x, y, curButtons[songName]):
                data.course = songName
                data.mode = "Difficulty"
                song.getSong("Songs", data)
                
    elif data.mode == "Difficulty":
        for difficulty in curButtons:
            if isTouchingButton(x, y, curButtons[difficulty]):
                data.difficulty = difficulty
                data.mode = "Name"
                
    elif data.mode == "Name":
        if isTouchingButton(x, y, curButtons["Play"]):
            data.mode = "Instruction"
    
    elif data.mode == "Instruction":
        if isTouchingButton(x, y, curButtons["Play"]):
            data.mode = "Play"
        
    elif data.mode == "Play" or data.mode == "Score":
        if isTouchingButton(x, y, curButtons["Replay"]):
            return "init"
        elif isTouchingButton(x, y, curButtons["High Scores"]):
            data.mode = "High Scores"
    
    elif data.mode == "High Scores":
        if isTouchingButton(x, y, curButtons["Replay"]):
            return "init"
            
    elif data.mode == "Record":
        if isTouchingButton(x, y, curButtons["Play"]):
            return "init"
        elif isTouchingButton(x, y, curButtons["High Scores"]):
            data.mode = "High Scores"
        elif isTouchingButton(x, y, curButtons["Record"]):
            record.record(data) 
        elif isTouchingButton(x, y, curButtons["Length"]):
            curButtons["Length"][4] = True
            curButtons["Title"][4] = False
        elif isTouchingButton(x, y, curButtons["Title"]):
            curButtons["Title"][4] = True
            curButtons["Length"][4] = False
            
def isTouchingButton(x, y, butVals):
    #Checks to see if mous click is within button dimensions
    x1, x2, y1, y2 = butVals[0:4]
    if x > x1 and x < x2 and y > y1 and y < y2: return True
    else: return False
    