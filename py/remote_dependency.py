# -*- coding: utf-8 -*-

import sys
import os.path
import commands
from BeautifulSoup import BeautifulSoup

coordinates = []
group_path = ''
artifact_dir = ''
version_dir = '*'
classifier_name = ''
extension_name = 'jar'
repo_base_url = ''

def parse_all_versions_jcenter():
    curl_url = 'curl ' + repo_base_url + group_path + '/' + artifact_dir + '/'
    status, result = commands.getstatusoutput(curl_url)
    soup = BeautifulSoup(result)
    version_href_array = soup.findAll('a')
    if not version_href_array:
        return
    version_list=[]
    for version_a in version_href_array:
        if not version_a.attrs:
            continue
        for attr in version_a.attrs:
            if attr and len(attr) >= 2 and attr[0] == 'href' and attr[1].encode('utf-8').startswith(':') and attr[1].endswith('/'):
                version_list.append(attr[1].encode('utf-8').replace(':', ''))
    if version_list:
        print coordinates[0]
        print '\t', coordinates[1]
        for version in version_list:
            print '\t\t', version.replace('/', '')



def parse_specific_version():
    curl_url = 'curl ' + repo_base_url + group_path + '/' + artifact_dir + '/' + version_dir + '/'
    status, result = commands.getstatusoutput(curl_url)
    soup = BeautifulSoup(result)
    file_a_list = soup.findAll('a')
    if not file_a_list:
        return
    find_extension = False
    gav_files = []
    for file_a in file_a_list:
        if not file_a.attrs:
            continue
        for attr in file_a.attrs:
            if attr and len(attr) >= 2 and attr[0] == 'href':
                gav_files.append(attr[1].encode('utf-8').replace(':', ''))
                if attr[1].encode('utf-8').startswith(':') \
                        and attr[1].encode('utf-8').endswith(classifier_name+'.' + extension_name):
                    find_extension = True
    if find_extension:
        print coordinates[0], ':'
        print '\t', coordinates[1], ':'
        print '\t\t', version_dir.replace('/', ''), ':'
        for gav_file in gav_files:
            print '\t\t\t', gav_file


def parse_jar_coordinate_jcenter(jar_name):
    global coordinates
    global group_path
    global artifact_dir
    global version_dir
    global classifier_name
    global extension_name
    global repo_base_url

    coordinates = jar_name.split(':')
    coordinates_len = len(coordinates)
    if 0 < coordinates_len:
        group_name = coordinates[0]
        group_path = group_name.replace('.', '/')

    if 1 < coordinates_len:
        artifact_dir = coordinates[1]

    if 2 < coordinates_len:
        version_dir = coordinates[2]

    if 3 < coordinates_len:
        classifier_name = coordinates[3]

    if 4 < coordinates_len:
        extension_name = coordinates[4]

    if not group_path or not artifact_dir:
        return

    if version_dir == '*':
        parse_all_versions_jcenter()
    else:
        parse_specific_version()

repo_base = sys.argv[1]
repo_base_url = "http://jcenter.bintray.com/"
parse_jar_coordinate_jcenter(sys.argv[2])

