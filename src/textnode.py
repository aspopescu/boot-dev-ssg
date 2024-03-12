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
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})


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
            raise ValueError(f"Invalid delimiter count, found: {len(old_node_split) - 1} --{old_node_split}--")
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
    #print(f"+{old_nodes}==")
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
    #print(f"+return+{new_text_nodes}--")
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
    #print(f"+return+text_node_s+{text_node_s}--")
    return text_node_s


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    e = []
    for b in blocks:
        if b != "":
            e.append(b.strip())  
    return e

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

def block_to_block_type(block):
    block_lines = block.split("\n")
    lines_count = len(block_lines)
    headings_prefixes = ('# ','## ','### ','#### ','##### ','###### ',)
    if block.startswith(headings_prefixes):
        return block_type_heading
    code_affix = "```"
    if block.startswith(code_affix) and block.endswith(code_affix):
        return block_type_code
    quote_prefix = ">"
    unordered_list_prefixes = ("* ", "- ")
    quote_status = True
    asterisk_status = True
    hyphen_status = True
    ordered_status = True
    for l in range(lines_count):
        if not block_lines[l].startswith(quote_prefix):
            quote_status = False
        if not block_lines[l].startswith(unordered_list_prefixes[0]):
            asterisk_status = False
        if not block_lines[l].startswith(unordered_list_prefixes[1]):
            hyphen_status = False
        if not block_lines[l].startswith(f"{l + 1}. "):
            ordered_status = False
    if quote_status:
        return block_type_quote
    if asterisk_status or hyphen_status:
        return block_type_unordered_list
    if ordered_status:
        return block_type_ordered_list
    #print(f"+return+block_type_paragraph+{block_type_paragraph}-for-{block}--")
    return block_type_paragraph

def markdown_to_html_node(markdown):
    md_blocks = markdown_to_blocks(markdown)
    #print(f"+md_blocks+{md_blocks}--")
    list_of_html_nodes = []
    for b in md_blocks:
        #print(f"+b+{b}--")
        lines = b.split("\n")
        #print(f"+lines+{lines}--")
        if block_to_block_type(b) == block_type_paragraph:
            #print(f"+block_to_block_type(b)+{block_to_block_type(b)}--")
            white_space_fix = " ".join(lines)
            #print(f"+white_space_fix+{white_space_fix}--")
            leaf_nodes = []
            text_nodes = text_to_textnodes(white_space_fix)
            #print(f"+text_nodes+{text_nodes}--")
            for t in text_nodes:
                #print(f"+t+{t}--")
                leaf_node = text_node_to_html_node(t)
                #print(f"+leaf_node+{leaf_node}--")
                leaf_nodes.append(leaf_node)
                #print(f"+leaf_nodes+{leaf_nodes}--")
            paragraph_node = ParentNode("p", leaf_nodes)
            list_of_html_nodes.append(paragraph_node)
        if block_to_block_type(b) == block_type_heading:
            for l in lines:
                if l.startswith("# "):
                    l = l[2:]
                    heading = LeafNode("h1", l)
                    list_of_html_nodes.append(heading)
                if l.startswith("## "):
                    l = l[3:]
                    heading = LeafNode("h2", l)
                    list_of_html_nodes.append(heading)
                if l.startswith("### "):
                    l = l[4:]
                    heading = LeafNode("h3", l)
                    list_of_html_nodes.append(heading)
                if l.startswith("#### "):
                    l = l[5:]
                    heading = LeafNode("h4", l)
                    list_of_html_nodes.append(heading)
                if l.startswith("##### "):
                    l = l[6:]
                    heading = LeafNode("h5", l)
                    list_of_html_nodes.append(heading)
                if l.startswith("###### "):
                    l = l[7:]
                    heading = LeafNode("h6", l)
                    list_of_html_nodes.append(heading)
        if block_to_block_type(b) == block_type_code:
            b = b[3:]
            b = b[:-3]
            b = b.strip()
            code_block = ParentNode("pre", [LeafNode("code", b)])
            list_of_html_nodes.append(code_block)
        if block_to_block_type(b) == block_type_quote:
            quote_fix = []
            for l in lines:
                quote_fix.append(l[2:])
            white_space_fix = " ".join(quote_fix)
            quote = LeafNode("blockquote", white_space_fix)
            list_of_html_nodes.append(quote)
        if block_to_block_type(b) == block_type_unordered_list:
            hyphen_fix = []
            for l in lines:
                hyphen_fix.append(l[2:])
            nodes = []
            for i in hyphen_fix:
                if len(text_to_textnodes(i)) == 1 and text_to_textnodes(i)[0].text_type == text_type_text:
                    nodes.append(LeafNode("li", i))
                else:
                    text_nodes = text_to_textnodes(i)
                    leaf_nodes = []
                    for t in text_nodes:
                        leaf_node = text_node_to_html_node(t)
                        leaf_nodes.append(leaf_node)
                    nodes.append(ParentNode("li", leaf_nodes))
            unordered_list = ParentNode("ul", nodes)
            list_of_html_nodes.append(unordered_list)
        if block_to_block_type(b) == block_type_ordered_list:
            number_fix = []
            for l in lines:
                number_fix.append(l[3:])
            nodes = []
            for i in number_fix:
                if len(text_to_textnodes(i)) == 1 and text_to_textnodes(i)[0].text_type == text_type_text:
                    nodes.append(LeafNode("li", i))
                else:
                    text_nodes = text_to_textnodes(i)
                    leaf_nodes = []
                    for t in text_nodes:
                        leaf_node = text_node_to_html_node(t)
                        leaf_nodes.append(leaf_node)
                    nodes.append(ParentNode("li", leaf_nodes))
            ordered_list = ParentNode("ol", nodes)
            list_of_html_nodes.append(ordered_list)
    return ParentNode("div", list_of_html_nodes)

