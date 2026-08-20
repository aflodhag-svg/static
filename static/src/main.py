from textnode import TextNode, TextType

print("hello world")


def main():
    message = TextNode("Some text", TextType.LINK, "https://www.boot.dev")
    print(message)


main()
