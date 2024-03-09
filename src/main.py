from textnode import TextNode
from htmlnode import *


def main():
    print("hello world")
    tn_text = "this is a text node"
    tn_text_type = "bolda"
    tn_url = "https://www.boot.dev"
    
    test_textnode = TextNode(tn_text, tn_text_type, tn_url)
    print(test_textnode)

    leaf = LeafNode("p", "text test", {"href": "https://www.google.com"})
    leaf.to_html()
    print(leaf)
    print(leaf.to_html())

main()

