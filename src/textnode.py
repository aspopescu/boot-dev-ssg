from htmlnode import *
import re

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other_node):
        return (self.text == other_node.text and self.text_type == other_node.text_type and self.url == other_node.url)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"
text_type_list = [text_type_text, text_type_bold, text_type_italic, text_type_code, text_type_link, text_type_image]

def text_node_to_html_node(text_node):
    if text_node.text_type not in text_type_list:
        raise Exception(f"Invalid text_node.text_type: {text_node.text_type}")
    if text_node.text_type == text_type_text:
        return LeafNode(None, text_node.text)
    if text_node.text_type == text_type_bold:
        return LeafNode("b", text_node.text)
    if text_node.text_type == text_type_italic:
        return LeafNode("i", text_node.text)
    if text_node.text_type == text_type_code:
        return LeafNode("code", text_node.text)
    if text_node.text_type == text_type_link:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == text_type_image:
        return LeafNode("img", "", {"src": text_node.url, "src": text_node.text})


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_text_nodes = []
    for old_node in old_nodes:
        if not isinstance(old_node, TextNode):
            new_text_nodes.append(old_node)
            continue
        if delimiter not in ["**", "*", "`"]:
            raise ValueError(f"Invalid delimiter: {delimiter}")
        old_node_split = old_node.text.split(delimiter)
        if len(old_node_split) == 1:
            new_text_nodes.append(old_node)
            continue
        if len(old_node_split) % 2 == 0:
            raise ValueError(f"Invalid delimiter count, found: {len(old_node_split) - 1}")
        x = 0
        for o_n_s in old_node_split:
            if o_n_s == "":
                x += 1
            elif x % 2 == 0:
                new_text_nodes.append(TextNode(o_n_s, text_type_text))
            else:
                new_text_nodes.append(TextNode(o_n_s, text_type))
            x += 1
    return new_text_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)" , text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)" , text)


def split_nodes_image(old_nodes):
    new_text_nodes = []
    for old_node in old_nodes:
        if not isinstance(old_node, TextNode):
            new_text_nodes.append(old_node)
        extracted_images = extract_markdown_images(old_node.text)
        count_e = len(extracted_images)
        if count_e == 0:
            new_text_nodes.append(old_node)
        text_to_split = old_node.text
        for j in extracted_images:
            reconstructed_e = f"![{j[0]}]({j[1]})"
            split_by_e = text_to_split.split(reconstructed_e, 1)
            if split_by_e[0] != "":
                new_text_nodes.append(TextNode(split_by_e[0], text_type_text))
            new_text_nodes.append(TextNode(j[0], text_type_image, j[1]))
            if split_by_e[1] != "":
                if extracted_images.index(j) < (count_e - 1):
                    text_to_split = split_by_e[1]
                else:
                    new_text_nodes.append(TextNode(split_by_e[1], text_type_text))
    return new_text_nodes

def split_nodes_link(old_nodes):
    new_text_nodes = []
    for old_node in old_nodes:
        if not isinstance(old_node, TextNode):
            new_text_nodes.append(old_node)
        extracted_links = extract_markdown_links(old_node.text)
        count_e = len(extracted_links)
        if count_e == 0:
            new_text_nodes.append(old_node)
        text_to_split = old_node.text
        for j in extracted_links:
            reconstructed_e = f"[{j[0]}]({j[1]})"
            split_by_e = text_to_split.split(reconstructed_e, 1)
            if split_by_e[0] != "":
                new_text_nodes.append(TextNode(split_by_e[0], text_type_text))
            new_text_nodes.append(TextNode(j[0], text_type_link, j[1]))
            if split_by_e[1] != "":
                if extracted_links.index(j) < (count_e - 1):
                    text_to_split = split_by_e[1]
                else:
                    new_text_nodes.append(TextNode(split_by_e[1], text_type_text))
    return new_text_nodes


def text_to_textnodes(text):
    text_node_s = [TextNode(text, text_type_text)]
    text_node_s = split_nodes_delimiter(text_node_s, "**", text_type_bold)
    text_node_s = split_nodes_delimiter(text_node_s, "*", text_type_italic)
    text_node_s = split_nodes_delimiter(text_node_s, "`", text_type_code)
    text_node_s = split_nodes_image(text_node_s)
    text_node_s = split_nodes_link(text_node_s)
    return text_node_s

