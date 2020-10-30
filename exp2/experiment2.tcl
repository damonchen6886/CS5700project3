# Create a Simulator object
set ns [new Simulator]

# Set tcpvariant in first argument
set tcp_variant1 [lindex $argv 0]
# Set tcpvariant in first argument
set tcp_variant2 [lindex $argv 1]
# CBR/UDP rate in second argument
set rate [lindex $argv 2]

# Open the trace file
set tf [open tcp_${tcp_variant1}_${tcp_variant2}_atRate${rate}.tr w]
$ns trace-all $tf

# Define a 'finish' procedure
proc finish {} {
	global ns tf
	$ns flush-trace
	#Close the Trace file
	close $tf
	exit 0
}

# create six nodes
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]
set n6 [$ns node]

#create links between the nodes
#Set bandwidth to 10 Mbps
$ns duplex-link $n1 $n2 10Mb 10ms DropTail
$ns duplex-link $n5 $n2 10Mb 10ms DropTail
$ns duplex-link $n2 $n3 10Mb 10ms DropTail
$ns duplex-link $n4 $n3 10Mb 10ms DropTail
$ns duplex-link $n6 $n3 10Mb 10ms DropTail

#Set Queue Size of link (n2-n3) to 10
$ns queue-limit $n2 $n3 10


#Setup a UDP connection
set udp [new Agent/UDP]
$ns attach-agent $n2 $udp
set null [new Agent/Null]
$ns attach-agent $n3 $null
$ns connect $udp $null

#Setup a CBR over UDP connection
set cbr [new Application/Traffic/CBR]
$cbr attach-agent $udp
$cbr set type_ CBR
#$cbr set packet_size_ 1000
$cbr set rate_ ${rate}mb


#Setup a TCP1 connection
if {$tcp_variant1 ne "Tahoe"} {
    set tcp [new Agent/TCP/${tcp_variant1}]
} else {
    # set tcp to Tahoe
    set tcp [new Agent/TCP]
}

# N1 to N4
# set the tcp flow id to 2
$tcp set fid_ 2
$tcp set class_ 2
$ns attach-agent $n1 $tcp
set sink [new Agent/TCPSink]
$ns attach-agent $n4 $sink
$ns connect $tcp $sink
$tcp set window_ 100

#Setup TCP2 connection
if {$tcp_variant2 ne "Tahoe"} {
    set tcp2 [new Agent/TCP/${tcp_variant2}]
} else {
    # set tcp2 to Tahoe
    set tcp2 [new Agent/TCP]
}
# N5  to N6
# set the tcp flow id to 3
$tcp2 set fid_ 3
$tcp2 set class_ 3
$ns attach-agent $n5 $tcp2
set sink2 [new Agent/TCPSink]
$ns attach-agent $n6 $sink2
$ns connect $tcp2 $sink2
$tcp2 set window_ 100


#setup a FTP Application
set ftp [new Application/FTP]
$ftp attach-agent $tcp

#setup a FTP Application
set ftp2 [new Application/FTP]
$ftp2 attach-agent $tcp2

#Schedule events for the CBR and FTP agents
$ns at 0.0 "$cbr start"
$ns at 0.0 "$ftp start"
$ns at 0.0 "$ftp2 start"
$ns at 15.0 "$ftp stop"
$ns at 15.0 "$ftp2 stop"
$ns at 15.0 "$cbr stop"

#Call the finish procedure after 15 seconds of simulation time
$ns at 15.0 "finish"

#Run the simulation
$ns run