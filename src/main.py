from helperfunctions import markdown_to_html_node
from helper_vars import markdown
from helper_text import markdown_text
import os

from directories import PUBLIC_PATH, create_public_dir
from src.titlefunctions import generate_page



def main():
  print(markdown_to_html_node(markdown_text))
  # create_public_dir()
  generate_page('./src/', './src/template.html', '')
  
if __name__ == '__main__':
  main()