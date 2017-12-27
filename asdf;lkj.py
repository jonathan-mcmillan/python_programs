from cs1graphics import *
numLevels = 8
unitSize = 12
screenSize = unitSize * (numLevels + 1)
paper = Canvas(screenSize, screenSize)
for level in range(numLevels):
    centerX = screenSize / 2
    leftMostX = centerX - unitSize / 2 * level
    centerY = (level +1) * unitSize
    for blockCount in range(level +1):
        block = Square(unitSize)
        block.move(leftMostX + blockCount * unitSize, centerY)
        block.move(centerX, centerY)
        block.setFillColor('gray')
        paper.add(block)
    
'''
from cs1graphics import *
numLevels = 8
unitSize = 12
screenSize = unitSize * (numLevels + 1)
paper = Canvas(screenSize, screenSize)
for level in range(numLevels):
    width = (level +1) * unitSize
    height = unitSize
    block = Rectangle(width, height)
    
    width = (level +1) * unitSize
    block = Rectangle(width, unitSize)

    block = Rectangle((level +1)* unitSize, unitSize)

    these two do the same thing as the first set of code
    
    centerX = screenSize/2
    centerY = (level +1) * unitSize
    block.move(centerX, centerY)
    block.setFillColor('gray')
    paper.add(block)
    '''
