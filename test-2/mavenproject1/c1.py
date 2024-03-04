import requests
import json
import urllib3
from requests.auth import HTTPBasicAuth

# Disable SSL warnings
urllib3.disable_warnings()

def get_build_info(job_names, jenkins_urls, user, password):
    for JOB_NAME in job_names:
        found_job = False
        for JENKINS_URL in jenkins_urls:
            response = requests.get(f"{JENKINS_URL}/job/{JOB_NAME}/api/json?tree=builds[result,number]", auth=HTTPBasicAuth(user, password), verify=False)
            data = response.json()
            builds = data.get('builds', [])
            successful_builds = len([build for build in builds if build['result'] == 'SUCCESS'])
            failed_builds = len([build for build in builds if build['result'] == 'FAILURE'])
            build_count = len(builds)

            if build_count > 0:
                print(f"Total number of builds for job {JOB_NAME} at URL {JENKINS_URL}: {build_count}")
                print(f"Number of successful builds for job {JOB_NAME} at URL {JENKINS_URL}: {successful_builds}")
                print(f"Number of failed builds for job {JOB_NAME} at URL {JENKINS_URL}: {failed_builds}")
                found_job = True
                break

        if not found_job:
            print(f"Job {JOB_NAME} not found in any of the URLs.")

# Usage example
JOB_NAMES = ["jen_rest", "copy_job", "key_test"]
JENKINS_URLS = ["http://127.0.0.1:8080", "http://localhost:8080/job/test_01"]
user = "nik"
password = "iis123"

get_build_info(JOB_NAMES, JENKINS_URLS, user, password)
