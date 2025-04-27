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
  no_jump_lines_text = re.search(r'^\n*(.*?)\n*$', text, re.DOTALL).group(1)
  initial_text_node_lst = [TextNode(no_jump_lines_text, TextType.TEXT)]
  text_nodes = split_nodes_link(initial_text_node_lst)
  text_nodes_images = split_nodes_images(text_nodes)
  text_nodes_bold = split_nodes_delimiter(text_nodes_images, '**', TextType.BOLD)
  text_nodes_italic = split_nodes_delimiter(text_nodes_bold, '_', TextType.ITALIC)
  text_nodes_code = split_nodes_delimiter(text_nodes_italic, '`', TextType.CODE)
  return text_nodes_code

def markdown_to_blocks(markdown):
  lines = markdown.split('\n\n')
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
    if line != '' and line[0] == str(count) and line[1] == '.' and line[2] == ' ':
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

def matchHeader(text):
  result = re.search(r"^#{1,6}\s", text)
  headerNumber = len(result[0].strip())
  match headerNumber:
    case 2:
      return TextTypeMarkdown.HEADING_2
    case 3:
      return TextTypeMarkdown.HEADING_3
    case 4:
      return TextTypeMarkdown.HEADING_4
    case 5:
      return TextTypeMarkdown.HEADING_5
    case 6:
      return TextTypeMarkdown.HEADING_6
    case _: 
      return TextTypeMarkdown.HEADING
    


def block_to_block_type(text):
  matches_code_block = re.search(r"\n*```\n*(.*?)\n*```\n*", text, re.DOTALL)
  if matches_code_block:
    return TextTypeMarkdown.CODE_BLOCK, matches_code_block.group(1)
  
  [is_type_heading, list_text_heading] = match_text_regex_list(text, r"^#{1,6}\s(.*)")
  if is_type_heading:
    return matchHeader(text), list_text_heading

  
  [is_type_italics, list_text_italics] = match_text_regex_list(text, r"^_(.*)_$")
  if is_type_italics:
    return TextTypeMarkdown.ITALICS, list_text_italics

  [is_type_quote, list_text_quote] = match_text_regex_list(text, r"^\>(.*)")
  if is_type_quote:
    return TextTypeMarkdown.QUOTE, list_text_quote

  [is_type_unordered_list, list_text_unordered_list] = match_text_regex_list(text, r"^[-*]\s(.*)")
  if is_type_unordered_list:
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
    type = block_to_block_type(mark_down_text)
    blocks = markdown_to_blocks(mark_down_text)
    
    for text in blocks:
      text_cleanedup = block_to_block_type(text)
      tuple_block = (type[0], text_cleanedup[1])

      if type[0] == TextTypeMarkdown.ORDERED_LIST_ITEM:
        ordered_list_item_text = match_text_regex_list(text, r"^\d+\.\s(.*)")
        tuple_block = (type[0], ordered_list_item_text[1])

      list_blocks_text_nodes.append(markdown_to_text_node(tuple_block))




  # TODO: validate for unordered lists

  # TODO: convert to HTML Nodes
  return list_blocks_to_html_nodes(list_blocks_text_nodes)


def text_to_children(text):
  text_nodes = separate_text_based_on_markdown(text)
  nodes = []
  for text_node in text_nodes:
    temp_node = text_node
    if text_node.text_type != TextType.TEXT:
      temp_node = text_node_to_leaf_node(text_node)
    nodes.append(temp_node)
  if len(nodes) > 1:
    return nodes
  return None

def list_blocks_to_html_nodes(list_blocks_text_nodes):
  html_nodes = []
  html_node_parent = None
  list_counter = 0
  list_type_map = {
    TextType.UNORDERED_LIST_ITEM: 'ul',
    TextType.ORDERED_LIST_ITEM: 'ol'
  }
  
  for index, text_node in enumerate(list_blocks_text_nodes):
    current_type = text_node.text_type
    if current_type == TextType.CODE_BLOCK:
      html_nodes.append(factory_text_node_to_html_node(text_node, text_node))
      continue

    if current_type in list_type_map:
      if list_counter == 0:
        html_node_parent = HTMLNode()
        html_node_parent.tag = list_type_map[current_type]
        html_node_parent.children = []
        list_counter += 1
      ## TODO: refactor this with the below application :3
      children_nodes_list = text_to_children(text_node.text)
      html_node_parent.children.append(factory_text_node_to_html_node(text_node, children_nodes_list))
      if children_nodes_list:
        html_node_parent.value = None

      if (index + 1 < len(list_blocks_text_nodes) and
        list_blocks_text_nodes[index + 1].text_type != current_type):
        html_nodes.append(html_node_parent)
        html_node_parent = None
        list_counter = 0
      continue

    ## TODO: refactor this with the above application :3
    children_nodes = text_to_children(text_node.text)
    html_node = factory_text_node_to_html_node(text_node, children_nodes)

    if children_nodes:
      html_node.value = None

    html_nodes.append(html_node)




  


  return wrapper_html_nodes_to_tags(html_nodes)

def html_nodes_to_html_tags(node):

  if isinstance(node, TextNode):
    return node.text

  if node.children is None:
    return node.to_html()
  
  children_html = ''
  for child in node.children:
    children_html += html_nodes_to_html_tags(child)

  return f'<{node.tag}>{children_html}</{node.tag}>'

def wrapper_html_nodes_to_tags(html_nodes):
  tags = ''
  for node in html_nodes:
    tags += html_nodes_to_html_tags(node)

  return " ".join(f'<div>{tags}</div>'.strip().split('\n'))

def markdown_to_text_node_heading(markdown_tuple):
  [markdown_type, markdown_text] = markdown_tuple 
  
  match(markdown_type):
    case TextTypeMarkdown.HEADING:
      return TextNode(markdown_text, TextType.HEADING)
    case TextTypeMarkdown.HEADING_2:
      return TextNode(markdown_text, TextType.HEADING_2)
    case TextTypeMarkdown.HEADING_3:
      return TextNode(markdown_text, TextType.HEADING_3)
    case TextTypeMarkdown.HEADING_4:
      return TextNode(markdown_text, TextType.HEADING_4)
    case TextTypeMarkdown.HEADING_5:
      return TextNode(markdown_text, TextType.HEADING_5)
    case TextTypeMarkdown.HEADING_6:
      return TextNode(markdown_text, TextType.HEADING_6)
    case _:
      return None

def markdown_to_text_node(markdown_tuple):
  [markdown_type, markdown_text] = markdown_tuple 

  if markdown_type == TextTypeMarkdown.CODE:
    return TextNode(markdown_text, TextType.CODE)
  
  if markdown_type == TextTypeMarkdown.CODE_BLOCK:
    return TextNode(markdown_text, TextType.CODE_BLOCK)

  if markdown_to_text_node_heading(markdown_tuple):
    return markdown_to_text_node_heading(markdown_tuple)

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

def factory_text_node_to_html_node(text_node, children=None):
  if children is None:
    return text_node_to_leaf_node(text_node)
  return text_node_to_html_node(text_node, children)

def text_node_to_leaf_node(text_node):
  match(text_node.text_type):
    case TextType.TEXT:
      return LeafNode("p", text_node.text)
    case TextType.HEADING:
      return LeafNode("h1", text_node.text)
    case TextType.HEADING_2:
      return LeafNode("h2", text_node.text)
    case TextType.HEADING_3:
      return LeafNode("h3", text_node.text)
    case TextType.HEADING_4:
      return LeafNode("h4", text_node.text)
    case TextType.HEADING_5:
      return LeafNode("h5", text_node.text)
    case TextType.HEADING_6:
      return LeafNode("h6", text_node.text)
    case TextType.BOLD:
      return LeafNode("b", text_node.text)
    case TextType.ITALIC:
      return LeafNode("i", text_node.text)
    case TextType.CODE:
      return LeafNode("code", text_node.text)
    case TextType.CODE_BLOCK:
      return LeafNode("pre", text_node.text)
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

def text_node_to_html_node(text_node, children):
  match(text_node.text_type):
    case TextType.TEXT:
      return HTMLNode("p", text_node.text, children)
    case TextType.HEADING:
      return HTMLNode("h1", text_node.text, children)
    case TextType.BOLD:
      return HTMLNode("b", text_node.text, children)
    case TextType.ITALIC:
      return HTMLNode("i", text_node.text, children)
    case TextType.CODE:
      return HTMLNode("code", text_node.text, children)
    case TextType.CODE_BLOCK:
      return HTMLNode("pre", None, [LeafNode('code', children.text)])
    case TextType.UNORDERED_LIST_ITEM:
      return HTMLNode("li", text_node.text, children)
    case TextType.ORDERED_LIST_ITEM:
      return HTMLNode("li", text_node.text, children)
    case TextType.LINK:
      return HTMLNode("a", text_node.text, children, {"href": text_node.url})
    case TextType.IMAGE:
      return HTMLNode("img", text_node.text, children, {"src": text_node.url, "alt": text_node.text})
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
