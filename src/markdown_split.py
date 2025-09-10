import re
from textnode import TextType,TextNode

def split_nodes_delimiter(old_nodes, delimeter, text_type):
    res = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            res.append(node)
            continue
        list_word = node.text.split()
        block = []
        same = ""
        for word in list_word:
            # Single word modifyer
            if (word[0] == delimeter or word[:2] == delimeter) and (word[-1] == delimeter or word[-2:] == delimeter):
                if block:
                    res.append(TextNode(" ".join(block), node.text_type))
                    block = []
                if len(delimeter) == 2:
                    res.append(TextNode(word[2:-2], text_type))
                elif len(delimeter) == 1:
                    res.append(TextNode(word[1:-1], text_type))
            
            # Check for start of modifier block
            elif word[0] == delimeter or word[:2] == delimeter:
                if block:
                    res.append(TextNode(" ".join(block), node.text_type))
                    block = []
                if delimeter == "**":
                    block.append(word[2:])
                    same = "**"
                elif delimeter == "`":
                    block.append(word[1:])
                    same = "`"
                elif delimeter == "_":
                    block.append(word[1:])
                    same = "_"
                
            # Check for end of modifier block
            elif word[-1] == delimeter or word[-2:] == delimeter:
                if same != delimeter:
                    raise Exception("Nested element is not allowed, for now")
                if delimeter == "**" and same == delimeter:
                    block.append(word[:-2])
                    same = ""
                elif delimeter == "`" and same == delimeter:
                    block.append(word[:-1])
                    same = ""
                elif delimeter == "_" and same == delimeter:
                    block.append(word[:-1])
                    same = ""

                res.append(TextNode(" ".join(block), text_type))
                block = []

            # Adding middle block or normal text
            else:
                block.append(word)

        if same:
            raise Exception("No closing delimeter found")
        if block:
            res.append(TextNode(" ".join(block), node.text_type))   
        return res


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    res = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            res.append(node)
            continue
        list_image = extract_markdown_images(node.text)
        
        remains = node.text
        for couple in list_image:
            
            text, url = couple
            start = remains.find(text)
            
            length = len(text) + len(url) + 3
            
            res.append(TextNode(remains[:start-2], node.text_type))
            res.append(TextNode(text, TextType.IMAGE, url))
            remains = remains[start+length:]
            
        if remains:
            res.append(TextNode(remains, node.text_type))
        
        return res

def split_nodes_link(old_nodes):
    res = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            res.append(node)
            continue
        list_image = extract_markdown_links(node.text)
        
        remains = node.text
        for couple in list_image:
            
            text, url = couple
            start = remains.find(text)
            
            length = len(text) + len(url) + 3
            
            res.append(TextNode(remains[:start-1], node.text_type))
            res.append(TextNode(text, TextType.LINK, url))
            remains = remains[start+length:]
            
        if remains:
            res.append(TextNode(remains, node.text_type))
        
        return res


def text_to_textnodes(text):
    