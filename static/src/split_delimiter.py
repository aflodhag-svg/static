from collections.abc import Sequence
from typing import assert_never

from extract_markdown_images import extract_markdown_images, extract_markdown_links
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import BlockType, TextNode, TextType, text_node_to_html_node


def split_nodes_delimiter(
    old_nodes: list[TextNode],
    delimiter: str,
    text_type: TextType) -> list[TextNode]:

    output_list:list [TextNode] = []
    for node in old_nodes:
        temp_list: list[TextNode] = []
        if node.text_type != TextType.TEXT:
            output_list.append(node)
            continue
        new_nodes = node.text.split(delimiter)
        if len(new_nodes) % 2 == 0:
            error = "No closing delimiter"
            raise ValueError(error)
        for i, v in enumerate(new_nodes):
            if v == "":
                continue
            if i % 2 == 0:
                temp_list.append(TextNode(v, TextType.TEXT))
            else:
                temp_list.append(TextNode(v, text_type))
        output_list.extend(temp_list)
    return output_list




def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    output_list: list[TextNode] = []
    for node in old_nodes:
        temp_list: list[TextNode] = []
        if node.text_type != TextType.TEXT:
            output_list.append(node)
            continue
        new_nodes = extract_markdown_images(node.text)
        if new_nodes == []:
            output_list.append(node)
            continue
        remaining_text = node.text
        for alt_text, url in new_nodes:
            marker = f"![{alt_text}]({url})"
            sections = remaining_text.split(marker, 1)
            text_to_append = TextNode(sections[0], TextType.TEXT)
            if sections[0] != "":
               temp_list.append(text_to_append)
            temp_list.append(TextNode(alt_text, TextType.IMAGE, url))
            remaining_text = sections[1]
        final_node = TextNode(remaining_text, TextType.TEXT)
        if final_node.text != "":
           temp_list.append(final_node)
        output_list.extend(temp_list)
    return output_list




def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    output_list: list[TextNode] = []
    for node in old_nodes:
        temp_list: list[TextNode] = []
        if node.text_type != TextType.TEXT:
            output_list.append(node)
            continue
        new_nodes = extract_markdown_links(node.text)
        if new_nodes == []:
            output_list.append(node)
            continue
        remaining_text = node.text
        for alt_text, url in new_nodes:
            marker = f"[{alt_text}]({url})"
            sections = remaining_text.split(marker, 1)
            text_to_append = TextNode(sections[0], TextType.TEXT)
            if sections[0] != "":
               temp_list.append(text_to_append)
            temp_list.append(TextNode(alt_text, TextType.LINK, url))
            remaining_text = sections[1]
        final_node = TextNode(remaining_text, TextType.TEXT)
        if final_node.text != "":
           temp_list.append(final_node)
        output_list.extend(temp_list)
    return output_list



def text_to_textnodes(text: str) -> list[TextNode]:
    converted_text = [TextNode(text, TextType.TEXT)]
    split_nodes_run1 = split_nodes_delimiter(converted_text, "**", TextType.BOLD)
    split_nodes_run2 = split_nodes_delimiter(split_nodes_run1, "`", TextType.CODE)
    split_nodes_run3 = split_nodes_delimiter(split_nodes_run2, "_", TextType.ITALIC)
    split_image_run = split_nodes_image(split_nodes_run3)
    return split_nodes_link(split_image_run)



def markdown_to_blocks(markdown: str) -> list[str]:
    split_markdown = markdown.split("\n\n")
    stripped_markdown = list(map(str.strip, split_markdown))
    return [item for item in stripped_markdown if item != ""]


def block_to_block_type(block: str) -> BlockType:
    split_block = block.split("\n")
    # Checking for hashtags in block;
    # if between 1-6 followed by a space, it is a heading. Otherwise, move on.
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    # Checking if the block starts and ends with backticks and is multiline,
    # in which case it is code. Otherwise, move on.
    if (len(split_block) > 1
        and split_block[0].startswith("```")
        and split_block[-1].startswith("```")):
        return BlockType.CODE
    # Checking if all lines starts with >, in which case it is a quote block;
    # otherwise, not.
    if all(line.startswith(">") for line in split_block):
        return BlockType.QUOTE
    # Checking if all lines starts with a dash and a space,
    # in which case it is an unordered list. Otherwise, moves on.
    if all(line.startswith("- ") for line in split_block):
            return BlockType.UNORDERED_LIST
    # Checking if the first line starts with 1.
    # and all following lines increment the number by 1,
    # in which case it is an ordered list. Otherwise, move to the final check
    if block.startswith("1. ") and all(
        line.startswith(f"{i}. ") for i, line in enumerate(split_block, start=1)):
            return BlockType.ORDERED_LIST
    # If none of the above, then it is a paragraph!
    return BlockType.PARAGRAPH

def text_to_children(text: str) -> Sequence[HTMLNode]:
    text_node = text_to_textnodes(text)
    children: list[LeafNode] = []
    for node in text_node:
        html_node = text_node_to_html_node(node)
        children.append(html_node)
    return children


def blocktype_to_html_node(block: str) -> ParentNode:
    block_type = block_to_block_type(block)
    match block_to_block_type(block):
        case BlockType.HEADING:
            heading_split = block.split(" ", 1)
            max_headers = 6
            if len(heading_split[0]) > max_headers:
                error = "Invalid routing has made amount of headers exceed 6"
                raise ValueError(error)
            level = f"h{len(heading_split[0])}"
            text = heading_split[1]
            children: Sequence[HTMLNode] = text_to_children(text)
            return ParentNode(level, children=children)
        case BlockType.QUOTE:
            quote_split = block.split("\n")
            stripped_list = [
                line.lstrip(">").strip() for line in quote_split
            ]
            text = " ".join([line for line in stripped_list if line])
            children = text_to_children(text)
            return ParentNode("blockquote", children=children)
        case BlockType.CODE:
            split_block = block.split("\n")
            first_last_gone = split_block[1:-1]
            text = "\n".join(first_last_gone) + "\n"
            code_node = TextNode(text, TextType.CODE)
            leaf = text_node_to_html_node(code_node)
            return ParentNode("pre", children=[leaf])
        case BlockType.UNORDERED_LIST:
            split_list = block.split("\n")
            line_list: list[ParentNode] = []
            for line in split_list:
                cleaned_line = line.lstrip("-").strip()
                children = text_to_children(cleaned_line)
                to_append = ParentNode("li", children=children)
                line_list.append(to_append)
            return ParentNode("ul", children=line_list)
        case BlockType.ORDERED_LIST:
            split_block = block.split("\n")
            ordered_lines: list[ParentNode] = []
            for line in split_block:
                period_found = line.split(".", 1)
                stuff_removed = period_found[1].strip()
                children = text_to_children(stuff_removed)
                to_append = ParentNode("li", children=children)
                ordered_lines.append(to_append)
            return ParentNode("ol", children=ordered_lines)
        case BlockType.PARAGRAPH:
            new_string = " ".join(block.split("\n"))
            children = text_to_children(new_string)
            return ParentNode("p", children=children)
    assert_never(block_type)



def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocked = markdown_to_blocks(markdown)
    children: list[ParentNode] = []
    for block in blocked:
        child = blocktype_to_html_node(block)
        children.append(child)
    return ParentNode("div", children=children)
