import re
from htmlnode import HTMLNode
from leafnode import LeafNode
from textnode import TextNode, TextType, TextTypeMarkdown

def split_nodes_delimiter(old_nodes, delimiter, text_type):
  delimiters_nodes = []
  for old_node in old_nodes:
    if old_node.text_type != TextType.TEXT:
      delimiters_nodes.append(old_node)
      continue
    try:
      delimiters_nodes.extend(single_split_node_delimiter(old_node, delimiter, text_type))
    except ValueError as e:
      # print(f"ValueError: {e}")
      delimiters_nodes.append(old_node)
      continue
  return delimiters_nodes

def single_split_node_delimiter(old_node, delimiter, text_type):
  list_text = old_node.text.split(delimiter)

  if len(list_text) < 3:
    raise ValueError(f'Invalid syntax, no closer delimiter found: {delimiter} at: {list_text}')
  
  text_nodes_list = []
  for i in range(len(list_text)):
    if list_text[i] == '':
      continue
    if i % 2 == 1:
      text_nodes_list.append(TextNode(list_text[i], text_type))
    elif i % 2 == 0:
      text_nodes_list.append(TextNode(list_text[i], TextType.TEXT))

  return (
      text_nodes_list
    )

def extract_markdown_images(text):
  return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
  return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_general(old_nodes, regex, text_type):
  text_node_list = []
  mapped_nodes = []
  for i in old_nodes:
    if i.text_type == TextType.TEXT:
      mapped_nodes.extend(re.split(regex, i.text))
    elif i.text_type == TextType.IMAGE or i.text_type == TextType.LINK:
      mapped_nodes.append(i)
  for node in mapped_nodes:
    if isinstance(node, str):
      if node == '':
        continue
      
      extracted_objects = []
      if text_type == TextType.IMAGE:
        extracted_objects = extract_markdown_images(node)
      else:
        extracted_objects = extract_markdown_links(node)

      if len(extracted_objects) > 0:
        extracted_links_tuple = extracted_objects[0]
        text, url = extracted_links_tuple
        text_node_list.append(TextNode(text, text_type, url))
        continue
      
      text_node_list.append(
        TextNode(node, TextType.TEXT)
      )
    else:
      text_node_list.append(
          node
        )

  return text_node_list

def split_nodes_images(old_nodes):
  return split_nodes_general(old_nodes, r"(!\[.*?\]\(.*?\))", TextType.IMAGE)

def split_nodes_link(old_nodes):
  return split_nodes_general(old_nodes, r"(?<!\!)(\[.*?\]\(.*?\))", TextType.LINK)
  
def separate_text_based_on_markdown(text): 
  initial_text_node_lst = [TextNode(text, TextType.TEXT)]
  text_nodes = split_nodes_link(initial_text_node_lst)
  text_nodes_images = split_nodes_images(text_nodes)
  text_nodes_bold = split_nodes_delimiter(text_nodes_images, '**', TextType.BOLD)
  text_nodes_italic = split_nodes_delimiter(text_nodes_bold, '*', TextType.ITALIC)
  text_nodes_code = split_nodes_delimiter(text_nodes_italic, '`', TextType.CODE)
  return text_nodes_code

def markdown_to_blocks(markdown):
  lines = markdown.split('\n')
  total_lines_lst = []
  lines_lst = []

  for i in range(len(lines)):
    if lines[i] == '':
      total_lines_lst.extend(lines_lst)
      lines_lst = []
      continue
    lines_lst.append(lines[i])
    if i == len(lines) - 1:
      total_lines_lst.extend(lines_lst)

  return total_lines_lst

def match_ordered_list(text):
  text_split = text.split('\n')
  count = 1
  list_text = []

  for line in text_split:
    if line[0] == str(count) and line[1] == '.' and line[2] == ' ':
      count += 1
      list_text.append(line[3:])
      continue
    return False, text_split[0]
      
  return True, list_text[0]

def match_text_regex_list(text, regex):
  text_split = text.split('\n')
  list_text = []  

  for inner_text in text_split:
    result = re.findall(regex, inner_text)
    if not result:
      return False, text_split[0]
    list_text.extend(result)

  return True, list_text[0]

def block_to_block_type(text):
  # TODO: add bold italic
  print('----->block_to_block_type')
  print(text)
  list_separate_text_nodes = separate_text_based_on_markdown(text)
  if (len(list_separate_text_nodes) > 1):
    print("---------------->len(list_separate_text_nodes) > 1")
    print(list_separate_text_nodes)

  [is_type_heading, list_text_heading] = match_text_regex_list(text, r"^#{1,6}\s(.*)")
  if is_type_heading:
    return TextTypeMarkdown.HEADING, list_text_heading

  [is_type_code, list_text_code] = match_text_regex_list(text, r"^```(.*)```$")
  if is_type_code:
    return TextTypeMarkdown.CODE, list_text_code

  [is_type_quote, list_text_quote] = match_text_regex_list(text, r"^\>(.*)")
  if is_type_quote:
    return TextTypeMarkdown.QUOTE, list_text_quote

  [is_type_unordered_list, list_text_unordered_list] = match_text_regex_list(text, r"^[-*]\s(.*)")
  if is_type_unordered_list:
    print("list_text_unordered_list")
    print(list_text_unordered_list)
    return TextTypeMarkdown.UNORDERED_LIST_ITEM, list_text_unordered_list
    
  [is_type_ordered_list, list_text_ordered_list] = match_ordered_list(text)
  if is_type_ordered_list:
    return TextTypeMarkdown.ORDERED_LIST_ITEM, list_text_ordered_list

  return TextTypeMarkdown.PARAGRAPH, text

def markdown_to_list(markdown_text):
  return markdown_text.split('\n\n')

def markdown_to_html_node(markdown_text):
  markdown_list = markdown_to_list(markdown_text)

  list_blocks_text_nodes = []
  for mark_down_text in markdown_list:
    blocks = markdown_to_blocks(mark_down_text)
    print("blocks")
    print(blocks)
    for text in blocks:
      print(f"----->text: '{text}'")
      markdown_block = block_to_block_type(text)


      print("markdown_block")
      print(markdown_block)
      text_node = markdown_to_text_node(markdown_block)
      list_blocks_text_nodes.append(text_node)

  print('list_blocks_text_nodes')
  print(list_blocks_text_nodes)

  # TODO: validate for unordered lists

  # TODO: convert to HTML Nodes
  list_blocks_to_html_nodes(list_blocks_text_nodes)

def convert_to_list_parent_html():
  pass


def list_blocks_to_html_nodes(list_blocks_text_nodes):
  html_nodes = []
  list_counter = 0
  html_node_list_parent = HTMLNode()
  html_node_list_parent.children = []
  for index, text_node in enumerate(list_blocks_text_nodes):
    if text_node.text_type == TextType.UNORDERED_LIST_ITEM:
      if list_counter == 0:
        html_node_list_parent.tag = 'ul'
        list_counter += 1
      else:
        html_node_list_parent.children.append(text_node_to_html_node(text_node))
      if index + 1 < len(list_blocks_text_nodes) and list_blocks_text_nodes[index + 1].text_type != TextType.UNORDERED_LIST_ITEM:
        html_nodes.append(html_node_list_parent)
        html_node_list_parent = HTMLNode()
        list_counter = 0
        continue

    if text_node.text_type == TextType.ORDERED_LIST_ITEM:
      if list_counter == 0:
        html_node_list_parent.tag = 'ol'
        list_counter += 1
      else:
        html_node_list_parent.children.append(text_node_to_html_node(text_node))
      if index + 1 < len(list_blocks_text_nodes) and list_blocks_text_nodes[index + 1].text_type != TextType.ORDERED_LIST_ITEM:
        html_nodes.append(html_node_list_parent)
        html_node_list_parent = HTMLNode()
        list_counter = 0
        continue
    
    print('-->appended')
    html_nodes.append(text_node_to_html_node(text_node))

    print('---------------------------->separate_text_based_on_markdown(html_node.value)')

  print('------>html_nodes')
  print(html_nodes)
  
  print('html_nodes2')
  print([text_node_to_html_node(text_node) for text_node in list_blocks_text_nodes])

  return list_blocks_text_nodes


def markdown_to_text_node(markdown_tuple):
  [markdown_type, markdown_text] = markdown_tuple 
  print("markdown")
  print(markdown_type)
  print(markdown_text)

  if markdown_type == TextTypeMarkdown.CODE:
    return TextNode(markdown_text, TextType.CODE)

  if markdown_type == TextTypeMarkdown.HEADING:
    return TextNode(markdown_text, TextType.HEADING)

  if markdown_type == TextTypeMarkdown.LINK:
    return TextNode(markdown_text, TextType.LINK)
  
  if markdown_type == TextTypeMarkdown.IMAGE:
    return TextNode(markdown_text, TextType.IMAGE)

  if markdown_type == TextTypeMarkdown.ITALICS:
    return TextNode(markdown_text, TextType.ITALIC)

  if markdown_type == TextTypeMarkdown.BOLD:
    return TextNode(markdown_text, TextType.BOLD)
  
  if markdown_type == TextTypeMarkdown.UNORDERED_LIST_ITEM:
    return TextNode(markdown_text, TextType.UNORDERED_LIST_ITEM)
  
  if markdown_type == TextTypeMarkdown.ORDERED_LIST_ITEM:
    return TextNode(markdown_text, TextType.ORDERED_LIST_ITEM)
   
  return TextNode(markdown_text, TextType.TEXT)


def text_node_to_html_node(text_node):
  match(text_node.text_type):
    case TextType.TEXT:
      return LeafNode("p", text_node.text)
    case TextType.HEADING:
      return LeafNode("h1", text_node.text)
    case TextType.BOLD:
      return LeafNode("b", text_node.text)
    case TextType.ITALIC:
      return LeafNode("i", text_node.text)
    case TextType.CODE:
      return LeafNode("code", text_node.text)
    case TextType.UNORDERED_LIST_ITEM:
      return LeafNode("li", text_node.text)
    case TextType.ORDERED_LIST_ITEM:
      return LeafNode("li", text_node.text)
    case TextType.LINK:
      return LeafNode("a", text_node.text, {"href": text_node.url})
    case TextType.IMAGE:
      return LeafNode("img", text_node.text, {"src": text_node.url, "alt": text_node.text})
    case _:
      raise ValueError(f"Invalid text type: {text_node.text_type}")

# <img src='https://boot.dev' alt='bootdev'/>
# <h1>Miguel<h1/>
# <h6>Miguel<h6/>

# # Miguel
# ###### Miguel


# def mark_down_type_to_html_node(block_type, block):
#   if block_type == TextTypeMarkdown.CODE:
#     block.
