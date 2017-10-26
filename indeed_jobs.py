# Connor Sanders
# 10/9/2017
# Indeed API Job Search
# MIT License

import pip
import datetime
import codecs
import os
import sys


# Missing Package installer
def install(package):
    print(str(package) + ' package for Python not found, pip installing now....')
    pip.main(['install', package])
    print(str(package) + ' package has been successfully installed for Python\n Continuing Process...')

# Install urllib or urllib2 depending on version of python
if sys.version_info > (3, 0):
    try:
        import urllib.request as urllib
    except:
        install('urllib')
        import urllib.request as urllib
else:
    try:
        import urllib2 as urllib
    except:
        install('urllib2')
        import urllib2 as urllib

# Check for xml package and install if missing
try:
    import xml.etree.ElementTree as ET
except:
    install('xml')
    import xml.etree.ElementTree as ET

# Declare datetime tim stamp, and local dir and file variables
dt = datetime.datetime.today()
c_dir = os.getcwd()
os_system = os.name
if os_system == 'nt':
    csv_local_dir = c_dir + '\\job_results\\'
else:
    csv_local_dir = c_dir + '/job_results/'


# Function to make apisearch call and return results
def api_call(e_type, start_ps, locations, st):
    publisherID = '2849821278263879'
    api_url = 'http://api.indeed.com/ads/apisearch?publisher=' + publisherID + '&format=xml&q=' + e_type + '&l=' + \
              locations + '%2C+' + st + '&sort=&radius=&st=&jt=fulltime&start=' + str(start_ps) + \
              '&limit=100&fromage=&filter=&latlong=1&co=us&chnl=&userip=1.2.3.4&useragent=Mozilla/%2F4.0%28Firefox%29&v=2'
    data = urllib.urlopen(api_url)
    results = data.read()
    return results


# Function for python 2 data manipulation
def indeed_process_py2(r, i, o_file):
    i += 1
    none_str = lambda d: d or ""
    r_city = none_str(r.find('city').text).encode('utf-8').strip().replace(',', ' ')
    r_company = none_str(r.find('company').text).encode('utf-8').strip().replace(',', ' ')
    r_jobtitle = none_str(r.find('jobtitle').text).encode('utf-8').strip().replace(',', ' ')
    r_jobkey = none_str(r.find('jobkey').text).encode('utf-8').strip().replace(',', ' ')
    r_snipp = none_str(r.find('snippet').text).encode('utf-8').strip().replace(',', '|')
    r_expire = none_str(r.find('expired').text).encode('utf-8').strip().replace(',', ' ')
    r_url = none_str(r.find('url').text).encode('utf-8').strip().replace(',', ' ')
    if r_expire != 'True':
        data_row = r_city + ',' + r_company + ',' + r_jobtitle + ',' + r_jobkey + ',' + r_snipp + ',' + r_url + \
                    ','  + r_expire + '\n'
        o_file.write(data_row.decode('utf-8'))
    return i


# Function for python 3 data manipulation
def indeed_process_py3(r, i, o_file):
    i += 1
    r_city = str(r.find('city').text).replace(',', ' ')
    r_company = str(r.find('company').text).replace(',', ' ')
    r_jobtitle = str(r.find('jobtitle').text).replace(',', ' ')
    r_jobkey = str(r.find('jobkey').text).replace(',', ' ')
    r_snipp = str(r.find('snippet').text).replace(',', '|')
    r_expire = str(r.find('expired').text).replace(',', ' ')
    r_url = str(r.find('url').text).replace(',', ' ')
    if r_expire != 'True':
        data_row = r_city + ',' + r_company + ',' + r_jobtitle + ',' + r_jobkey + ',' + r_snipp + ',' + r_url + ',' \
                   + r_expire + '\n'
        o_file.write(data_row)
    return i


# Function to determine whether to use python 2 or 3 process
def process_handler(r, i, o_file):
    if sys.version_info > (3, 0):
        i = indeed_process_py3(r, i, o_file)
    else:
        i = indeed_process_py2(r, i, o_file)
    return i


# Define indeed data extraction function with parameter extract type
def extract_job_listings(e_type, location, st):
    created_file = e_type.replace('+', '_') + '_' + str(dt).replace(':', '-').replace(' ', '_').split('.')[0] + '.csv'
    o_file = codecs.open(csv_local_dir + created_file, 'w', 'utf-8')
    o_file.write('city,company,jobtitle,jobkey,description,url,expired\n')
    results = api_call(e_type, 0, location, st)
    root = ET.fromstring(results)

    # Pagination code block
    total_results = 0
    for child in root:
        if 'totalresults' in child.tag:
            total_results = int(child.text)

    # Iterate through individual job postings
    i = 0
    for r in root.findall("./results/result"):
        i = process_handler(r, i, o_file)

    # If more than 100 results returned per query, call and paginate through rest of results
    if total_results > i:
        while i < total_results:
            results2 = api_call(e_type, i, location, st)
            root2 = ET.fromstring(results2)
            for r2 in root2.findall("./results/result"):
                i = process_handler(r2, i, o_file)
    else:
        pass
    print(created_file + ' has been created!!')
    o_file.close()


if __name__ == "__main__":
    extract_job_listings(sys.argv[1].lower(), sys.argv[2].lower(), sys.argv[3].lower())
