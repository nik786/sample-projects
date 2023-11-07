#!/bin/bash

# Input YAML file
input_file="test.yml"

p1=`yq eval '.eurekazuul.serviceClientVersionMap.debitcardsetup-iapi.clientVersionRules' test.yml`

echo "printing data before addition: $p1"



# New data to add under clientVersionRules
new_data="        sysTIAGGDHGSDK:
          defaultMajorMinorVersion: 1.3-1.11
          versionRules:
            1:
              defaultMinorVersion: 3-1.13"

# Use yq to add the new data
yq eval '.eurekazuul.serviceClientVersionMap.debitcardsetup-iapi.clientVersionRules += {"sysTIAGGDHGSDK": {"defaultMajorMinorVersion": "1.3-1.11", "versionRules": {"1": {"defaultMinorVersion": "3-1.13"}}}}' "$input_file" > "$input_file.tmp"

# Replace the original file with the updated one
mv "$input_file.tmp" "$input_file"

echo "New data added under clientVersionRules in $input_file."

p2=`yq eval '.eurekazuul.serviceClientVersionMap.debitcardsetup-iapi.clientVersionRules' test.yml`

echo "printing data after addition: $p2"
