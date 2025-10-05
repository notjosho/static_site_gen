import os
import shutil

PUBLIC_PATH = './public'
STATIC_PATH = './src/static'

def create_public_dir():
	create_dir_copy(PUBLIC_PATH, STATIC_PATH)

def copy_directory_to_path(path, destination_path):
	for file in os.listdir(path):
		full_path = os.path.join(path, file)
		full_path_dest = os.path.join(destination_path, file)

		if os.path.isfile(full_path):
			shutil.copy(full_path, full_path_dest)
			print(f"copied file: {full_path_dest}")
			return

		os.mkdir(full_path_dest)
		print(f"copied dir: {full_path_dest}")
		copy_directory_to_path(full_path, full_path_dest)

def create_dir_copy(from_path, dest_path):
	if os.path.exists(from_path):
		print(f"{from_path} dir found")
		print(f"deleting {from_path}...")
		shutil.rmtree(f"{from_path}/")
		print(f"{from_path} deleted successfully")

	print("creating public dir...")
	os.mkdir(from_path)
	print(f"{from_path} dir created")
	print(f"copying directories and files from {from_path} to {dest_path}...")
	copy_directory_to_path(dest_path, from_path)
	print(f"files copied successfully")

def create_file_add_text(file_name, path, text):
	file_path = os.path.join(path, file_name)
	if os.path.exists(file_path):
		print(f"{file_path} dir found")
		print(f"deleting {file_path}...")
		os.remove(file_path)
		print(f"{file_path} deleted successfully")

	print(f"creating file to {path}...")

	with open(file_path, 'w') as file:
		file.write(text)

	print(f"file created successfully")
