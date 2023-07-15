import os


def make_dir(dir_string):
    if not os.path.exists(dir_string):
        os.mkdir(dir_string)


def clean_dir(dir_string):
    old_file_list = os.listdir(dir_string)

    for old_file in old_file_list:
        remove_dir = os.path.join(dir_string, old_file)
        if os.path.exists(remove_dir) and not os.path.isdir(remove_dir):
            os.remove(remove_dir)

def make_or_clean_dir(dir_string):
    make_dir(dir_string)
    clean_dir(dir_string)