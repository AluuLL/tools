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
       # inputMatrix = self.kwargs.get('inputMatrix')
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
       # MatrixInst = FileIter(inputMatrix)
     # count = 0
        for inputItem  in  inputInst:
            if inputItem[2] == 'D':
                inputItem.insert(2,str(int(inputItem[1])+ len(inputItem[3]) - len(inputItem[4])))
            else:
                inputItem.insert(2,inputItem[1])
            inputItem.insert(6,SampleList[0])
            F.write('\t'.join(inputItem) + '\n')

def cmdPhase( argv):
    callerDict = {
        'inputFile':argv[0],
        'inputLines':argv[1],
        'inputFormat':argv[2],
      #  'inputMatrix':argv[3],
        'outputFileName':argv[3],
        'SampleName': argv[4],
        'BaseNum': argv[5]

    }
    return callerDict


if __name__ == '__main__':
    callerDict = cmdPhase(sys.argv[1:])
    inst = allCallerSimple(**callerDict)
    inst.run()




