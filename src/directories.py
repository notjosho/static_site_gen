import os
import shutil

PUBLIC_PATH = './public'
STATIC_PATH = './src/static'

def make_dir(path):
	if os.path.exists(path):
		print("public dir found")
		print(f"deleting {PUBLIC_PATH}...")
		shutil.rmtree(f"{PUBLIC_PATH}/")
		print(f"{PUBLIC_PATH} deleted successfully")
	print("creating public dir...")
	os.mkdir(path)
	print("public dir created")
	print(f"copying directories and files from {PUBLIC_PATH} to {STATIC_PATH}...")
	copy_directory_to_path(STATIC_PATH, PUBLIC_PATH)
	print(f"files copied successfully")

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
