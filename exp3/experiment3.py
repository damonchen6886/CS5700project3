import os


# traceFile attributes
#   event   time    formNode    toNode  pktType     pkeSize    flags   flowId   srcAddr     dstAddr    seqNum   pktId

# calculate throughput: return rate in kb
def throughPut(begin, end, dataSize):
    return float(dataSize * 8 / (end - begin) / 1024)


# def Drop(countSent, countReceive):
#     return float(1 - float(countReceive)/float(countSent))


# calculate latency
# return the latency in ms
def latency(duration, totalPacket):
    if totalPacket == 0:
        return 0
    else:
        return float(duration / totalPacket * 1000)


"""
process the data from trace file, calculate the throughput, dropRate, and latency.
return: a list of list of int, each inner list are the result of throughput and latency for cbr and tcp, respectively.
"""


def parseData(tcpName, queue):
    filename = "tcp_" + tcpName + "_" + queue + ".tr"
    with open(filename) as file:
        content = file.readlines()
        totalReceive1 = 0
        totalReceive2 = 0
        timeCount = 0
        sentRecord1 = {}
        receivedRecord1 = {}
        totalReceivePakcet1 = []
        sentRecord2 = {}
        receivedRecord2 = {}
        totalReceivePakcet2 = []
        duration1 = 0
        duration2 = 0
        throughPutRate1List = []
        throughPutRate2List = []
        latencyTime1List = []
        latencyTime2List = []
        sumPacket1 = 0
        sumPacket2 = 0

        for line in content:
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
                if event == "+":
                    if fromNode == '0':
                        sentRecord1.update({sequenceNumber: time})
                if event == "r":
                    totalReceive1 += packetSize
                    if toNode == "0":
                        receivedRecord1.update({sequenceNumber: time})
                    # calculate package received in every second

            # cbr
            if flowId == '0':
                if event == "+":
                    if fromNode == '4':
                        sentRecord2.update({sequenceNumber: time})
                if event == "r":
                    if toNode == "5":
                        totalReceive2 += packetSize
                        receivedRecord2.update({sequenceNumber: time})

            # add value to the result list
            # if the cur time is in 1 ms interval, delta in 0.01
            if 0 <= time - timeCount <= 0.01:
                # convert size to kb
                cur1 = totalReceive1 / 1024
                cur2 = totalReceive2 / 1024
                throughPutRate1List.append(cur1)
                throughPutRate2List.append(cur2)
                timeCount += 1
                # reset sum
                totalReceive1 = 0
                totalReceive2 = 0

                # tcp latency
                for data in sentRecord1:
                    if data in receivedRecord1.keys():
                        totalReceivePakcet1.append(data)

                for data in totalReceivePakcet1:
                    curDuration = receivedRecord1.get(data) - sentRecord1.get(data)
                    duration1 += curDuration
                    sumPacket1 += 1
                # cbr latency
                for data in sentRecord2:
                    if data in receivedRecord2.keys():
                        totalReceivePakcet2.append(data)

                for data in totalReceivePakcet2:
                    curDuration = receivedRecord2.get(data) - sentRecord2.get(data)
                    duration2 += curDuration
                    sumPacket2 += 2
                curLate1 = latency(duration1, sumPacket1)
                curLate2 = latency(duration2, sumPacket2)
                latencyTime1List.append(curLate1)
                latencyTime2List.append(curLate2)
        # print(throughPutRate1List)
        # print(throughPutRate2List)
        # print(latencyTime1List)
        # print(latencyTime2List)
        result = []
        result.append(throughPutRate1List)
        result.append(throughPutRate2List)
        result.append(latencyTime1List)
        result.append(latencyTime2List)
        return result


# run the tcl file, generate the trace file based on name and rate
def processTcl(tcpName, queue):
    for name in tcpName:
        for q in queue:
            os.system("/course/cs4700f12/ns-allinone-2.35/bin/ns " + "experiment3.tcl " + str(name) + " " + str(q))


"""
wwrite data to the destination  file.
"""


def processFile(tcpname, queue, data1, data2, data3, data4):
    file = open("exp3_" + tcpname + "_" + queue + "_" + "_output.txt", "w+")
    for i in range(len(data1)):
        if i == 0:
            file.write(
                "time" + "\t" + "TCPThroughPut" + "\t" + "cbrThroughPut" + "\t" + "TCPLatency" + "\t" + "cbrLatnecy" + "\n")

        file.write(str(i + 1) + "\t" + str(data1[i]) + "\t" + str(data2[i]) + "\t" + str(data3[i]) + "\t" + str(
            data4[i]) + "\n")


"""
initialize the program
does: 
1. generate tracy file
2. create output data file for us to plot the graph
3. parse data from the tracy file and write to the targeted output files.
"""


def starter():
    tcpNames = ["Reno", "Sack1"]
    queue = ["RED", "DropTail"]
    datatype = ["latency", "throughput"]

    # create test files
    processTcl(tcpNames, queue)
    for name in tcpNames:
        for q in queue:
            # list of list of data
            curdata = parseData(name, q)
            data1 = curdata[0]
            data2 = curdata[1]
            data3 = curdata[2]
            data4 = curdata[3]

            processFile(name, q, data1, data2, data3, data4)


if __name__ == "__main__":
    starter()
