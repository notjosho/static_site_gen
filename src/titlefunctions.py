from directories import create_dir_copy, create_file_add_text, create_public_dir
from helperfunctions import extract_title, markdown_to_html_node
import re

def generate_page(from_path, template_path, dest_path):
  from_path_str = ""
  with open(from_path, 'r') as file:
    contents = file.read()
    from_path_str = contents

  template_path_str = ""
  with open(template_path, 'r') as file:
    contents = file.read()
    template_path_str = contents

  # fix this so it returns an html_node and a .to_html()
  html_content = markdown_to_html_node(from_path_str)

  page_title = extract_title(from_path_str)

  template_replaced_title = template_path_str.replace("{{ Title }}", page_title)
  template_replaced_content = template_replaced_title.replace("{{ Content }}", html_content)
  # copy the html to a file, idk what file yet

  create_public_dir()
  create_file_add_text('index.html', './public', template_replaced_content)

  # create_dir_copy(from_path, dest_path)
