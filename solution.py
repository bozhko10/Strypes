# Python progam that finds the longest adjacent sequence 
# of colors in a matrix (2D grid).
# Colors are represented by 'R', 'G', 'B' characters.
#
# The matrix can be input manually. Example:
# ./solution.py
# Please, enter the size of the matrix (rows columns): 2 2
# 0: B B
# 1: R G

# The program also accepts from one to four additional 
# parameters (names of the test files in /test directory)
# Example:
# ./solution.py test_1 test_2 test_3 test_4

# Bozhidar Nedelchev 18.05.2019

# Import 'sys' library in order to read from the terminal
import sys

# Class Matrix (object for holding a matrix)
class Matrix():

    # Class variables
    theMatrix = []
    width = 0
    height = 0

    # Constructor
    # Takes a boolean variable and a string
    def __init__(self, line, isItFromFile):

        # Clears the matrix every time, a new one is made
        self.theMatrix.clear()

        # If it is true this means that the given string is name of a test file
        if(isItFromFile):
            # Reads from the file
            file = open("tests\\" + line)
            # First line is the file contains the parameters of the matrix
            firstLine = file.readline()

            (givenHeight, sep, givenWidth) = firstLine.strip().partition(' ')

            # Sets the class variable
            self.width = int(givenWidth)
            self.height = int(givenHeight)

            # Reads the matrix from the file
            for line in file:
                row = line.split()
                self.theMatrix.append(row)

            file.close()
        # If it is false - the line contains the parameters of the matrix
        else:
            (givenHeight, sep, givenWidth) = line.strip().partition(' ')

            # Sets the class variable
            self.height = int(givenHeight)
            self.width = int(givenWidth)

            # Reads the matrix from the terminal
            for i in range (self.height):
                nextLine = input(str(i) + ": ").strip().split()
                if (len(nextLine) != self.width):
                    print("The number of colors on each line should be equal" 
                    + "to the given number of columns!")
                    exit()
                self.theMatrix.append(nextLine)

    # Function for printing the matrix (it is not used in the main method) 
    def printMatrix(self):
        for i in range(len(self.theMatrix)):
            print(str(i) + ': ', end = '')
            for j in range(len(self.theMatrix[i])):
                print(self.theMatrix[i][j], end=' ')
            print()

    # Function for the getting the area of the matrix
    def getArea(self):
        return self.height * self.width

    # Function for finding the longest path from given cell(i, j)
    def findPathFromCell(self, i, j, pathLenght, isBeenHere):

        # Saving the coordinates of the starting cell in different variables
        startI = i
        startJ = j
        # Sets the pathLenght of cell (startI, startJ) to 0
        pathLenght[startI][startJ] = 0

        # While the cell (i, j) is in the matrix, execute:
        while not(i < 0 or i >= self.height or j < 0 or j >= self.width):
            # Sets the cell (i, j) as true in order to know later if this cell
            # is been in the while or not
            isBeenHere[i][j] = True 
 
            # Checks if the cell (i, j) has already had longest path
            if (pathLenght[i][j] != -1):
                # If the path till now is less than the path from cell(i, j)
                if (pathLenght[startI][startJ] < pathLenght[i][j]):
                    # Set the path with biggest number and exit the while
                    pathLenght[startI][startJ] = pathLenght[i][j]
                    break

            # Increases the path with one
            pathLenght[startI][startJ] += 1
            # Sets the path of current cell to be equal the one of starting cell
            pathLenght[i][j] = pathLenght[startI][startJ]
            
            # Checks if the RIGHT cell has the same element as current
            if (j < self.width - 1 
                and ((self.theMatrix[i][j]) == self.theMatrix[i][j + 1]) 
                and not(isBeenHere[i][j + 1])):
                # Goes RIGHT
                j += 1
                continue 

            # Checks if the LEFT cell has the same element as current
            if (j>0 
                and (self.theMatrix[i][j] == self.theMatrix[i][j - 1]) 
                and not(isBeenHere[i][j - 1])):
                # Goes LEFT
                j -= 1
                continue

            # Checks if the DOWN cell has the same element as current
            if (i>0 
                and (self.theMatrix[i][j] == self.theMatrix[i - 1][j]) 
                and not(isBeenHere[i - 1][j])): 
                # Goes DOWN
                i -= 1
                continue 

            # Checks if the UP cell has the same element as current
            if (i < self.height - 1 
                and (self.theMatrix[i][j] == self.theMatrix[i + 1][j]) 
                and not(isBeenHere[i + 1][j])):
                # Goes UP
                i += 1
                continue
            
            # Exit if there other direction to go
            break

        # Return the path lenght of the given cell     
        return pathLenght[startI][startJ]

    # Function for finding the longest path in the matrix
    def findLongestSequence(self):
        # Setting the longest sequence to be 1
        longestSeq = 1

        # Matrix for holding the lenght of every pathLenght
        pathLenght = [[-1 for i in range(self.width)]
                       for i in range(self.height)]

        # Goes through every cell in the matrix
        for i in range(self.height):
            for j in range(self.width):
                if (pathLenght[i][j] == -1):
                    #Boolean matrix whether the cell has been part of the path
                    isBeenHere = [[False for i in range(self.width)]
                                   for i in range(self.height)]
                    # Finding the longest path from every cell
                    pathLenght[i][j]  = self.findPathFromCell(i, j,
                                                         pathLenght, isBeenHere)
                #Finding the longestSequence, so far
                longestSeq = max(longestSeq, pathLenght[i][j])
                # If the longest path is equal to the area that this means 
                # there cannot be found longer path than this
                if (longestSeq == self.getArea()):
                    break
        # Returns the result
        return longestSeq 

# Creating a boolean variables
isItFromFile = None

# Checks if there are additional parameters
if (len(sys.argv) > 1 and len(sys.argv) <= 5):
    # Sets the variable to True
    isItFromFile = True
    for numOfParm in range(1, len(sys.argv)):
        # For every given parameter, it creates a matrix
        matrix = Matrix(sys.argv[numOfParm], isItFromFile)
        # Print the result after calling the function for finding longest path 
        print("The number of the longest adjacent sequence from " 
        + sys.argv[numOfParm] + " is " + str(matrix.findLongestSequence()))
# This means there are no additional parameters
elif (len(sys.argv) == 1):
    # Sets the variable to True
    isItFromFile = False
    # Getting the parameters of the wanted matrix
    firstLine = input("Please, enter the size of the matrix (rows columns): ")
    # Creates a matrix with given parameters
    matrix = Matrix(firstLine, isItFromFile)
    # Print the result after calling the function for finding the longest path
    print("The number of the longest adjacent sequence is " 
    + str(matrix.findLongestSequence()))
# There are more than 4 additional parameters
else:
    print("The program accepts from one to four additional parameters!")
