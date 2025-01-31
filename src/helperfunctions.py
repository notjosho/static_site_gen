import re
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
      total_lines_lst.append(lines_lst)
      lines_lst = []
      continue
    lines_lst.append(lines[i])
    if i == len(lines) - 1:
      total_lines_lst.append(lines_lst)

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
    return False, text_split
      
  return True, list_text

def match_text_regex_list(text, regex):
  text_split = text.split('\n')
  list_text = []  

  for inner_text in text_split:
    result = re.findall(regex, inner_text)
    if not result:
      return False, text_split
    list_text.append(result)

  return True, list_text

def block_to_block_type(text):
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
    return TextTypeMarkdown.UNORDERED_LIST, list_text_unordered_list
    
  [is_type_ordered_list, list_text_ordered_list] = match_ordered_list(text)
  if is_type_ordered_list:
    return TextTypeMarkdown.ORDERED_LIST, list_text_ordered_list

  return TextTypeMarkdown.PARAGRAPH, text.split('\n')

def markdown_to_html_node(markdown):
  blocks = markdown_to_blocks(markdown)
  for block in blocks:
    block_type = block_to_block_type(block)
    

# def mark_down_type_to_html_node(block_type, block):
#   if block_type == TextTypeMarkdown.CODE:
#     block.

