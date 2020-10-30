import os


# traceFile attributes
#   event   time    formNode    toNode  pktType     pkeSize    flags   flowId   srcAddr     dstAddr    seqNum   pktId

# calculate throughput: return rate in kb
def throughPut(begin, end, dataSize):
    if end - begin == 0:
        return 0
    return float(dataSize * 8 / (end - begin) / 1024)


# calculate dropRate
# return a digit represents the drop rate
def Drop(countSent, countReceive):
    if countSent == 0:
        return 0
    return float(1 - float(countReceive) / float(countSent))


# calculate latency
# return the latency in ms
def latency(duration, totalPacket):
    if totalPacket == 0:
        return 0
    return float(duration / totalPacket * 1000)


"""
process the data from trace file, calculate the throughput, dropRate, and latency.
return: the value of throughput, dropRate, and latency value  
"""


def parseData(tcpName, cbrRate):
    filename = "tcp_" + tcpName + "_atRate" + str(cbrRate) + ".tr"
    with open(filename) as file:
        content = file.readlines()
        totalReceive = 0
        begin = 0
        end = 15
        sentRecord = {}
        receivedRecord = {}
        totalReceivePakcet = []
        duration = 0
        countReceive = 0
        countSent = 0
        for line in content:
            # separate the line data
            data = line.split()
            event = data[0]
            time = float(data[1])
            fromNode = data[2]
            toNode = data[3]
            packetType = data[4]
            packetSize = int(data[5])
            flag = data[6]
            flowId = data[7]
            srcAddress = data[8]
            desAddress = data[9]
            sequenceNumber = data[10]
            pktId = data[11]
            # tcp or ack
            if flowId == '2':
                if event == "r":
                    countReceive += 1
                    if toNode == "0":
                        # add the received data to a dictionary
                        receivedRecord.update({sequenceNumber: time})
                    totalReceive += packetSize
                    # get the last time receive data
                    end = time
                if event == "+":
                    countSent += 1
                    if fromNode == '0':
                        # add the sent data to a dictionary
                        sentRecord.update({sequenceNumber: time})
                        if begin == 0:
                            # get the time while first receive data
                            begin = time
        # add the received data into a list
        for data in sentRecord:
            if data in receivedRecord.keys():
                totalReceivePakcet.append(data)
        # calculate durations for all packets,
        for data in totalReceivePakcet:
            curDuration = receivedRecord.get(data) - sentRecord.get(data)
            duration += curDuration
        throughPutRate = throughPut(begin, end, totalReceive)
        dropRate = Drop(countSent, countReceive)
        latencyTime = latency(duration, len(totalReceivePakcet))
        return throughPutRate, dropRate, latencyTime


# run the tcl file, generate the trace file based on name and rate
def processTcl(tcpName, rate):
    for name in tcpName:
        os.system("/course/cs4700f12/ns-allinone-2.35/bin/ns " + "experiment1.tcl " + str(name) + " " + str(rate))


"""
initialize the program
does: 
1. generate tracy file
2. create output data file for us to plot the graph
3. parse data from the tracy file and write to the targeted output files.
"""


def starter():
    tcpNames = ["Tahoe", "Reno", "Newreno", "Vegas"]
    # increasing CBR flow rate from 1 to 15
    for rate in range(15):
        # create test files
        processTcl(tcpNames, rate)

    file1 = open("exp1_throughput.txt", "w+")
    file2 = open("exp1_dropRate.txt", "w+")
    file3 = open("exp1_latency.txt", "w+")
    # with open("experience1.throughput.txt", "w") as file1, open("experience1.dropRate.txt", "w") as file2, open(
    #         "experience1.latency.txt", "w") as file3:
    for rate in range(15):
        curThroughPut = ""
        curDropRate = ""
        curLatency = ""
        for name in tcpNames:
            curThroughPut = curThroughPut + '\t' + str(parseData(name, rate)[0])
            curDropRate = curDropRate + '\t' + str(parseData(name, rate)[1])
            curLatency = curLatency + '\t' + str(parseData(name, rate)[2])
        file1.write(str(rate) + curThroughPut + '\n')
        file2.write(str(rate) + curDropRate + '\n')
        file3.write(str(rate) + curLatency + '\n')


if __name__ == "__main__":
    starter()
