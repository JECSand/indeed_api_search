# indeed_api_search

## Overview

A Simple Python Script to create a csv containing a list of job openings from indeed by location and type
Developed and Test with Python 2.7 and 3.5 on Linux Debian 9

## Features
Runs on Linux, Mac and Windows machines.
Runs on both Python 3.x and 2.x
The script is set up to automatically install all unmet prerequisite packages using pip

## How to Use
1. Make sure you have python 2 or 3 installed with pip on your machine
2. git copy the repository
```R
git clone https://github.com/JECSand/indeed_api_search.git
```
3. cd into the indeed_api_search directory
4. Enter the command in the following format:
```R
python indeed_jobs.py job city state_code
```
  or
```R
python3 indeed_jobs.py job city state_code
```
5. If job or location is a string with multiple words, enter in this format:
```R
python indeed_jobs.py "job+name" "city+name" state_code
```
* If script fails the first time due to permissions, try running as sudo to get the packages installed
6. extracted csv data will be located in the job_results folder

## Examples
```R
python3 indeed_jobs.py developer houston tx
python indeed_jobs.py "financial+analyst" "new+york" ny
```
