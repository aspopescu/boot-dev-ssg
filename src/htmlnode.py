class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("HTMLNode: to_html not done.")

    def props_to_html(self):
        p_to_h = ""
        if self.props == None:
            return p_to_h
        for p in self.props:
            value = f'"{self.props[p]}"'
            to_add = f" {p}={value}"
            p_to_h += to_add
        return p_to_h

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        #print(f"LN::{self.__repr__()}::")
        if self.value == None:
            raise ValueError("LeafNode: All leaf nodes require a value.")
        if self.tag == None:
            return self.value
        tag_value = self.value
        returned_props = self.props_to_html()
        opening_tag = f"<{self.tag}{returned_props}>"
        closing_tag = f"</{self.tag}>"
        return f"{opening_tag}{tag_value}{closing_tag}"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNode: The tag is not provided.")
        if self.children == None:
            raise ValueError("ParentNode: There are no children.")
        opening_tag = f"<{self.tag}>"
        closing_tag = f"</{self.tag}>"
        returned_html = ""
        #print(f"pn_ch--{self.children}--")
        if len(self.children) == 0:
            returned_html += ""
            return f"{opening_tag}{returned_html}{closing_tag}"
        for c in self.children:
            returned_html += c.to_html()
        return f"{opening_tag}{returned_html}{closing_tag}"

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"

