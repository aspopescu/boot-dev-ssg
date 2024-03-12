from textnode import *
from htmlnode import *
from copy_contents import *
from generate_pages import *


path_to_static = "./static/"
path_to_public = "./public/"
path_to_template_html = "./template.html"
path_to_content = "./content/"

def main():
    setup_public_dir(path_to_public)
    copy_contents(path_to_static, path_to_public)
    pages = generate_pages_recursive(path_to_content, path_to_template_html, path_to_public)
    for page in pages:
        create_file(page[1], "index.html", page[0])
main()

