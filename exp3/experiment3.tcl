# Create a Simulator object
set ns [new Simulator]

# Set tcpvariant in first argument
set tcp_variant [lindex $argv 0]
# Set queue or red in second argument
set queue_Red [lindex $argv 1]


# Open the trace file
set tf [open tcp_${tcp_variant}_${queue_Red}.tr w]
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
if {$queue_Red eq "RED"} {
    $ns duplex-link $n1 $n2 10Mb 10ms RED
    $ns duplex-link $n5 $n2 10Mb 10ms RED
    $ns duplex-link $n2 $n3 10Mb 10ms RED
    $ns duplex-link $n4 $n3 10Mb 10ms RED
    $ns duplex-link $n6 $n3 10Mb 10ms RED
} else {
    $ns duplex-link $n1 $n2 10Mb 10ms DropTail
    $ns duplex-link $n5 $n2 10Mb 10ms DropTail
    $ns duplex-link $n2 $n3 10Mb 10ms DropTail
    $ns duplex-link $n4 $n3 10Mb 10ms DropTail
    $ns duplex-link $n6 $n3 10Mb 10ms DropTail
}
#Set Queue Size of link to 20
$ns queue-limit $n1 $n2 20
$ns queue-limit $n5 $n2 20
$ns queue-limit $n2 $n3 20
$ns queue-limit $n4 $n3 20
$ns queue-limit $n6 $n3 20



#Setup a UDP connection (n5 -n6)
set udp [new Agent/UDP]
$ns attach-agent $n5 $udp
set null [new Agent/Null]
$ns attach-agent $n6 $null
$ns connect $udp $null

#Setup a CBR over UDP connection
set cbr [new Application/Traffic/CBR]
$cbr attach-agent $udp
$cbr set type_ CBR
#$cbr set packet_size_ 1000
$cbr set rate_ 5mb


#Setup a TCP1 connection
set tcp [new Agent/TCP/${tcp_variant}]
set sink [new Agent/TCPSink]


# set the tcp flow id to 2
$tcp set fid_ 2
$tcp set class_ 2
$ns attach-agent $n1 $tcp
$ns attach-agent $n4 $sink
$ns connect $tcp $sink
#$tcp set window_ 100



#setup a FTP Application
set ftp [new Application/FTP]
$ftp attach-agent $tcp



#Schedule events for the CBR and FTP agents

$ns at 0.0 "$ftp start"
$ns at 2.0 "$cbr start"
$ns at 15.0 "$ftp stop"
$ns at 15.0 "$cbr stop"

#Call the finish procedure after 15 seconds of simulation time
$ns at 15.0 "finish"

#Run the simulation
$ns run