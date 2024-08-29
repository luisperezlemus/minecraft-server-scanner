#!/bin/bash

# Check if the country code argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <text file with ranges>"
  exit 1
fi

# Set the country code and the corresponding file name
# TODO: revert to this while also making it possible to test the major_isps.txt file
# COUNTRY_CODE=$1
# FILE_NAME="ip-addresses-${COUNTRY_CODE}.txt" removed this to test the major_isps.txt file, 
FILE_NAME="$1"

# Check if the file exists
if [ ! -f "$FILE_NAME" ]; then
    # Extract the directory name from the file name
    DIRECTORY=$(dirname "$FILE_NAME")
    
    # Check if the directory exists
    if [ ! -d "$DIRECTORY" ]; then
        echo "Directory $DIRECTORY not found!"
        exit 1
    fi
    
    echo "File $FILE_NAME not found in directory $DIRECTORY!"
    exit 1
fi

# Read the file line by line
while IFS= read -r IP_RANGE || [ -n "$IP_RANGE" ]; do
  # Execute the other bash script with the current IP range
  ./run_scanner.sh "$IP_RANGE" "25565,19132" "3000" "1000000"
  
  # Check if the script executed successfully
  if [ $? -eq 0 ]; then
    # Remove the processed IP range from the file
    sed -i.bak "/^${IP_RANGE}$/d" "$FILE_NAME"
  else
    echo "Failed to process IP range: $IP_RANGE"
    exit 1
  fi
done < "$FILE_NAME"

echo "All IP ranges processed successfully."