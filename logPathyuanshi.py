

import  os
import  sys
import  re


import  datetime
import  time

def readTime( fp ):
    #print fp
    startTime = 0
    endtime = 0
    with open(fp,"r") as F:

        for item in F :
            startRe =  re.search('(?<=start ).+$',item)
            endRe = re.search('(?<=stop ).+$',item)

            if startRe is not None:
                d = datetime.datetime.strptime(startRe.group(), "%Y-%m-%d %H:%M:%S")
                t = d.timetuple()
                startTime =   int(time.mktime(t))


            if endRe is not None:
                d = datetime.datetime.strptime(endRe.group(), "%Y-%m-%d %H:%M:%S")
                t = d.timetuple()

                endtime =  int(time.mktime(t))
                #print  endRe.group()

    return  (startTime,endtime,fp)



def sortList(listTime ,bound):

    return map(lambda x: (x[0] - bound, x[1] - bound), listTime)


if __name__ == '__main__':

    path = sys.argv[1]

    listBwaProcess = []
    listIndex = []
    listMerge = []
    listGvc = []
    taskDict = {}
    for root, dirs, files in os.walk(path):

        for fileName in files:
            if re.search('^bwa.+.log$',fileName):
                listBwaProcess.append(readTime(root+fileName))

            if re.search('^index.+.log$',fileName):
                listIndex.append(readTime(root+fileName))

            if re.search('^merge.+.log$',fileName):
                listMerge.append(readTime(root+fileName))

            if re.search('^gvc.+.log$', fileName):
                listGvc.append(readTime(root + fileName))

        L = []
        for item  in (listBwaProcess,listIndex,listMerge,listGvc):
            L.extend(item)
        L= sorted(L,key= lambda  x:x[0])

        listGvc = sorted(listGvc, key= lambda  x: x[0] -x[1]) 
        print listGvc[0][2]

        #listBwaProcess = [(3,5),(1,3)]
        #print sorted(listBwaProcess, key=lambda x: x[1])
        #taskDict['bwa'] = sortList(listBwaProcess,L[0][0][0])
        #taskDict['index'] = sortList(listIndex,L[0][0][0])
        #taskDict['merge'] = sortList(listMerge,L[0][0][0])
        #taskDict['gvc'] = sortList(listGvc,L[0][0][0])
         
   #print taskDict
       # pass
