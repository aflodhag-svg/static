from enum import Enum
from typing import assert_never

from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold_text"
    ITALIC = "italic_text"
    CODE = "code_text"
    LINK = "link"
    IMAGE = "image"


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"



class TextNode:
    def __init__(self,
        text: str,
        text_type: TextType,
        url: str | None = None) -> None:

        self.text = text
        self.text_type = text_type
        self.url = url


    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextNode):
            return False
        return (
        self.text == other.text
        and self.text_type == other.text_type
        and self.url == other.url)


    def __hash__(self) -> int:
        return hash((self.text, self.text_type, self.url))

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"



def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            if text_node.url is None:
                error = "link text node missing url"
                raise ValueError(error)
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            if text_node.url is None:
                error = "image text node missing url"
                raise ValueError(error)
            return LeafNode("img","", {"src": text_node.url, "alt": text_node.text})
    assert_never(text_node.text_type)
