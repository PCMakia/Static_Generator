from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode():
    def __init__(self, content, TType, url=None):
        self.text = content
        self.text_type = TType
        self.url = url

    def __eq__(self, Node):
        if self.text == Node.text:
            if self.text_type == Node.text_type:
                if self.url == Node.url:
                    return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


    