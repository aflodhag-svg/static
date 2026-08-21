import re


def extract_markdown_images(text) -> list[tuple]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)



def extract_markdown_links(text) -> list[tuple]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
