import unittest
from textnode import *

class TestMarkdownToHTML(unittest.TestCase):
    def test_code_blocks_v(self):
        md = """
# Markdown syntax guide

## Headers

# This is a Heading h1
## This is a Heading h2
###### This is a Heading h6

## Emphasis

*This text will be italic*  
*This will also be italic*

**This text will be bold**  
**This will also be bold**

You **can** *combine* them

## Lists

### Unordered

* Item 1
* Item 2
* Item 2a
* Item 2b

### Ordered

1. Item 1
2. Item 2
3. Item 3
4. Item 3a
5. Item 3b

## Images

This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)

## Links

You may be using [Markdown Live Preview](https://markdownlivepreview.com/).

## Blockquotes

> Markdown is a lightweight markup language with plain-text-formatting syntax, created in 2004 by John Gruber with Aaron Swartz.
>
> Markdown is often used to format readme files, for writing messages in online discussion forums, and to create rich text using a plain text editor.

## Blocks of code

```
let message = 'Hello world';
alert(message);
```

## Inline code

This web site is using `markedjs/marked`.
"""
        expected_html = """<div><h1>Markdown syntax guide</h1><h2>Headers</h2><h1>This is a Heading h1</h1><h2>This is a Heading h2</h2><h6>This is a Heading h6</h6><h2>Emphasis</h2><p>This text will be italic<i>   </i>This will also be italic</p><p>This text will be bold<b>   </b>This will also be bold</p><p>You <b>can</b> <i>combine</i> them</p><h2>Lists</h2><h3>Unordered</h3><ul><li>Item 1</li><li>Item 2</li><li>Item 2a</li><li>Item 2b</li></ul><h3>Ordered</h3><ol><li>Item 1</li><li>Item 2</li><li>Item 3</li><li>Item 3a</li><li>Item 3b</li></ol><h2>Images</h2><p>This is text with an <img src="https://i.imgur.com/zjjcJKZ.png" alt="image"></img> and another <img src="https://i.imgur.com/3elNhQu.png" alt="second image"></img></p><h2>Links</h2><p>You may be using <a href="https://markdownlivepreview.com/">Markdown Live Preview</a>.</p><h2>Blockquotes</h2><blockquote>Markdown is a lightweight markup language with plain-text-formatting syntax, created in 2004 by John Gruber with Aaron Swartz.  Markdown is often used to format readme files, for writing messages in online discussion forums, and to create rich text using a plain text editor.</blockquote><h2>Blocks of code</h2><pre><code>let message = 'Hello world';
alert(message);</code></pre><h2>Inline code</h2><p>This web site is using <code>markedjs/marked</code>.</p></div>"""
        node = markdown_to_html_node(md)
        #print(f"code--{node}--code")
        html = node.to_html()
        #print(f"code----{html}--[][]")
        self.assertEqual(
            html,
            expected_html
        )

if __name__ == "__main__":
    unittest.main()
