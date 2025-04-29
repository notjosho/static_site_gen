from helperfunctions import markdown_to_html_node
from helper_vars import markdown
from helper_text import markdown_text
import os

from directories import PUBLIC_PATH, make_dir



def main():
  # Write a recursive function that copies all the contents from a source directory to a destination directory (in our case, static to public)
  # ----------It should first delete all the contents of the destination directory (public) to ensure that the copy is clean. 
  # It should copy all files and subdirectories, nested files, etc.
  # I recommend logging the path of each file you copy, so you can see what's happening as you run and debug your code.
  print(markdown_to_html_node(markdown_text))
  make_dir(PUBLIC_PATH)
  
if __name__ == '__main__':
  main()