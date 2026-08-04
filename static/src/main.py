from textnode import TextType
from textnode import TextNode

print("hello world")


def main():
    message = TextNode("Some text", TextType.LINK, "https://www.boot.dev")
    print(message)


main()
