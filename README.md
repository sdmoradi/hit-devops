# HIT DevOps Challenge

## Introduction

This is the sample project for the DevOps challenge. If you have reached this repo it means that you have passed the technical interview for the DevOps position in HIT (congratulations!l) and it's time for a challenge 🚀.

## Getting Started:

To complete the challenge you should complete the following steps:

1. Clone the project in a version control system of your choice

2. Create a CI/CD pipeline that does the following
    - Bumps the version in `version.txt`
        - If there are changes in `requirements.txt` you should bump the major version
        - If there are changes in the code you should bump the minor version
        - If there are changes in `README.md` you should bump the patch version
    - Create a container image with a tag equal to the version
    - Deploy it on a Kubernetes cluster

4. Change the code to print a log with the following format to STDOUT:
    
    ```json
    {
        "url": "hit.local/version",
        "time": "2022-01-01 14:22:33",
        "client_ip": "0.0.0.0",
        "service_name": "medusa"
    }
    ```

5. Deploy a log management service (e.g. Elasticsearch)

6. Redirect logs to the log management service

7. Deploy a GUI for the log management service and create a histogram for client IPs

## Build and Test

Execute the above-mentioned steps on your desired platform and make them ready for a code review session (demo).

## Rules

There are no rules for this challenge.

You are free to use any software, tool or procedure to complete the challenge.

Happy building 🏗️