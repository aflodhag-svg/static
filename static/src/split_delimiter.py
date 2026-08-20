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
