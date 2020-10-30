
The object of this project is to study and understand the TCP features and behavior of the TCP variants under load conditions and queuing algorithm.

In each experiment, we use NS-2 network simulator to perform experiments for different TCP variant(Tahoe, Reno, NewReno, Vegas nad SACK) and use metrics such as latency, dropout rate, as well as throughput to analyse the performance and behaviour of each TCP variant


Topology: 
                         N1                      N4
                           \                    /
                            \                  /
                             N2--------------N3
                            /                  \
                           /                    \
                         N5                      N6



process of experiment:
We first build the topology above and set various conditions in NS-2 simulator, and then use python script to run the tcl file and generated trace file which contains raw data, python script will also parse the data and generate the output data set. We plot the data set and interpret the graph accordingly.    


Run: 
Go to the experiment folder, run python experiment{}.py, it will generate result data set of latency, dropout and throughput for different tcp variant  

experiment details:
https://david.choffnes.com/classes/cs4700fa20/project3.php


Result:
Please refer to the paper for detailed interpretation of result.