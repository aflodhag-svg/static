from typing import override


class HTMLNode:
    tag: str | None
    value: str | None
    children: list["HTMLNode"] | None
    props: dict[str, str] | None

    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ) -> None:

        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        if self.props == {} or self.props is None:
            return ""
        result = ""
        for key, value in self.props.items():
            result += f' {key}="{value}"'
        return result
    @override
    def __repr__(self) -> str:
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HTMLNode):
            return False
        return (
                self.tag == other.tag
                and self.value == other.value
                and self.children == other.children
                and self.props == other.props
        )


class LeafNode(HTMLNode):
    def __init__(self,
        tag: str | None,
        value: str | None,
        props: dict[str, str] | None = None
    ):
        super().__init__(tag=tag, value=value, children=None, props=props)

    @override
    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("No value")
        if self.tag is None:
            return str(self.value)
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    @override
    def __repr__(self):
        return f'LeafNode({self.tag}, {self.value}, {self.props})'

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LeafNode):
            return False
        if self.tag is not None:
            return self.tag == other.tag and self.value == other.value and self.props == other.props
        else:
            return self.value == other.value and self.props == other.props


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        children: list[HTMLNode] | None = None,
        props: dict[str, str] | None = None
    ):
        super().__init__(tag=tag, value=None, children=children, props=props)
    @override
    def to_html(self) -> str:
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
