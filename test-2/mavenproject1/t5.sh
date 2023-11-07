#!/bin/bash

# Input YAML file
input_file="test.yml"

# Service name
service_name="debitcardsetup-iapi"

# New data to add under clientVersionRules
new_data="      sysTIAGGDHGSDK:
        defaultMajorMinorVersion: 1.3-1.11
        versionRules:
          1:
            defaultMinorVersion: 3-1.13"

# Use awk to add the new data
awk -v new_data="$new_data" -v srv_name="$service_name" '
  # Set the flag when we find the service name
  $1 == srv_name ":" { found = 1 }

  # Print the current line
  { print }

  # When we find "clientVersionRules:" and the service name, add the new data
  found && $0 ~ /^    clientVersionRules:/ {
    print new_data
    found = 0
  }
' "$input_file" > "$input_file.tmp"

# Replace the original file with the updated one
mv "$input_file.tmp" "$input_file"

echo "New data added under clientVersionRules in $input_file."
