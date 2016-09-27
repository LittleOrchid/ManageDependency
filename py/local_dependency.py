import sys
import os.path

coordinates = []
group_path = ''
artifact_dir = ''
version_dir = '*'
classifier_name = ''
extension_name = 'jar'

repo_base = ''

def parse_jar_group_artifact(group_artifact_path):
    version_bundle = os.listdir(group_artifact_path)
    if not version_bundle:
        return

    result_version_dirs = []
    for candidate_version_dir in version_bundle:
        tmp_version_dir = os.path.join(group_artifact_path, candidate_version_dir)
        if os.path.isfile(tmp_version_dir):
            continue
        for tmp_file in os.listdir(tmp_version_dir):
            suffix_of_jar = '.' + extension_name
            if classifier_name:
                suffix_of_jar = '-' + classifier_name + '.' + extension_name
            if tmp_file.endswith(suffix_of_jar):
                result_version_dirs.append(candidate_version_dir)
                break

    if len(result_version_dirs) == 0:
        return
    elif version_dir == '*':
        return result_version_dirs
    elif version_dir in result_version_dirs:
        result_version_dirs = []
        result_version_dirs.append(version_dir)
        return result_version_dirs
    else:
        return


def parse_jar_coordinate(jar_name):
    global coordinates
    global group_path
    global artifact_dir
    global version_dir
    global classifier_name
    global extension_name

    repo_base = '/Users/RexNJC/.m2/repository/'

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

    group_dir_path = os.path.join(repo_base, group_path)
    candidate_artifacts = os.listdir(group_dir_path)
    if not candidate_artifacts:
        return

    result_artifact_version_dirs = {}
    for candidate_artifact in candidate_artifacts:
        if candidate_artifact.startswith(artifact_dir):
            group_artifact_path = os.path.join(repo_base, group_path, candidate_artifact)
            result_version_dirs = parse_jar_group_artifact(group_artifact_path)
            if result_version_dirs:
                result_artifact_version_dirs.setdefault(candidate_artifact, result_version_dirs)

    return result_artifact_version_dirs


repo_base = sys.argv[1]
result_versions = parse_jar_coordinate(sys.argv[2])
if not result_versions:
    print '!!!Filed to find specific jars in ', repo_base, '!!!'
else:
    print coordinates[0] + ' : '
    for artifact in result_versions.keys():
        print '\t', artifact, ' : '
        versions = result_versions.get(artifact)
        for version in versions:
            print '\t', '\t', version
