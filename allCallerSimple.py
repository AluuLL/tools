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

    def outLine(self,inputList,num,germline,mainLines,sampleLines):
        outputList = []
        for id in range(0,num,1):
            # germLine Handle
            if id == 0 and germline == False:
                outputList.append([])
            else:
                outputList.append(map(lambda x :x if  x <= mainLines else x + sampleLines*id,inputList))
        return  outputList

    def run(self):

        inputFile = self.kwargs.get('inputFile')
        inputLines = self.kwargs.get('inputLines')
        inputFormat = self.kwargs.get('inputFormat')
        inputMatrix = self.kwargs.get('inputMatrix')
        SampleList = self.kwargs.get('SampleName').split(',')
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
        outputSampeColunm = int(inputLines.split(':')[0])
        fpLines = map(lambda x : int(x),inputLines.split(':')[1].split(','))
        finalOutputList = self.outLine(fpLines,len(SampleList),type,int(mainLines),int(sampleLines))
        #print finalOutputList
        inputInst =  FileIter(inputFile)
        MatrixInst = FileIter(inputMatrix)

        for ( inputItem , matrixLineItem) in  izip(inputInst,MatrixInst):
            for  (id ,cellItem) in  enumerate(matrixLineItem):
                # Somatic Normal can't output
                if  id == 0 and   type == False:
                    continue

                if cellItem == '1':
                    #print id ,finalOutputList[id],len(inputItem)
                    writeData = map(lambda x : inputItem[x-1],finalOutputList[id])
                    if outputSampeColunm != 0:
                        writeData.insert(outputSampeColunm-1,SampleList[id])
                    F.write('\t'.join(writeData))
                    F.write('\n')


def cmdPhase( argv):
    callerDict = {
        'inputFile':argv[0],
        'inputLines':argv[1],
        'inputFormat':argv[2],
        'inputMatrix':argv[3],
        'type':argv[4],
        'outputFileName':argv[5],
        'SampleName':argv[6]
    }
    return callerDict


if __name__ == '__main__':
    callerDict = cmdPhase(sys.argv[1:])
    inst = allCallerSimple(**callerDict)
    inst.run()




