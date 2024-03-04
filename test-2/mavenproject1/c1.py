import requests
import json
import urllib3
from requests.auth import HTTPBasicAuth

# Disable SSL warnings
urllib3.disable_warnings()

def get_build_info(job_names, jenkins_urls, user, password):
    found_jobs = False
    for JOB_NAME in job_names:
        for JENKINS_URL in jenkins_urls:
            try:
                response = requests.get(f"{JENKINS_URL}/job/{JOB_NAME}/api/json?tree=builds[result,number]", auth=HTTPBasicAuth(user, password), verify=False)
                response.raise_for_status()
                data = response.json()
                builds = data.get('builds', [])
                successful_builds = len([build for build in builds if build['result'] == 'SUCCESS'])
                failed_builds = len([build for build in builds if build['result'] == 'FAILURE'])
                build_count = len(builds)

                if build_count > 0:
                    print(f"Total number of builds for job {JOB_NAME} at URL {JENKINS_URL}: {build_count}")
                    print(f"Number of successful builds for job {JOB_NAME} at URL {JENKINS_URL}: {successful_builds}")
                    print(f"Number of failed builds for job {JOB_NAME} at URL {JENKINS_URL}: {failed_builds}")
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
