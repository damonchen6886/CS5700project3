import os


# traceFile attributes
#   event   time    formNode    toNode  pktType     pkeSize    flags   flowId   srcAddr     dstAddr    seqNum   pktId

# calculate throughput: return rate in kb
def throughPut(begin, end, dataSize):
    return float(dataSize * 8 / (end - begin) / 1024)


# calculate dropRate
# return a digit represents the drop rate
def Drop(countSent, countReceive):
    if countReceive == 0:
        return 0
    return float(1 - float(countReceive) / float(countSent))


# calculate latency
# return the latency in ms
def latency(duration, totalPacket):
    if totalPacket == 0:
        return 0
    else:
        return float(duration / totalPacket * 1000)


"""
process the data from trace file, calculate the throughput, dropRate, and latency.
return: the value of throughput, dropRate, and latency value for two tcp 
"""


def parseData(tcpName1, tcpname2, cbrRate):
    filename = "tcp_" + tcpName1 + "_" + tcpname2 + "_atRate" + str(cbrRate) + ".tr"
    with open(filename) as file:
        content = file.readlines()
        begin1 = 0
        begin2 = 0
        end1 = 15
        end2 = 15
        # n1 to n4
        totalReceive1 = 0
        sentRecord1 = {}
        receivedRecord1 = {}
        totalReceivePakcet1 = []
        duration1 = 0
        countReceive1 = 0
        countSent1 = 0
        # n5 to n6
        totalReceive2 = 0
        sentRecord2 = {}
        receivedRecord2 = {}
        totalReceivePakcet2 = []
        duration2 = 0
        countReceive2 = 0
        countSent2 = 0
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
            # tcp 1 (class id 2)
            if flowId == '2':
                if event == "r":
                    countReceive1 += 1
                    if toNode == "0":
                        receivedRecord1.update({sequenceNumber: time})
                    totalReceive1 += packetSize
                    # get the last time receive data
                    end1 = time
                if event == "+":
                    countSent1 += 1
                    if fromNode == '0':
                        sentRecord1.update({sequenceNumber: time})
                        if begin1 == 0:
                            # get the time while first receive data
                            begin1 = time
            # tcp 2 (class id 3)
            if flowId == '3':
                if event == "r":
                    countReceive2 += 1
                    if toNode == "4":
                        receivedRecord2.update({sequenceNumber: time})
                    totalReceive2 += packetSize
                    # get the last time receive data
                    end2 = time
                if event == "+":
                    countSent2 += 1
                    if fromNode == '4':
                        sentRecord2.update({sequenceNumber: time})
                        if begin2 == 0:
                            # get the time while first receive data
                            begin2 = time

        # n1 to n4
        # add the received data into a list
        for data in sentRecord1:
            if data in receivedRecord1.keys():
                totalReceivePakcet1.append(data)
        # calculate durations for all packets,
        for data in totalReceivePakcet1:
            curDuration1 = receivedRecord1.get(data) - sentRecord1.get(data)
            duration1 += curDuration1
        throughPutRate1 = throughPut(begin1, end1, totalReceive1)
        dropRate1 = Drop(countSent1, countReceive1)
        latencyTime1 = latency(duration1, len(totalReceivePakcet1))

        # n5 to n6
        # add the received data into a list
        for data in sentRecord2:
            if data in receivedRecord2.keys():
                totalReceivePakcet2.append(data)
        # print("sentRecord2  = " )
        # print( len(sentRecord2))
        # calculate durations for all packets,
        for data in totalReceivePakcet2:
            curDuration2 = receivedRecord2.get(data) - sentRecord2.get(data)
            duration2 += curDuration2
        throughPutRate2 = throughPut(begin2, end2, totalReceive2)
        dropRate2 = Drop(countSent2, countReceive2)
        latencyTime2 = latency(duration2, len(totalReceivePakcet2))

        return str(throughPutRate1) + '\t' + str(throughPutRate2), \
               str(dropRate1) + '\t' + str(dropRate2), \
               str(latencyTime1) + '\t' + str(latencyTime2)


# run the tcl file, generate the trace file based on name and rate
def processTcl(tcpName1, tcpName2, rate):
    for name1, name2 in zip(tcpName1, tcpName2):
        os.system("/course/cs4700f12/ns-allinone-2.35/bin/ns " + "experiment2.tcl " + str(name1) + " " + str(
            name2) + " " + str(rate))


"""
initialize the program
does: 
1. generate tracy file
2. create output data file for us to plot the graph
3. parse data from the tracy file and write to the targeted output files.
"""


def starter():
    tcpNames1 = ["Reno", "Newreno", "Vegas", "Newreno"]
    tcpNames2 = ["Reno", "Reno", "Vegas", "Vegas"]

    # increasing CBR flow rate from 1 to 15
    for rate in range(15):
        # create test files
        processTcl(tcpNames1, tcpNames2, rate)

    fileRR1 = open("exp2_Reno_Reno_throughput.txt", "w+")
    fileRR2 = open("exp2_Reno_Reno_dropRate.txt", "w+")
    fileRR3 = open("exp2_Reno_Reno_latency.txt", "w+")
    fileNR1 = open("exp2_NewReno_Reno_throughput.txt", "w+")
    fileNR2 = open("exp2_NewReno_Reno_dropRate.txt", "w+")
    fileNR3 = open("exp2_NewReno_Reno_latency.txt", "w+")
    fileVV1 = open("exp2_Vegas_Vegas_throughput.txt", "w+")
    fileVV2 = open("exp2_Vegas_Vegas_dropRate.txt", "w+")
    fileVV3 = open("exp2_Vegas_Vegas_latency.txt", "w+")
    fileNV1 = open("exp2_NewReno_Vegas_throughput.txt", "w+")
    fileNV2 = open("exp2_NewReno_Vegas_dropRate.txt", "w+")
    fileNV3 = open("exp2_NewReno_Vegas_latency.txt", "w+")

    for rate in range(15):
        count = 0
        # print(rate)
        for name1, name2 in zip(tcpNames1, tcpNames2):
            count += 1
            print(count)
            curThroughPut = '\t' + str(parseData(name1, name2, rate)[0])
            curDropRate = '\t' + str(parseData(name1, name2, rate)[1])
            curLatency = '\t' + str(parseData(name1, name2, rate)[2])
            print(curLatency)
            if count == 1:
                # print("proces reno reno")
                fileRR1.write(str(rate) + curThroughPut + '\n')
                fileRR2.write(str(rate) + curDropRate + '\n')
                fileRR3.write(str(rate) + curLatency + '\n')
            elif count == 2:
                # print("proces NewReno reno")
                fileNR1.write(str(rate) + curThroughPut + '\n')
                print(curLatency)
                fileNR2.write(str(rate) + curDropRate + '\n')
                fileNR3.write(str(rate) + curLatency + '\n')
            elif count == 3:
                # print("proces Vegas Vegas")
                fileVV1.write(str(rate) + curThroughPut + '\n')
                fileVV2.write(str(rate) + curDropRate + '\n')
                fileVV3.write(str(rate) + curLatency + '\n')
            elif count == 4:
                # print("proces newReno Vegas")
                fileNV1.write(str(rate) + curThroughPut + '\n')
                fileNV2.write(str(rate) + curDropRate + '\n')
                fileNV3.write(str(rate) + curLatency + '\n')


if __name__ == "__main__":
    starter()
