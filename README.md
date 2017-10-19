# indeed_api_search

## Overview

A Simple Python Script to create a csv containing a list of job openings from indeed by location and type

## Features
Runs on Linux, Mac and Windows machines.
The script is set up to automatically install all unmet prerequisite packages using pip

## How to Use
1. Make sure you have python 2 or 3 installed with pip on your machine
2. git copy the repository
'''
git clone https://github.com/JECSand/indeed_api_search.git
'''
3. cd into the indeed_api_search directory
4. Enter the command in the following format:
'''
python indeed_jobs_py2.py job city
'''
or
'''
python3 indeed_jobs_py3.py job city
'''
5. If job or location is a string with multiple words, enter in this format:
'''
python indeed_jobs_py2.py "job+name" "city+name"
'''
6. extracted csv data will be located in the job_results folder
