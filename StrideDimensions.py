#!/usr/bin/env python

"""
# StrideDimension is an implementation of the ideas
# StrideDimension is based on the ideas in Computerphile video
# "Multi-Dimensional Data (as used in Tensors)
# https://www.youtube.com/watch?v=DfK83xEtJ_k
#
# The main thing is to find data/loop through multidimensional data
# that is represented in one dimension. For more info, please watch
# linked youtube-video above.
#
# Usage:
#
#   Fast example:
#       Tic-Tac-Toe board   -> ticTacToeBoard = StrideDimension([3,3])
#       Sudoku board        -> sudokuBoard = StrideDimension([3,3,9])
#       Chessboard          -> chessBoard = StrideDimension([8,8])
#
# Crate an object of class StrideDimension with values:
# inDim -   a tuple with the dimensions that shall be represented.
#           Example 1: To represent two dimension, eg. tic-tac-toe board
#           use isDim = (3,3). This means two dimensions with 3 in each
#           dimension.
#           Example 2: A sudoku board can be represented with inDim=(3,3,9)
#           meaning, nine smaller 3x3 squares.
#           Example 3: Chess board - inDim=(8,8)
#
# defaultData - The data used as default for each position in StrideDimension object.
#               If left out, all data will be "None" as default. Which is the typical use.
#               Example: Can be used to put '-' for a sudoku-board.
#

"""

__author__ = "Helge Modén, www.github.com/helgemod"
__copyright__ = "Copyright 2020, Helge Modén"
__credits__ = None
__license__ = "MIT"
__version__ = "1.0.1"
__maintainer__ = "Helge Modén, https://github.com/helgemod/StrideDimensions"
__email__ = "helgemod@gmail.com"
__status__ = "https://github.com/helgemod/StrideDimensions"
__date__ = "2020-11-17"

########################################################################
class StrideDimension:


    #Note, offset is not really used in this version.
    offset = 0 #Offset where acual data starts in theData (Typically 0)
    dimensions = []
    strides = [] #How many jumps in "theData" to reach next data in that dimension.
    theData = [] #The actual data

    KEY_OFFSET      = "KEY_StrideDimensionOffset"
    KEY_DIMENSIONS  = "KEY_StrideDimensionDimensions"
    KEY_STRIDES     = "KEY_StrideDimensionStrides"
    KEY_THEDATA     = "KEY_StrideDimensionTheData"

    def __init__(self,inDim,offset=0,fillWithNumbering=False):

        #Check valid data
        if not (isinstance(inDim,list) or isinstance(inDim,tuple)):
            inDim = [1,1]

        if not isinstance(fillWithNumbering,bool):
            fillWithNumbering=False

        if not isinstance(offset,int) or offset<0:
            offset=0

        #SETUP Data
        self.offset=offset
        self.dimensions = inDim
        dataLength = 1
        for element in inDim:
            dataLength *= element

        for i in range(dataLength):
            if fillWithNumbering:
                self.theData.append(i+1)
            else:
                self.theData.append(None)


        self.strides = [0]*len(inDim)
        self.strides[0]=1 #Alwas one step between values in first dimension
        for i in range(1,len(inDim)):
            self.strides[i] = self.strides[i-1]*inDim[i-1]

    #For debug reason
    def print(self):
        print("*"*10)
        print("StrideDimension object")
        print("-"*10)
        print("Offset: "+str(self.offset))
        print("dimensions: " + str(self.dimensions))
        print("strides: " + str(self.strides))
        print("theData: ")
        print(self.theData)
        print("-" * 10)

    #Used when restarting a program and read data saved to file.
    #Note, see "getDataForSave" below.
    def setUpWithData(self,setupDic):
        self.offset = setupDic[self.KEY_OFFSET]
        self.dimensions = setupDic[self.KEY_DIMENSIONS]
        self.strides = setupDic[self.KEY_STRIDES]
        self.theData = setupDic[self.KEY_THEDATA]

    #Returns a Dictionary representation for this object. Used to save to binary file.
    #To recreate this object -> Create object with init, then call "setUpWithData" with
    #the from file read Dictionary.
    def getDataForSave(self):
        return  {self.KEY_OFFSET:self.offset,self.KEY_DIMENSIONS:self.dimensions,self.KEY_STRIDES:self.strides,self.KEY_THEDATA:self.theData}

    #Set ONE value at coords (on format (2,3,4))
    def setData(self,coords,value):
        index = self.__indexForDimCoordinate(coords)
        self.__setDataAtIndex(index,value)

    #Get ONE value at coords (on format (2,3,4))
    #For multiple value, choose loopThruData or loopThruDimension below!
    def getData(self,coords):
        index = self.__indexForDimCoordinate(coords)
        if index == None:
            return None
        return self.theData[index]


    # def getDimensionalData(self,inDims):
    #
    # Get all data in specified dimensions according to "inDims"
    #
    # "inDims" is a tuple that represent the dimensions when created this object.
    # Format for dims: (None,1,2)
    # Means loop through dimension 1 while dimension 2 is fixed to value 1 and dimension 3 is fixed to value 2.
    #
    # Example:
    # A StrideDimension object is created like: sd = StrideDimension((3,3),fillWithNumbering=True) will look like:
    #   1 2 3
    #   4 5 6
    #   7 8 9
    # getDimensionalData((None,1)) will return [1,2,3]
    # getDimensionalData((1,None)) will return [1,4,7]
    # getDimensionalData((2,None)) will return [2,5,8]
    #
    # (To retrieve diagonal data use "getDimensionalDataWithDirection" below.)
    #
    # Further examples:
    # To get all values in the middle square of a sudoku board call:
    #   getDimensionalData((None,None,5)) - Saying "loop through all x-data and y-data in dimension 5."
    def getDimensionalData(self,inDims):
        #Sanity check
        if not len(inDims) == len(self.dimensions):
            return None

        if not None in inDims:
            index = self.__indexForDimCoordinate(inDims)
            if index == None:
                return None
            else:
                return self.theData[index]

        retList = []
        buildList = list(inDims)
        for x in range(len(inDims)-1,-1,-1):
            if inDims[x] == None:
                for dims in range(self.dimensions[x]):
                    buildList[x] = dims+1
                    retList = retList + [self.getDimensionalData(tuple(buildList))]
                return retList

    # def getDimensionalDataWithDirection(self, startCoord, direction):
    #
    # Best used to get DIAGONALS from dimensions!!
    #
    # Starts at startCoord (tuple) and collect data in direction (tuple)
    # until it reaches the end of any dimension.
    #
    # direction: 1=>forward -1=>backward 0=>don't go through this dimension
    #
    # Example:
    # A StrideDimension object is created like: sd = StrideDimension((3,3),fillWithNumbering=True).
    # This will look like:
    #   1 2 3
    #   4 5 6
    #   7 8 9
    #
    #   getDimensionalDataWithDirection((1,1), (1, 1)) will return [1,5,9]
    #   getDimensionalDataWithDirection((1,3), (1,-1)) will return [7,5,3]
    #   getDimensionalDataWithDirection((3,3), (-1,-1)) will return [9,5,1]
    #
    def getDimensionalDataWithDirection(self, startCoord, direction):
        startIndex = self.__indexForDimCoordinate(startCoord)
        if startIndex==None:
            return []
        retList = [self.theData[startIndex]]
        nextCoord = self.__getNextCoordinateAfter(startCoord,direction)
        while not nextCoord == None:
            retList.append(self.theData[self.__indexForDimCoordinate(nextCoord)])
            nextCoord = self.__getNextCoordinateAfter(nextCoord, direction)
        return retList


    #
    # getIndexAtFirstOccurrenceOfData - setDataAtIndex
    #
    # Use these methods in conjunction with each other!
    #
    # Starts at the beginning of internal represenation of data
    # and returns index of first occurrence of "inData".
    def getIndexAtFirstOccurrenceOfData(self,inData):
        for i in range(len(self.theData)):
            if self.theData[i] == inData:
                return i
        return None

    # Place data directly indexed - Use in conjunction with "getIndexAtFirstOccurrenceOfData"
    def setDataAtIndex(self, index, value):
        if index == None or not isinstance(index,int):
            return
        if index < 0 or index >= len(self.theData):
            return
        self.theData[index] = value

    # Fill all data in all dimensions with "data"
    def fillData(self,data):
        mult=len(self.theData)
        self.theData = [data]*mult








    ########################################################
    #
    #   Private methods of StrideDimension class
    #
    ########################################################

    # dim is a tuple with the coordinates. Coordinate begins at 1 for each dimension. (1,1,1) is "Origo".
    def __indexForDimCoordinate(self,dim):
        if not len(dim)==len(self.dimensions):
            return None
        index = 0
        for x in range(len(dim)):
            index += (dim[x]-1) * self.strides[x]
        if index<0 or index>=len(self.theData):
            return None
        return index

    def __getNextCoordinateAfter(self,inCoord,dir):
        nextCoord = []
        #inIndex = self.__indexForDimCoordinate(inCoord)
        for x in range(len(inCoord)):
            nextCoord.append(inCoord[x] + dir[x])
        for y in range(len(self.dimensions)):
            if nextCoord[y] <= 0 or nextCoord[y] > self.dimensions[y]:
                return None
        #outIndex = self.__indexForDimCoordinate(nextCoord)
        return nextCoord