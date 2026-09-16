from extract_markdown_images import extract_markdown_images, extract_markdown_links
from textnode import BlockType, TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    output_list = []
    for node in old_nodes:
        temp_list = []
        if node.text_type != TextType.TEXT:
            output_list.append(node)
            continue
        new_nodes = node.text.split(delimiter)
        if len(new_nodes) % 2 == 0:
            raise ValueError("No closing delimiter")
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
    output_list = []
    for node in old_nodes:
        temp_list = []
        if node.text_type != TextType.TEXT:
            output_list.append(node)
            continue
        new_nodes = extract_markdown_images(node.text)
        if new_nodes == []:
            output_list.append(node)
            continue
        remaining_text = node.text
        for alt_text, url in new_nodes:
            marker = f'![{alt_text}]({url})'
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
    output_list = []
    for node in old_nodes:
        temp_list = []
        if node.text_type != TextType.TEXT:
            output_list.append(node)
            continue
        new_nodes = extract_markdown_links(node.text)
        if new_nodes == []:
            output_list.append(node)
            continue
        remaining_text = node.text
        for alt_text, url in new_nodes:
            marker = f'[{alt_text}]({url})'
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



def text_to_textnodes(text):
    converted_text = [TextNode(text, TextType.TEXT)]
    split_nodes_run1 = split_nodes_delimiter(converted_text, "**", TextType.BOLD)
    split_nodes_run2 = split_nodes_delimiter(split_nodes_run1, "`", TextType.CODE)
    split_nodes_run3 = split_nodes_delimiter(split_nodes_run2, "_", TextType.ITALIC)
    split_image_run = split_nodes_image(split_nodes_run3)
    split_link_run = split_nodes_link(split_image_run)
    return split_link_run



def markdown_to_blocks(markdown):
    output_list = []
    split_markdown = markdown.split("\n\n")
    stripped_markdown = list(map(str.strip, split_markdown))
    for item in stripped_markdown:
        if item != "":
            output_list.append(item)
    return output_list


def block_to_block_type(block: str):
    split_block = block.split("\n")
    # Checking for hashtags in block; if between 1-6 followed by a space, it is a heading. Otherwise, move on.
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    # Checking if the block starts and ends with backticks, and is multiline, in which case it is code. Otherwise, move on.
    if len(split_block) > 1 and split_block[0].startswith("```") and split_block[-1].startswith("```"):
        return BlockType.CODE
    # Checking if all lines starts with >, in which case it is a quote block; otherwise, not.
    if all(line.startswith(">") for line in split_block):
        return BlockType.QUOTE
    # Checking if all lines starts with a ash and a space, in which case it is an unordered list. Otherwise, moves on.
    if all(line.startswith("- ") for line in split_block):
            return BlockType.UNORDERED_LIST
    # Checking if the first line starts with 1. and all following lines increment the number by 1,
    #  in which case it is an ordered list. Otherwise, move to the final check
    if block.startswith("1. ") and all(
        line.startswith(f"{i}. ") for i, line in enumerate(split_block, start=1)):
            return BlockType.ORDERED_LIST
    # If none of the above, then it is a paragraph!
    return BlockType.PARAGRAPH
