class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None)
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props

    def to_html(self):
        raise Exception(NotImplementedError)

    def props_to_html(self):
        if self.props == {} or self.props is None:
            return ""
        result = ""
        for key, value in self.props.items():
            result +=   f' {key}="{value}"'
        return result
