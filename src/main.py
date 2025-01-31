from helperfunctions import block_to_block_type, extract_markdown_images, extract_markdown_links, markdown_to_blocks, separate_text_based_on_markdown, split_nodes_delimiter, split_nodes_images, split_nodes_link
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextType
from helper_vars import markdown

def main():
  # text_node = TextNode("This is a text node", TextType.BOLD, "https://.boot.dev")
  # print(text_node.__repr__())
  # children_node_1 = HTMLNode()
  # children_node_2 = HTMLNode()
  # html_node = HTMLNode("tag_name", "value_name", [children_node_1, children_node_2], {"children":"children1","children2":"children3"})
  # print(html_node.__repr__())
  # leaf_node_1 = LeafNode(
  #   "p",
  #   "Some text",
  #   {"class": "something", "href": "https://boot.dev"}
  # )
  # print(leaf_node_1)
  # node = ParentNode(
  #   "p",
  #   [
  #   ],
  # )
  # print("html_node_2")
  # html_node_2 = text_node_to_html_node(text_node)
  # print(html_node_2)
  # print(html_node_2.to_html())

  # node = TextNode("This is text with a `code block` word", TextType.TEXT)
  # new_nodes_link = split_nodes_delimiter([node], "`", TextType.CODE)
  # node_last = TextNode("This is text with a word `code block`", TextType.TEXT)
  # new_nodes_last = split_nodes_delimiter([node_last], "`", TextType.CODE)
  # node_first = TextNode("`code block` This is text with a word", TextType.TEXT)
  # new_nodes_first = split_nodes_delimiter([node_first], "`", TextType.CODE)
  
  # node_new_links = TextNode(
  #   "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
  #   TextType.TEXT,
  # )
  # node_new_images = TextNode(
  #   "This is text with a link ![boot dev image](https://www.boot.dev) and ![youtube image](https://www.youtube.com/@bootdotdev)",
  #   TextType.TEXT,
  # )

  # new_nodes_link = split_nodes_link([node_new_links])
  # print("--->new_nodes_link")
  # print(new_nodes_link)
  # for i in new_nodes_link:
  #   print(f'--->{i}')
  # new_nodes_image = split_nodes_images([node_new_images])
  # print("--->new_nodes_image")
  # print(new_nodes_image)

  # [
  #     TextNode("This is text with a link ", TextType.TEXT),
  #     TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
  #     TextNode(" and ", TextType.TEXT),
  #     TextNode(
  #         "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
  #     ),
  # ]
  # text = "This is **bold text** with *italic text 1* an *italic text* word and *italic 3* a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
  # print(separate_text_based_on_markdown(text))

  # text2 = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
  # print(separate_text_based_on_markdown(text2))

  # print('---')
  # print(markdown_to_blocks(markdown))
  # print('---_')
  # text = ["asdf", "##### ASdf asdf qwer asdf \n###### ASdf asdf qwer asdf", "# asdf asdqwe qwe", "####### asdf qwer", "###qwer", "#qwer", "#######qwer"]
  # text_code = ["```  asdf  3 things```", "`  asdf qwer`", "```  asdf```", "asdf  `", "`  asdfqwe rrqw `qwer", "asdf"]
  # text_quote = [">  asdf  ```", "< asdf qwer", "`>  asdf 123 ", ">asdf", "> asdf", "asdf"]
  # text_unordered_list = ["ASD * asdf", "-asdf qwer", "*  asdf 123 ", "- asdf qwqer", "> asdf", "asdf"]
  # text_ordered_list = ["1. ASD * asdf \n2. thing. \n3. thing2\n4. thing3", "2 .-asdf qwer", "3. *  asdf 123 \n2. asdf \n 1.", "1. asdf\n 2. asdf\n 4. - asdf qwqer", "> asdf", "asdf", "1. asdf \n2. asdf2 \n3. asdf3\n4. asdf4\n5. asdf5"]

  # print('--->block_to_block_type')
  # for i in text:
  #   print(block_to_block_type(i))
  # for i in text_code:
  #   print(block_to_block_type(i))
  # for i in text_quote:
  #   print(block_to_block_type(i))
  # for i in text_unordered_list:
  #   print(block_to_block_type(i))
  # for i in text_ordered_list:
  #   print(block_to_block_type(i))

  # print('<---block_to_block_type')

  text_list = ['- asdf\n* asdf2\n* asdf3\n- some']

  block_to_block_type(text_list[0])


def text_node_to_html_node(text_node):
  match(text_node.text_type):
    case TextType.TEXT:
      return LeafNode("p", text_node.text)
    case TextType.BOLD:
      return LeafNode("b", text_node.text)
    case TextType.ITALIC:
      return LeafNode("i", text_node.text)
    case TextType.CODE:
      return LeafNode("code", text_node.text)
    case TextType.LINK:
      return LeafNode("a", text_node.text, {"href": text_node.url})
    case TextType.IMAGE:
      return LeafNode("img", text_node.text, {"src": text_node.url, "alt": text_node.text})
    case _:
      raise ValueError(f"Invalid text type: {text_node.text_type}")


if __name__ == '__main__':
  main() 