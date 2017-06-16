# coding=utf8
import sys
import os.path
from xml.dom import minidom
from local_dependency import list_local_jars
from remote_jcenter_dependency import get_jcenter_versions
from remote_maven_center_dependency import get_mavenCenter_versions


# 爬取配置信息
def parse_repo_config(pro_path_param):
    local_maven_repo_func = []
    local_gradle_repo_func = []
    remote_maven_center_url_func = []
    remote_jcenter_url_func = []
    remote_maven_url_func = []
    if not os.path.exists(pro_path_param + '/config.xml'):
        print "---> The config file is missing!"
        exit(1)
    doc = minidom.parse(pro_path_param + "/config.xml")
    root = doc.documentElement
    if root.nodeName != 'repo':
        print "---> The root of the config file must be 'repo'"
        exit(1)
    # parse local configs
    local_repos = root.getElementsByTagName("local")
    if not local_repos:
        print "---> You should config the local repo path"
        exit(1)
    if len(local_repos) > 1:
        print "---> Only support for a single local repo tag"
        exit(1)
    local_repo = local_repos[0]
    local_sub_repos = local_repo.childNodes
    if not local_sub_repos or len(local_sub_repos) <= 0:
        print "---> Not found a local maven repo or a gradle repo"
        exit(1)
    for local_sub_repo in local_sub_repos:
        if local_sub_repo.nodeName == 'maven' or local_sub_repo.nodeName == 'gradle':
            if not local_sub_repo.childNodes \
                    or len(local_sub_repo.childNodes) <= 0:
                print "You should set the value in the tag 'maven'"
                exit(1)
            else:
                if local_sub_repo.nodeName == 'maven':
                    local_maven_repo_func.append(local_sub_repo.firstChild.data)
                elif local_sub_repo.nodeName == 'gradle':
                    local_gradle_repo_func.append(local_sub_repo.firstChild.data)
    # parse remote configs
    remote_repos = root.getElementsByTagName("remote")
    if remote_repos and len(remote_repos) == 1:
        remote_repo = remote_repos[0]
        remote_sub_repos = remote_repo.childNodes
        if remote_sub_repos and len(remote_sub_repos) > 0:
            for remote_sub_repo in remote_sub_repos:
                if remote_sub_repo.nodeName == 'url':
                    if not remote_sub_repo.childNodes \
                            or len(remote_sub_repo.childNodes) <= 0:
                        print "You should set the value in the tag 'url'"
                        exit(1)
                    else:
                        if remote_sub_repo.getAttribute('repo') == 'jcenter':
                            remote_jcenter_url_func.append(remote_sub_repo.firstChild.data)
                        elif remote_sub_repo.getAttribute('repo') == 'mavenCenter':
                            remote_maven_center_url_func.append(remote_sub_repo.firstChild.data)
                        elif remote_sub_repo.getAttribute('repo') == 'maven':
                            remote_maven_url_func.append(remote_sub_repo.firstChild.data)
    return local_maven_repo_func, \
           local_gradle_repo_func, \
           remote_jcenter_url_func, \
           remote_maven_center_url_func, \
           remote_maven_url_func


# 显示所有的缓存的jar信息
def show_local_jars(local_maven_repo_func, local_gradle_repo_func, jar_name):
    if not local_maven_repo_func or not local_gradle_repo_func or len(local_maven_repo_func) <= 0 or len(local_gradle_repo_func) <= 0:
        print '    Cannot find ' + jar_name + 'in local repository'
    print "\n===> All Results In Local Maven Repositories Are Listed Below"
    for maven_repo_func in local_maven_repo_func:
        print "---> List all result in " + maven_repo_func
        list_local_jars(maven_repo_func, jar_name, "maven")
    print "\n===> All Results In Local Gradle Repositories Are Listed Below"
    for gradle_repo_func in local_gradle_repo_func:
        print "---> List all result in " + gradle_repo_func
        list_local_jars(gradle_repo_func, jar_name, "gradle")


def show_remote_jars(jcenter_repo_urls, mavenCenter_repo_urls, maven_repo_urls, jar_name_param):
    print "\n===> All Results In Remote Repositories Are Listed Below"
    if jcenter_repo_urls:
        for jcenter_url in jcenter_repo_urls:
            print "--> List all result in " + jcenter_url
            get_jcenter_versions(jcenter_url, jar_name_param)
    if mavenCenter_repo_urls:
        for mavenCenter_url in mavenCenter_repo_urls:
            print "--> List all result in " + mavenCenter_url
            get_mavenCenter_versions(mavenCenter_url, jar_name_param)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "----> There is a serious error in the script!"
        exit(1)
    pro_path = sys.argv[1]
    action = sys.argv[2]
    jar_name = sys.argv[3]
    local_maven_repo, local_gradle_repo, remote_jcenter_repo, remote_mavenCenter_repo, remote_maven_repo \
        = parse_repo_config(pro_path)
    if action == 'local':
        show_local_jars(local_maven_repo, local_gradle_repo, jar_name)
    elif action == 'remote':
        show_remote_jars(remote_jcenter_repo, remote_mavenCenter_repo, remote_maven_repo, jar_name)