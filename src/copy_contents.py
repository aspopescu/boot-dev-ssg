import os
import shutil


def setup_public_dir(destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
        os.mkdir(destination)
    else:
        os.mkdir(destination)

def copy_contents(source, destination):
    if not os.path.exists(source):
        raise Exception("static dir not found, process blocked")
    copy_list = source_to_destination_dirs(source, destination)
    for cl in copy_list:
        os.makedirs(cl[0], exist_ok=True)
        shutil.copy(cl[1], cl[0])
    return

def contents(path):
    path_contents = os.listdir(path)
    files = []
    for c in path_contents:
        c_path = os.path.join(path, c)
        if os.path.isfile(c_path):
            files.append((path, c_path))
            continue
        files.extend(contents(c_path))
    return files

def source_to_destination_dirs(source, destination):
    paths_tuples_list = contents(source)
    destination_dirs = []
    for ptl in paths_tuples_list:
        destination_dir = ptl[0].replace(source, destination)
        destination_dirs.append((destination_dir, ptl[1]))
    return destination_dirs

def create_file(contents, file_name, destination):
    path = os.path.join(destination, file_name)
    file = open(path, mode="w")
    file.write(contents)
    file.close()
    return

