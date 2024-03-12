import os
from copy_contents import *
from textnode import *


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md = get_disk_contents(from_path)
    template = get_disk_contents(template_path)
    content = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    title_placeholder ="{{ Title }}"
    content_placeholder ="{{ Content }}"
    return template.replace(title_placeholder, title).replace(content_placeholder, content)
    
def get_disk_contents(path):
    if path is None or path == "":
        raise ValueError("Provided path is not valid")
    file = open(path)
    md = file.read()
    file.close()
    return md

def extract_title(markdown):
    lines = markdown.split("\n")
    title = ""
    for l in lines:
        if l.startswith("# "):
            title = l[2:]
            break
        else:
            raise Exception("h1 markdown not found")
    return title

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    pages_to_generate = source_to_destination_dirs(dir_path_content, dest_dir_path)
    contents_and_destinations = []
    for page_tuple in pages_to_generate:
        os.makedirs(page_tuple[0], exist_ok=True)
        page_content = generate_page(page_tuple[1], template_path, page_tuple[0])
        contents_and_destinations.append((page_tuple[0], page_content))
    return contents_and_destinations
    
