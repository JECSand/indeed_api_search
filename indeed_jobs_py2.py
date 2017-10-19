# Connor Sanders
# 10/9/2017
# Indeed API Job Search

import pip
import datetime
import codecs
import os
import sys


# Package installer
def install(package):
    pip.main(['install', package])

try:
    import urllib2
except:
    print('urllib2 package for Python not found, pip installing now....')
    install('urllib2')
    import urllib2
    print('urllib2 package has been successfully installed for Python\n Continuing Process...')

try:
    import xml.etree.ElementTree as ET
except:
    print('xml package for Python not found, pip installing now....')
    install('xml')
    import xml.etree.ElementTree as ET
    print('xml package has been successfully installed for Python\n Continuing Process...')


# Make apisearch call and return results
def api_call(e_type, start_ps, locations):
    publisherID = '2849821278263879'
    api_url = 'http://api.indeed.com/ads/apisearch?publisher=' + publisherID + '&format=xml&q=' + e_type + '&l=' + \
              locations + '%2C+tx&sort=&radius=&st=&jt=fulltime&start=' + str(start_ps) + '&limit=100&fromage=' \
              '&filter=&latlong=1&co=us&chnl=&userip=1.2.3.4&useragent=Mozilla/%2F4.0%28Firefox%29&v=2'
    data = urllib2.urlopen(api_url)
    results = data.read()
    return results


# Define indeed data extraction function with parameter extract type
def extract_job_listings(e_type, location):

    # Declare datetime tim stamp, and local dir and file variables
    dt = datetime.datetime.today()
    c_dir = os.getcwd()
    os_system = os.name
    if os_system == 'nt':
        csv_local_dir = c_dir + '\\job_results\\'
    else:
        csv_local_dir = c_dir + '/job_results/'
    created_file = e_type.replace('+', '_') + '_' + str(dt).replace(':', '-').replace(' ', '_').split('.')[0] + '.csv'
    o_file = codecs.open(csv_local_dir + created_file, 'w', 'utf-8')
    o_file.write('city,company,jobtitle,jobkey,description,url,expired\n')

    # Call API function with e_type filter and return XML data
    results = api_call(e_type, 0, location)
    root = ET.fromstring(results)

    # Pagination code block
    total_results = 0
    for child in root:
        if 'totalresults' in child.tag:
            total_results = int(child.text)

    # Iterate through individual job postings
    i = 0
    for r in root.findall("./results/result"):
        i += 1
        r_city = r.find('city').text.encode('utf-8').strip().replace(',', ' ')
        r_company = r.find('company').text.encode('utf-8').strip().replace(',', ' ')
        r_jobtitle = r.find('jobtitle').text.encode('utf-8').strip().replace(',', ' ')
        r_jobkey = r.find('jobkey').text.encode('utf-8').strip().replace(',', ' ')
        r_snipp = r.find('snippet').text.encode('utf-8').strip().replace(',', '|')
        r_expire = r.find('expired').text.encode('utf-8').strip().replace(',', ' ')
        r_url = r.find('url').text.encode('utf-8').strip().replace(',', ' ')
        if r_expire != 'True':
            data_row = r_city + ',' + r_company + ',' + r_jobtitle + ',' + r_jobkey + ',' + r_snipp + ',' + r_url + ','\
                       + r_expire + '\n'
            o_file.write(data_row.decode('utf-8'))
        else:
            continue

    # If more than 100 results returned per query, call and paginate through rest of results
    if total_results > i:
        while i < total_results:
            results2 = api_call(e_type, i, location)
            root2 = ET.fromstring(results2)
            for r2 in root2.findall("./results/result"):
                i += 1
                r_city = r2.find('city').text.encode('utf-8').strip().replace(',', ' ')
                r_company = r2.find('company').text.encode('utf-8').strip().replace(',', ' ')
                r_jobtitle = r2.find('jobtitle').text.encode('utf-8').strip().replace(',', ' ')
                r_jobkey = r2.find('jobkey').text.encode('utf-8').strip().replace(',', ' ')
                r_snipp = r2.find('snippet').text.encode('utf-8').strip().replace(',', '|')
                r_expire = r2.find('expired').text.encode('utf-8').strip().replace(',', ' ')
                r_url = r2.find('url').text.encode('utf-8').strip().replace(',', ' ')
                if r_expire != 'True':
                    data_row = r_city + ',' + r_company + ',' + r_jobtitle + ',' + r_jobkey + ',' + r_snipp + ',' + \
                               r_url + ',' + r_expire + '\n'
                    o_file.write(data_row.decode('utf-8'))
                else:
                    continue
    else:
        pass
    print(created_file + ' has been created!!')
    o_file.close()

if __name__ == "__main__":
    extract_job_listings(sys.argv[1], sys.argv[2])
