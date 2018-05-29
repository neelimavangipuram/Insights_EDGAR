import datetime as dt
import collections
from collections import OrderedDict

sourceCode = '../src/sessionization.py'
inputFile = '../input/log.csv'
inactivityFile = '../input/inactivity_period.txt'
outputFile = '../output/sessionization.txt'

ipDict = collections.defaultdict(list)
result = []


def outputResult():
    with open(outputFile) as fin:
        lines = (line.rstrip() for line in fin)
        unique_lines = OrderedDict.fromkeys((line for line in lines if line))

    with open(outputFile, 'w') as op:
        for row in unique_lines.keys():
            userDetails = row + "\n"
            op.write(userDetails)


def checkInactivity(inTimestamp):
    global ipDict
    global result
    for key, value in ipDict.items():
        diff = inTimestamp - ipDict[key][1]
        if diff.total_seconds() > inactivityValue:
            duration = ipDict[key][1] - ipDict[key][0]
            result.append([key, ipDict[key][0], ipDict[key][1], int(duration.total_seconds()) + 1, ipDict[key][2]])

    with open(outputFile, 'a') as output:
        for value in result:
            userDetails = value[0] + "," + value[1].strftime('%Y-%m-%d %H:%M:%S') + "," + value[2].strftime(
                '%Y-%m-%d %H:%M:%S') + "," + str(value[3]) + "," + str(value[4]) + "\n"
            output.write(userDetails)
    result = []
    outputResult()


# Get the inactivity value from the inactivity_period file
with open(inactivityFile, 'r') as inactivity_period:
    for value in inactivity_period:
        inactivityValue = int(value)

with open(outputFile, 'w') as output_file:
    pass

# Read the input log file and create
with open(inputFile) as logFile:
    # Skip the headers
    logFile.readline()
    for line in logFile:
        reqReceived = line.split(',')

        # Get the IP address required
        userId = reqReceived[0]

        # Create the datetime object by concatenating 'date' and 'time' fields
        timestamp = dt.datetime.strptime(reqReceived[1] + ' ' + reqReceived[2], '%Y-%m-%d %H:%M:%S')

        checkInactivity(timestamp)

        changeTimestamp = False
        for key, value in ipDict.items():
            if key == userId:
                changeTimestamp = True
                break

        if changeTimestamp:
            ipDict[userId][1] = timestamp
            ipDict[userId][2] += 1
        else:
            ipDict[userId].extend([timestamp, timestamp, 1])

checkInactivity(dt.datetime.now())
