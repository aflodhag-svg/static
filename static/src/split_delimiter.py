from extract_markdown_images import extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    output_list = []
    for node in old_nodes:
        temp_list = []
        if node.text_type != TextType.TEXT:
            output_list.append(node)
            continue
        new_nodes = node.text.split(delimiter)
        if len(new_nodes) % 2 == 0:
            raise Exception("No closing delimiter")
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
