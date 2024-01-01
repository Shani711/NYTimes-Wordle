import Draw
import random

def getGuess(validWords, guess, guessNum):
    key = ""
    
    # get new letter until the word is complete
    while len(guess) < 5:
        if Draw.hasNextKeyTyped():
            
            newKey = Draw.nextKeyTyped()
            # changes every letter to lower case
            newKey = newKey.lower()
            # if a key has been pressed, add only LETTERS to the guess word 
            if newKey in "abcdefghijklmnopqrstuvwxyz":
                key = newKey
                guess += [key]     
                 
            # if a backspace if written it deletes the most recent letter
            elif newKey == "backspace" and len(guess) > 0:
                del guess[-1]
                # places white box on top of deleted letter
                delLetter(guessNum, guess)
                # redraw the updated guess
                redrawGuess(guessNum, guess)
                
        # if 5 letters were typed and not a real word, it will delete the whole word
        if len(guess) == 5 and ''.join(guess) not in validWords:
            del guess[:]
            # places white boxes on top of the whole invalid word
            clearGuess(guessNum, guess)
            
        # ajb: redraw the guess in a specially designated area on canvas
        # first draw a white box in that area, then loop through the
        # letters of the guess and display them on the guessNumber'th row
        clearGuess(guessNum, guess)     # avoids the letter from becoming thick
        redrawGuess(guessNum, guess)
        
        
    # if the word typed is valid, return the guess 
    return guess


# letters in uncolored boxes
def redrawGuess(guessNum, guess):
    Draw.setColor(Draw.BLACK)
    Draw.setFontSize(20)
    
    # calculated coordinates for words based on what guess number the user is up to
    # writes the letters in correct placement
    yLetter = 180
    xLetter = 185.5
    for j in range(guessNum):
        yLetter += 80
    for i in range(len(guess)):
        Draw.string(guess[i], xLetter, yLetter)
        xLetter += 80

    # draw uncolored boxes
    width = 75
    length = 75          
    yCoord = 70
    xCoord = 70
    for i in range(6):
        yCoord += 80
        xCoord = 70
        for j in range(5): 
            xCoord += 80
            Draw.setColor(Draw.BLACK)
            Draw.rect(xCoord, yCoord, width, length) 
    Draw.show()


def colorCheck(guessNum, guess, correctWord):
    width = 75
    height = 75          
    yCoord = 150
    xCoord = 150
    
    # calculates new y coord depending on what guess number it is
    for j in range(guessNum):
        yCoord += 80
        
    for i in range(len(guess)):
        #print("guess number:", guessNum, "xCoord:", xCoord, "yCoord:", yCoord, "letter:", guess[i], flush = True)
        
        # set the color box accordingly if right/wrong
        # green if the letter is the same
        if guess[i] == correctWord[i]:
            Draw.setColor(Draw.GREEN)
            Draw.filledRect(xCoord, yCoord, width, height)
        # yellow if the guessed letter is in the correct word
        elif guess[i] in correctWord:
            Draw.setColor(Draw.YELLOW)
            Draw.filledRect(xCoord, yCoord, width, height)
        # gray if not in word at all
        else:
            Draw.setColor(Draw.LIGHT_GRAY)
            Draw.filledRect(xCoord, yCoord, width, height)

        # incriment the x coord so the next colored box is in next position
        xCoord += 80
    
    Draw.show()
    redrawGuess(guessNum, guess)

def delLetter(guessNum, guess):
    width = 75
    height = 75          
    yCoord = 150
    xCoord = 150
    
    # calculates which box to redraw
    for j in range(guessNum):
        yCoord += 80
    for i in range(len(guess)):
        xCoord += 80
    # white boxes to cover already drawn letters
    Draw.setColor(Draw.WHITE)
    Draw.filledRect(xCoord, yCoord, width, height)
    
def clearGuess(guessNum, guess):
    width = 75
    height = 75          
    yCoord = 150
    xCoord = 150
    
    # calculating row
    for j in range(guessNum):
        yCoord += 80    
    
    # clears the whole row by placing white boxes over invalid word
    for i in range(5):
        Draw.setColor(Draw.WHITE)
        Draw.filledRect(xCoord, yCoord, width, height)  
        xCoord += 80
   

def playGame():
    # create screen
    size = 750
    Draw.setCanvasSize(size, size)
    
    # write wordle on top
    Draw.setFontSize(32)
    Draw.setColor(Draw.BLACK)            
    Draw.string("WORDLE", 275, 100) 
    
    # take all the 5 letter words and place them into the list called validWords
    # "words5-knuth.txt" found at URL https://introcs.cs.princeton.edu/java/data/ renamed to "wordle5letterwords.txt"
    validWords = []
    fiveLetterWords = open("wordle5letterwords.txt")
    for line in fiveLetterWords:
        validWords += [line[:-1]]
    fiveLetterWords.close()
    
    # shuffle the list of 5 letter words
    random.shuffle(validWords)
    
    # the correct word:
    correctWordString = str(validWords[0])
    correctWord = []
    # change currentWordString from string to list and delete the last index(the new line)
    for char in range(len(correctWordString)):
        correctWord += [str(correctWordString[char])]
    
    # coordinates of win/lose message
    xWin = 75
    yWin = 250
    win = False
    
    guessNum = 0                # 0, 1, 2, 3, 4, 5
    
    # 6 tries
    while guessNum < 6 and win == False:
        # reset the guess each time
        guess = []
        
        # returns a 5 letter list - will continue in getGuess until a 5 letter word comes out
        getGuess(validWords, guess, guessNum)
        
        # draws the colors accordingly
        colorCheck(guessNum, guess, correctWord)        
        
        # win message if the guess is correct
        if guess == correctWord:
            win = True
            Draw.setFontSize(140)
            Draw.setColor(Draw.RED)            
            Draw.string("You win!", xWin, yWin) 
            
        # incriment the guessNum since the guess was successful    
        guessNum += 1
        
    # lose message
    if guess != correctWord:
        Draw.setFontSize(130)
        Draw.setColor(Draw.RED)    
        Draw.string("You lost :(", xWin, yWin)
      
    Draw.show() 
playGame()
