class HTMLNode():
    def __init__(self,tag=None,value=None,children=None,props=None):
        # html tag string
        self.tag = tag
        # value inside html tag
        self.value = value
        # list of html nodes inside
        self.children = children
        # dictionary of attributes
        self.props = props
    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if self.props == None:
            return ''
        res = ''
        for tag in self.props:
            res += ' ' + tag + '="' + self.props[tag] + '"'
        return res
        
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class LeafNode(HTMLNode):
    # tag and value are required
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag,value=value,props=props)

    def to_html(self):
        if self.value is None:
            raise valueError("All leaf node must have value")
        if self.tag is None:
            return self.value

        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

