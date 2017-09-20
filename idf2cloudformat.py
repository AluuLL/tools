#!/usr/bin/python


import  sys
from itertools import  *
import time

class FileIter():
    def __init__(self,fileName):
        try:
            self.file = open(fileName,'r')
        except IOError:
            self.ERROR = True
            print "Can't open %s!" %(fileName)

    def next(self):
        line = self.file.readline()
        if  line == '':
            raise StopIteration
        else:
            return   line.strip('\n').split('\t')

    def __iter__(self):
        return self

class allCallerSimple():

    def __init__(self,**kwargs):
        self.kwargs = kwargs

    def outLine(self,inputList,num,mainLines,sampleLines):
        outputList = []
        for id in range(0,num,1):
            outputList.append(map(lambda x :x if  x <= mainLines else x + sampleLines*id,inputList))
        return  outputList

    def run(self):

        inputFile = self.kwargs.get('inputFile')
        inputLines = self.kwargs.get('inputLines')
        inputFormat = self.kwargs.get('inputFormat')
        inputMatrix = self.kwargs.get('inputMatrix')
        SampleList = self.kwargs.get('SampleName').split(',')
        BaseList = self.kwargs.get('BaseNum').split(',')
        type = self.kwargs.get('type')
        outputFileName =  self.kwargs.get('outputFileName')
        ##
        try:
           F = open(outputFileName, 'w')
        except IOError:
            print 'IO error: %s' %(outputFileName)
            sys.exit(-1)

        if type == '1':
            type = True
        else:
            type = False

        ( mainLines , sampleLines) =  inputFormat.split(',')
        #outputSampeColunm = int(inputLines.split('')[0])
        fpLines = map(lambda x : int(x),inputLines.split(','))
        finalOutputList = self.outLine(fpLines,len(SampleList),int(mainLines),int(sampleLines))
        #print finalOutputList
        inputInst =  FileIter(inputFile)
        MatrixInst = FileIter(inputMatrix)
     # count = 0
        for ( inputItem , matrixLineItem) in  izip(inputInst,MatrixInst):

            # List A -> Write Data
            # List B -> output sample List
            WriteListB = []
            OSampleList = []
            #output 3
            WriteListB.extend(map(lambda x: inputItem[int(x)-1],BaseList))
       #     count = count +1
            for (id ,cellItem) in  enumerate(matrixLineItem):
                #  output Lines -> write Data
                #   matrix item '1' -> sample List
                WriteListB.extend(map(lambda x : inputItem[x-1],finalOutputList[id]))
                #writeData.insert(outputSampeColunm - 1, SampleList[id])
               # if cellItem == '1':
               #    OSampleList.append(SampleList[id])
            #if len(OSampleList) == 0:
             #   OSampleList = '-'

            # samplie  ',' -> str
            # str append Write Data
            # write File
           # WriteListB.append(','.join(OSampleList))
            F.write('\t'.join(WriteListB)+ '\n')
      #  print count


def cmdPhase( argv):
    callerDict = {
        'inputFile':argv[0],
        'inputLines':argv[1],
        'inputFormat':argv[2],
        'inputMatrix':argv[3],
        'outputFileName':argv[4],
        'SampleName': argv[5],
        'BaseNum': argv[6]

    }
    return callerDict


if __name__ == '__main__':
    callerDict = cmdPhase(sys.argv[1:])
    inst = allCallerSimple(**callerDict)
    inst.run()




