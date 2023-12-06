#!/bin/bash

# List of namespaces
namespaces=("namespace1" "namespace2" "namespace3")

# Function to update the image for a deployment in a namespace
update_image() {
  namespace=$1
  deployment=$2
  new_image=$3

  echo "Updating image for deployment '$deployment' in namespace '$namespace' to '$new_image'"
  kubectl set image deployment/"$deployment" <container-name>="$new_image" --namespace="$namespace" --record
}

# Specify the new image
new_image="your-new-image:tag"

# Loop through each namespace
for namespace in "${namespaces[@]}"; do
  # List of deployments in the current namespace
  deployments=("deployment1" "deployment2" "deployment3")

  # Loop through each deployment in the current namespace
  for deployment in "${deployments[@]}"; do
    # Call the update_image function
    update_image "$namespace" "$deployment" "$new_image"
  done
done
