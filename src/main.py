from textnode import *
from htmlnode import *
from copy_contents import *

path_to_static = "../static/"
path_to_public = "../public/"

def main():
    setup_public_dir(path_to_public)
    copy_contents(path_to_static, path_to_public)
main()

