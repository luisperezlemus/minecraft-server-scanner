#!/bin/bash

if ["$#" -ne 2 ]; then
    echo "Usage: $0 <IP_RANGE> <PORTS>"
    echo "Example: $0 101.0.0.0-102.0.0.0 80,443"
    exit 1
fi

IP_RANGE="$1"
PORTS="$2"
RATE="1000"

# Extract the start and end IPs from the provided range
START_IP=$(echo $IP_RANGE | cut -d'-' -f1)
END_IP=$(echo $IP_RANGE | cut -d'-' -f2)


# calculate nth IP address given base IP and offset


ip_to_int() {
    local ip=$1
    local a b c d
    IFS=. read -r a b c d <<< "$ip"
    echo "$(( (a << 24) + (b << 16) + (c << 8) + d ))"
}

int_to_ip() {
    local int=$1
    echo "$(( (int >> 24) & 0xFF )).$(( (int >> 16) & 0xFF )).$(( (int >> 8) & 0xFF )).$(( int & 0xFF ))"
}


# Function to extract IPs in batches and run the masscan
scan_in_batches() {
    local ip_start=$1
    local ip_end=$2
    local batch_size=$3

    local start_ip_num=$(ip_to_int $ip_start)
    local end_ip_num=$(ip_to_int $ip_end)
    local batch_end_num=$(( start_ip_num + batch_size - 1 ))

    while true; do
        # If the end IP of the batch exceeds the actual end IP, adjust it
        if [ "$batch_end_num" -ge "$end_ip_num" ]; then
            batch_end_num=$end_ip_num
        fi

        start_ip=$(int_to_ip $start_ip_num)
        end_ip=$(int_to_ip $batch_end_num)

        echo "Scanning from $start_ip to $end_ip"
        mkdir -p batch_scan/$START_IP-$END_IP
        sudo masscan $start_ip-$end_ip -p$PORTS --rate $RATE --excludefile exclude.conf -oL batch_scan/$START_IP-$END_IP/scan-$start_ip-$end_ip.txt

        # Check if we have reached or exceeded the end of the range
        if [ "$start_ip_num" -ge "$end_ip_num" ]; then
            break
        fi

        # Move to the next batch
        start_ip_num=$((batch_end_num + 1))
        batch_end_num=$((start_ip_num + batch_size - 1))
    done
}



scan_in_batches $START_IP $END_IP 500000