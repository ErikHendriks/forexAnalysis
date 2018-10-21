import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import numpy as np
import time
import functools

totalStart = time.time()



def convert_date(date_bytes):
    return mdates.strpdate2num('%Y%m%d%H%M%S')(date_bytes.decode('ascii'))
#bid,ask = usecols = (1,2)
date,bid,ask = np.loadtxt('/path/to/GBPUSD1d.txt',
                              unpack=True,
                              delimiter=',',
                              converters={0:convert_date})


def percentChange(startPoint, currentPoint):
    try:
        x = ((float(currentPoint)-startPoint)/abs(startPoint))*100.00
        if x == 0.0:
            return 0.0000000001
        else:
            return x
    except:
        return 0.00000001

def patternStorage():
    patStartTime= time.time()
    x = len(avgLine)-60
    y = 31
    while y < x:
        pattern = []
        i = 29
        while i >= 0:
            ps = percentChange(avgLine[y-30],avgLine[y-i])
            pattern.append(ps)
            i-=1

        outcomeRange = avgLine[y+20:y+30]
        currentPoint = avgLine[y]
        try:
            avgOutcome = functools.reduce(lambda x, y: x+y, outcomeRange)/len(outcomeRange)
        except Exception as e:
            print(str(e))
            avgOutcome = 0

        futureOutcome = percentChange(currentPoint, avgOutcome)

        patternAr.append(pattern)
        performanceAr.append(futureOutcome)

        y+=1

    patEndTime = time.time()

def currentPattern():
    i = 30
    while i > 0:
        cp = percentChange(avgLine[-31],avgLine[-i])
        patForRec.append(cp)
        i-=1

def patternRecognition():
    patFound = 0
    
    for eachPattern in patternAr:
        i = 0
        howSim = 0
        while i <= 29:
            sim = 100.00 - abs(percentChange(eachPattern[i], patForRec[i]))
            i+=1
            howSim+=sim
        
        if howSim/30 > 80:
            print(howSim/30)
            patDex = patternAr.index(eachPattern)
            print('######')
            print('patForRec > ',patForRec)
            print('eachPattern > ',eachPattern)
            print('######!!!')
            print('predicted outcome > ',performanceAr[patDex])
            xp = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
            fig = plt.figure()
            plt.plot(xp, patForRec)
            plt.plot(xp, eachPattern)
            plt.show()
          
def graphRawFX():
    fig = plt.figure(figsize=(10,7))
    ax1 = plt.subplot2grid((40,40),(0,0),rowspan=40,colspan=40)

    ax1.plot(date,bid)
    ax1.plot(date,ask)
    plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)
    
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)

    ax1_2 = ax1.twinx()
    ax1_2.fill_between(date,0,(ask-bid),facecolor='g',alpha=.3)

    plt.subplots_adjust(bottom=.23)

    plt.grid(True)
    plt.show()

dataLenght = int(bid.shape[0])
print(dataLenght)
toWhat = 3700
while toWhat < dataLenght:
    avgLine = ((bid+ask)/2)
    avgLine = avgLine[:toWhat]
    patternAr = []
    performanceAr = []
    patForRec = []

    patternStorage()
    currentPattern()
    patternRecognition()
    totalTime = time.time()-totalStart
        
    toWhat+=1

print('Time elapsed: ',totalTime)
