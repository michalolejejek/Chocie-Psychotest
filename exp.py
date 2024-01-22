
import os, random, math, string
from random import randint
from math import radians, sin, cos
from psychopy import core, visual, event, gui, misc, data

def enterSubInfo(expName):
    """Brings up a GUI in which to enter all the subject info."""
    try:
        expInfo = misc.fromFile(expName+'_lastParams.pickle')
    except:
        expInfo = {'ExpTitle':expName,'Subject':'s01', 'Subject Initials':'abc','Start at trial':0,'Experimenter Initials':'KV'}
    expInfo['dateStr']= data.getDateStr() 
    dlg = gui.DlgFromDict(expInfo, title=expName+' Exp', fixed=['dateStr'])
    if dlg.OK:
        misc.toFile(expName+'_lastParams.pickle', expInfo)
    else:
        core.quit()
    return expInfo
    
def showInstructions(instructText1, instructText2, pos=[0,.3], waitKeys=True):
    """ Displays the experiment specific instructional/descriptive text. 
    The position/wrapWidth may need to be changed depending
    on the length of the text."""
    
    instructs1 = visual.TextStim(win, color='#fdfdfd',pos=pos,wrapWidth=1.2, height=.06,text= instructText1)
    instructs2 = visual.TextStim(win, color='#fdfdfd',pos=[coord*-.8 for coord in pos],wrapWidth=1.2, height=.06,text= instructText2)
    instructs1.draw()
    instructs2.draw()
    win.flip()
    
    if waitKeys:
        event.waitKeys()
    else:
        pass
    
def makeDataFile(subject, expName):
    """Make a text file to save data, will not overwrite existing data"""
    fileName = subject+'_'+expName 
    ext =''
    i = 1
    while os.path.exists(fileName+ext+'.xls'): #changes the extenstion on the filename so no file is ever overwritten.
        ext = '-'+str(i)
        i +=1
    dataFile = open(fileName+ext+'.xls', 'w')
    return dataFile

def writeToFile(fileHandle, trial, sync=True):
    """Writes a trial (a dictionary) to a fileHandle, in a specific order, given 
    by overall order (general variables that are always used) and experiment 
    specific variables (variables that vary based on what you're measuring)."""
    overallOrder = ['subject','subInitials','date','experimenter','totalTime','trialNum']
    overallOrder.extend(expVarOrder)
    
    line = ''

    if trialNum==0:
        for item in overallOrder:
            line += item
            line += '\t'
        line += '\n'
        
    for item in overallOrder:
        line += str(trial[item])
        line += '\t'
    line += '\n' #add a newline
    print(line)
    fileHandle.write(line)
    if sync:
        fileHandle.flush()
        os.fsync(fileHandle)

def generateTraining():
    """Generates initial trial list for training phase, before latencies are added."""
    
    trials = []
    
    for trial in range(numTraining):
        trials.append({'latency':'NA','avgChoiceTime':'NA'})
        
    return trials
    
def generateExperimental(throwOut=15):
    """Generates experimental trials."""
    

    choiceLatencies = [3,5]
    askConf = [0,1]
    

    trials = []
    
    for rep in range(reps):
        for latency in choiceLatencies:
            for asked in askConf:
                trials.append({'latency':int(latency),'avgChoiceTime':'NA','askConf':asked})
            

    random.shuffle(trials)
            
    return trials
    
def addTrialVariables():
    """Adds extra trial details to each line written to the datafile."""
    trial['subject'] = expInfo['Subject']
    trial['subInitials'] = expInfo['Subject Initials']
    trial['experimenter'] = expInfo['Experimenter Initials']
    trial['date'] = expInfo['dateStr']
    trial['totalTime'] = expClock.getTime()
    trial['trialNum'] = trialNum + 1 #add 1 because index starts at 0
    trial['circlePositions'] = circlePositions
    trial['squarePositions'] = squarePositions
    trial['response'] = response
    trial['responseTime'] = responseTime
    trial['choiceTime'] = choiceTime
    trial['confAnswer'] = confAnswer
    trial['colorOptions'] = colorOptions

def readySequence():
    """Prompts subject with "Ready" screen and counts down to stimulus presentation."""
    
    ready.draw()
    trialDisplay = visual.TextStim(win,text=trialNum+1,height=.08,pos=(0,-.8),color=[1,1,1]) #displays trial num.
    trialDisplay.draw()
    win.flip()

    if ['q']==event.waitKeys(keyList=['space','q']):
        quit.draw()
        win.flip()
        if ['y']==event.waitKeys(keyList=['y','n']):
            dataFile.close()
            win.close()
            core.quit()
        else:
            ready.draw()
            win.flip()
            event.waitKeys(keyList=['space'])
    
    fixation.draw()
    win.flip()
    core.wait(.5)

def presentStimuli(numCircles, askConf, latency='NA', training=False, numSquares=1):
    """Draws non-overlapping letters in window for specified time."""

    colorOptions = ['Red','Gold','Lime','Fuchsia','Aqua','Coral']
    random.shuffle(colorOptions)

    squareColorOptions = ['Red','Gold','Lime','Fuchsia','Aqua','Coral']
    random.shuffle(squareColorOptions)

    circles = []
    squares = []
    letters = []
    

    for circleNum in range(numCircles):
        circles.append(visual.Circle(win, size=70, units='pix',fillColor=colorOptions[circleNum],lineColor=colorOptions[circleNum]))
        

    for squareNum in range(numSquares):
        squares.append(visual.Rect(win,units='pix',width=70,height=70,fillColor=squareColorOptions[squareNum],lineColor=squareColorOptions[squareNum]))
        

    centerDist = 150

    for circleNum,circle in enumerate(circles):
        tryAgain = True
        while tryAgain:
            circleAng = radians(randint(0,360))
            circle.pos = (centerDist*sin(circleAng),centerDist*cos(circleAng))
            tryAgain = False      
            for i in range(circleNum): 
                if circle.overlaps(circles[i]):
                    tryAgain = True
                    break
                    
    for squareNum,square in enumerate(squares):
        tryAgain = True
        while tryAgain:
            circleAng = radians(randint(0,360))
            square.pos = (centerDist*sin(circleAng),centerDist*cos(circleAng))
            tryAgain = False      
            for i in range(squareNum): 
                if square.overlaps(circle[i]):
                    tryAgain = True
                    break
                    
    if training==True: 
        response = 'NA'
        responseTime = 'NA'
        confAnswer = 'NA'
                
  
        for circle in circles:
            circle.draw(win)
        for square in squares:
            square.draw(win)
        win.flip()

        choiceClock.reset()

        event.waitKeys(keyList=['space'])
        choiceTime = choiceClock.getTime()
    
    else: 
        choiceTime = 'NA'
        
        for n in range(latency):
            for circle in circles:
                circle.draw(win)
            for square in squares:
                square.draw(win)
            win.flip()
        
        centerCircle = visual.Circle(win,size=70,units='pix',pos=[0,0],fillColor=colorOptions[1],lineColor=colorOptions[1])
                
        for circle in circles:
            circle.draw(win)
        win.clearBuffer()
        win.flip()
        centerCircle.draw(win)
        win.flip()
    
        responseClock.reset()
        response = event.waitKeys(keyList=['t','f','c'])
        responseTime = responseClock.getTime()
        
        if askConf and response!=['c']:
            confQuestionVisual.draw(win)
            win.flip()
            confAnswer = event.waitKeys(keyList=['1','2','3','4','5'])
        else: 
            confAnswer = 'NA'
   
    circlePositions = [str(circle.pos) for circle in circles]
    squarePositions = [str(square.pos) for square in squares]
    return circlePositions, squarePositions, response,responseTime,choiceTime,confAnswer,colorOptions


expVarOrder = [
'latency',
'avgChoiceTime',
'circlePositions',
'squarePositions',
'response',
'responseTime',
'choiceTime',
'confAnswer',
'colorOptions'
]
expInfo = enterSubInfo('Choice Experiment')
dataFile = makeDataFile(expInfo['Subject'],expInfo['ExpTitle'])

win = visual.Window([1920, 1080], color=[-1, -1, -1], fullscr=False, monitor='testMonitor')
ready = visual.TextStim(win, text=u'Ready?', height=.3, color=[1,1,1])
fixation = visual.TextStim(win, text='+', height=.07, color=[1,1,1])
quit = visual.TextStim(win,text='Quit experiment now (y/n)?',height=.1,color=[1,1,1])

confQuestionText = u'On a scale from 1 to 5, how confident you are that this is your choice? (1= Not confident at all; 5= Extremely confident) '
confQuestionVisual = visual.TextStim(win,color='#fdfdfd',wrapWidth=1.2, height=.06,text=confQuestionText)

mouse = event.Mouse(visible=False,win=win)

expClock = core.Clock()
responseClock = core.Clock()
choiceClock = core.Clock()

text1 = 'Witaj! Celem tego eksperymentu jest zbadanie, jak ludzie dokonują wyboru między prostymi obiektami wizualnymi, \
a nie testowanie konkretnych umiejętności czy zdolności intelektualnych.'

text2 = 'Najpierw znak plusa (+) będzie migał na środku ekranu. \
Następnie na losowych miejscach na ekranie pojawią się 2 różnokolorowe kręgi. \
Tak szybko, jak potrafisz, będziesz musiał wybrać jeden z tych kręgów "w swojej głowie" i zapamiętać, który wybrałeś. \
Nie ma poprawnego ani niepoprawnego wyboru: odpowiedz na podstawie swoich osobistych preferencji (Naciśnij dowolny klawisz, aby kontynuować.)'

showInstructions(text1,text2)

text1 = 'Po pojawieniu się kręgów na ekranie, w środku pojawi się trzeci krąg, który pasuje do koloru jednego z dwóch pierwszych. \
Jeśli ten nowy krąg ma ten sam kolor co wybrany przez Ciebie krąg: naciśnij T (PRAWDA) na klawiaturze. \
Jeśli nie ma tego samego koloru: naciśnij F (FAŁSZ).'

text2 = 'Czasami trzeci krąg pojawi się bardzo szybko, dlatego ważne jest, aby spróbować wybrać krąg w swojej głowie tak szybko, jak to możliwe. Jeśli trzeci krąg pojawi się tak szybko, że nie zdążyłeś wybrać kręgu wcześniej, naciśnij C (Nie mogłem wybrać). (Naciśnij dowolny klawisz, aby kontynuować.)'

showInstructions(text1,text2)

text = 'W niektórych próbach zostaniesz zapytany Jak bardzo jesteś pewien, że to był ten wybrany krąg\
na skali od 1 do 5 (1=Bardzo mało pewny; 5=Bardzo pewny). \
Może się zdarzyć, że będziesz czuł się bardzo pewny na wszystkich lub większości prób, w takim przypadku jest w porządku \
odpowiadać zawsze 5 i vice versa.\
Po prostu odpowiadaj zgodnie z własnym uczciwym osądem. (Naciśnij dowolny klawisz, aby kontynuować.)'

instruct = visual.TextStim(win, color='#fdfdfd',pos=[0,0],wrapWidth=1.2, height=.06,text=text)
instruct.draw()
win.flip()
event.waitKeys()

text1 = 'Przed rozpoczęciem każdej aktywności na ekranie pojawi się napis Gotowy?(naciśnij SPACJĘ). \
Jeśli chcesz, możesz brać przerwy i czekać na ekran Gotowy?, jeśli chcesz zrobić przerwę i zadać pytania Eksperymentatorowi.'

text2 = 'Masz możliwość przećwiczenia zadania przed rozpoczęciem prawdziwego eksperymentu. Kiedy będziesz gotowy, \
naciśnij dowolny klawisz, aby kontynuować.'


showInstructions(text1,text2)


reps = 1 
practiceTrials = generateExperimental()

for trialNum,trial in enumerate(practiceTrials):
    readySequence()
    presentStimuli(1, trial['askConf'],trial['latency'])
    

text = 'Teraz rozpocznie się prawdziwy eksperyment. Pamiętaj, że możesz brać tyle przerw, ile chcesz, i że powinieneś zadać Eksperymentatorowi pytania, jeśli masz jakiekolwiek wątpliwości. Kiedy będziesz gotowy, naciśnij dowolny klawisz, aby kontynuować.'

instruct = visual.TextStim(win,color='#fdfdfd',pos=[0,0],wrapWidth=1.2,height=.06,text=text)
instruct.draw()
win.flip()
event.waitKeys()
    

reps = 14 
experimentalTrials = generateExperimental()

for trialNum,trial in enumerate(experimentalTrials):
    readySequence()
    circlePositions,squarePositions,response,responseTime,choiceTime,confAnswer,colorOptions = presentStimuli(1,trial['askConf'],trial['latency'])
    addTrialVariables()
    writeToFile(dataFile,trial)