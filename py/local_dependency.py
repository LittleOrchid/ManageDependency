# coding=utf8
import os.path

coordinates = []
group_path = ''
artifact_dir = ''
version_dir = '*'
classifier_name = ''
extension_name = 'jar'
repo_base = ''
support_extensions = ['so', 'jar']


def check_valid_with_pre_suffix(dir_path, file_prefix, file_suffix):
    if not os.path.isdir(dir_path):
        return False
    candidate_files = os.listdir(dir_path)
    if not candidate_files:
        return False
    for candidate_file in candidate_files:
        candidate_file = os.path.join(dir_path, candidate_file)
        if candidate_file.startswith(file_prefix) and candidate_file.endswith(file_suffix):
            return True
    return False


def parse_jar_coordinate(jar_name, build_method):
    global coordinates
    global group_path
    global artifact_dir
    global version_dir
    global classifier_name
    global extension_name
    global repo_base

    coordinates = jar_name.split(':')
    coordinates_len = len(coordinates)
    if 0 < coordinates_len:
        group_name = coordinates[0]
        group_path = group_name
        if build_method.upper() == "MAVEN":
            group_path = group_name.replace('.', '/')
    if 1 < coordinates_len:
        artifact_dir = coordinates[1]
    if 2 < coordinates_len:
        version_dir = coordinates[2]
    if 3 < coordinates_len:
        classifier_name = coordinates[3]
    if 4 < coordinates_len:
        extension_name = coordinates[4]


def check_group_artifact():
    if not group_path or not artifact_dir:
        return False
    group_dir_path = os.path.join(repo_base, group_path)
    if not os.path.exists(group_dir_path):
        return False
    artifact_dir_path = os.path.join(group_dir_path, artifact_dir)
    if not os.path.exists(artifact_dir_path):
        return False
    return True


def check_version(build_method):
    group_dir_path = os.path.join(repo_base, group_path)
    artifact_dir_path = os.path.join(group_dir_path, artifact_dir)
    candidate_version_dirs = os.listdir(artifact_dir_path)
    if not len(candidate_version_dirs):
        return None
    result_versions = []
    for candidate_version in candidate_version_dirs:
        if version_dir == '*':
            result_versions.append(candidate_version)
        elif candidate_version == version_dir:
            result_versions.append(candidate_version)
            break
    if len(result_versions) == 0:
        return None

    for i in range(len(result_versions)-1, -1, -1):
        candidate_version = result_versions[i]
        jar_path = os.path.join(artifact_dir_path, candidate_version)
        if build_method.upper() == 'GRADLE':
            if os.path.isdir(jar_path):
                candidate_file_signs = os.listdir(jar_path)
            else:
                candidate_file_signs = []
        else:
            candidate_file_signs = ['']
        valid_file = False
        for candidate_file_sign in candidate_file_signs:
            c_jar_path = os.path.join(jar_path, candidate_file_sign)
            dir_path = c_jar_path
            c_jar_path = os.path.join(c_jar_path, artifact_dir)
            c_jar_path += '-' + candidate_version
            if len(coordinates) < 5:
                for file_suffix in support_extensions:
                    if valid_file:
                        continue
                    if check_valid_with_pre_suffix(dir_path, c_jar_path, file_suffix):
                        valid_file = True
            else:
                c_jar_path += '-' + coordinates[3] + '.' + coordinates[4]
                if os.path.exists(c_jar_path):
                    valid_file = True
        if not valid_file:
            result_versions.remove(candidate_version)
    if len(result_versions) > 0:
        return result_versions
    else:
        return None


def list_local_jars(repo_base_parm, jar_coordinate, method):
    global repo_base
    repo_base = repo_base_parm
    # 程序开始, 默认是maven库
    if not method:
        method = "maven"
    parse_jar_coordinate(jar_coordinate, method)
    chk_ga_result = check_group_artifact()
    chk_v_result = None
    if chk_ga_result:
        chk_v_result = check_version(method)

    if not chk_ga_result or not chk_v_result:
        print '    Cannot find ' + jar_coordinate + 'in local repository'
    else:
        print '    ', coordinates[0] + ': '
        print '    ', '    ', coordinates[1] + ': '
        for version in chk_v_result:
            print '    ', '    ', '    ', version
