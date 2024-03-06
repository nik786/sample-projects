import requests
import json
import urllib3
import csv
import subprocess
from requests.auth import HTTPBasicAuth
import sys, os

# Disable SSL warnings
urllib3.disable_warnings()
user = os.environ['USER']
password = os.environ['PASS']


def get_build_info(job_names, jenkins_urls, user, password):
    found_jobs = False
    with open('build_info.csv', mode='w', newline='') as csv_file, open('line.txt', mode='w') as line_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['JOB-NAME', 'SUCCESSFUL-BUILDS', 'FAILED-BUILDS', 'TOTAL-BUILDS'])

        for JOB_NAME in job_names:
            for JENKINS_URL in jenkins_urls:
                try:
                    # Fetching total build count using curl command
                    curl_command = f'curl -ks --user "{user}:{password}" "{JENKINS_URL}/job/{JOB_NAME}/api/json?tree=builds[result,number]" | jq -r \'.builds | length\''
                    total_build_count = int(subprocess.check_output(curl_command, shell=True).decode().strip())

                    # Fetching other build information using requests
                    response = requests.get(f"{JENKINS_URL}/job/{JOB_NAME}/api/json?tree=builds[result,number]", auth=HTTPBasicAuth(user, password), verify=False)
                    response.raise_for_status()
                    data = response.json()
                    builds = data.get('builds', [])
                    successful_builds = len([build for build in builds if build['result'] == 'SUCCESS'])
                    failed_builds = len([build for build in builds if build['result'] == 'FAILURE'])

                    # Writing to CSV and HTML files
                    csv_writer.writerow([JOB_NAME, successful_builds, failed_builds, total_build_count])
                    line_file.write(f"<tr><td>{JOB_NAME}</td><td>{successful_builds}</td><td>{failed_builds}</td><td>{total_build_count}</td></tr>\n")
                    print(f"Total number of builds for job {JOB_NAME} at URL {JENKINS_URL}: {total_build_count}")
                    print(f"Number of successful builds for job {JOB_NAME}: {successful_builds}")
                    print(f"Number of failed builds for job {JOB_NAME}: {failed_builds}")
                    found_jobs = True
                except Exception as e:
                    print(f"An error occurred while fetching job {JOB_NAME} at URL {JENKINS_URL}: {str(e)}")

    if not found_jobs:
        raise Exception("None of the jobs found on any of the URLs.")

# Usage example
JOB_NAMES = ["jen_rest", "copy_job", "key_test"]
JENKINS_URLS = ["http://127.0.0.1:8080", "http://localhost:8080/job/test_01"]
user = "nik"
password = "iis123"

get_build_info(JOB_NAMES, JENKINS_URLS, user, password)
