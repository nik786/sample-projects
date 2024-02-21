import requests
import argparse
import json

requests.packages.urllib3.disable_warnings()

# Define namespaces, URLs, and URL templates
namespaces = ["kube-system", 
              "blue"]
urls = ["https://192.168.56.70:6443", 
        "https://192.168.56.71:6443"]
url_templates = ["%s/api/v1/namespaces/%s/pods/%s"]

def fetch_data_from_urls(namespaces, urls, pod_name):
    cert = ("/etc/kubernetes/pki/user/k8s-admin.crt", "/etc/kubernetes/pki/user/k8s-admin.key")
    cacert = "/etc/kubernetes/pki/user/k8s-admin.crt"

    for namespace in namespaces:
        for url in urls:
            for url_template in url_templates:
                full_url = url_template % (url, namespace, pod_name)
                try:
                    response = requests.get(full_url, cert=cert, verify=False)
                    response.raise_for_status()  # Raise an exception for HTTP errors

                    data = response.json()
                    name = data.get("metadata", {}).get("name", "N/A")
                    status = data.get("status", {}).get("phase", "N/A")

                    print(f"Pod found in namespace '{namespace}' at cluster '{url}':")
                    print(f"NAME: {name}")
                    print(f"STATUS: {status}")

                    print("\n")
                    # Return after finding the pod to avoid unnecessary iterations
                    return
                except requests.exceptions.RequestException as e:
                    print(f"An error occurred while fetching data from {full_url}: {e}")
                    print("\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch data from Kubernetes API URLs")
    parser.add_argument("-p", required=True, help="Pod Name")
    args = parser.parse_args()

    fetch_data_from_urls(namespaces, urls, args.p)

