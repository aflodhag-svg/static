class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props == {} or self.props is None:
            return ""
        result = ""
        for key, value in self.props.items():
            result += f' {key}="{value}"'
        return result

    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'

    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)


    def to_html(self):
        if self.value is None:
            raise ValueError("No value")
        if self.tag is None:
            return str(self.value)
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    def __repr__(self):
        return f'LeafNode({self.tag}, {self.value}, {self.props})'

    def __eq__(self, other):
        if self.tag is not None:
            return self.tag == other.tag and self.value == other.value and self.props == other.props
        if self.tag is None:
            return self.value == other.value and self.props == other.props


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("No tag")
        if self.children is None:
            raise ValueError("No children")
        if self.children == []:
            raise ValueError("List of children is empty")
        html_string = f'<{self.tag}{self.props_to_html()}>'
        for child in self.children:
               html_string += child.to_html()
        html_string += f"</{self.tag}>"
        return html_string
