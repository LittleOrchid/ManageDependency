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

def download_specific_version():
    curl_url = 'curl ' + repo_base_url + group_path + '/' + artifact_dir + '/' + version_dir + '/'
    status, result = commands.getstatusoutput(curl_url)
    soup = BeautifulSoup(result)
    file_a_list = soup.findAll('a')
    if not file_a_list:
        return
    if classifier_name:
        object_file = coordinates[1] + '-' + coordinates[2] + '-' + classifier_name + '.' + extension_name
    else:
        object_file = coordinates[1] + '-' + coordinates[2] + '.' + extension_name

    find_result = ''
    for file_a in file_a_list:
        if not file_a.attrs:
            continue
        for attr in file_a.attrs:
            if attr and len(attr) >= 2 and attr[0] == 'href' and attr[1].encode('utf-8').startswith(':'):
                if attr[1].encode('utf-8').replace(':', '') == object_file:
                    find_result = attr[1].encode('utf-8')

    if not find_result:
        print 'Sorry! Cannot find ' + coordinates + 'in ' + repo_base
    else:
        curl_url = 'curl ' + repo_base_url + group_path + '/' + artifact_dir + '/' + version_dir + '/' + find_result \
                   + '> ./cache/' + object_file
        status, result = commands.getstatusoutput(curl_url)
        if status != 0:
            print 'Sorry! Some errors occur while downloading ' + object_file
        else:
            mvn_url = 'mvn install:install-file  -Dfile=' + './cache/' + object_file \
                      + ' -DgroupId=' + coordinates[0] + ' -DartifactId=' + coordinates[1] + ' -Dversion=' + coordinates[2]
            if classifier_name:
                mvn_url = mvn_url + ' -Dclassifier' + classifier_name
            if extension_name:
                mvn_url = mvn_url + ' -Dpackaging=' + extension_name
            status, result = commands.getstatusoutput(mvn_url)
            if status != 0:
                print 'Sorry! Some errors occur in running mvn-install command'
            else:
                print 'Congratulation! Download the specific archive successfully'


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

    if not group_path or not artifact_dir or not version_dir:
        print "The specific file must have groupId, artifactId and version"
        return

    download_specific_version()

repo_base = sys.argv[1]
repo_base_url = "http://jcenter.bintray.com/"
parse_jar_coordinate_jcenter(sys.argv[2])


