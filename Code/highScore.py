#retrieved from course notes
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

        
def addScore(data):
    #add current score to list of past scores
    with open("scores.txt", "a") as f:
        f.write(data.playerName + " " +str(data.score) + "\n")

def compileScores(path):
    #retrieve scores from file and put in order of highest to lowest
    file = readFile(path)
    
    scores = []
    
    for line in file.splitlines():
        words = line.split(" ")
        if words == [""]: continue
        scores += [(int(words[1]), words[0])]
        
    return((sorted(scores))[::-1])


def drawScores(data, canvas):
    #retrieve scores from file display 10 highest
    scores = compileScores("scores.txt")
    
    xPos = data.width // 2
    topMargin = data.height // 6
    bottomMargin = 19*data.height // 24
    yShift = (bottomMargin - topMargin) // 11
    
    for i in range(10):
        if i >= len(scores):
            break
        yPos = topMargin + (i + 1)*yShift
        
        canvas.create_text(xPos, yPos, text= scores[i][1] + " " \
        + str(scores[i][0]), font=data.font +" 16", fill = "white")