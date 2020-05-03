from zipfile import ZipFile
from os import path
import os
import shutil
import os.path
import requests
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("--file_name",help="Name of JSON File, including the Directory",default="instances_val2017.json")
parser.add_argument("--zip_name",help="Name of Zip File, including Directory", default="instances_val2017.zip")
parser.add_argument("--save_img_dir",help="Path of the Directory, where Images would be downloaded", default="images/")

args = parser.parse_args()


def get_all_file_paths(dir):
    # initializing empty file paths list 
    file_paths = []

    # crawling through directory and subdirectories 
    for root, directories, files in os.walk(dir): 
        for filename in files: 
            # join the two strings in order to form the full filepath. 
            filepath = os.path.join(root, filename) 
            file_paths.append(filepath)

    # returning all file paths 
    return file_paths



def zipdir(source_path, dest_path):
    """
    Creates a zip file with the given file_name from all the files in the given path. The zip file would be saved in current Directory

    @param path: Path of the Parent FOlder for which you want to convert to zip folder. All the sub directories will be included into the zip folder
    @param fileNanme: Name of the zip file that you want to the new file to be
    """
    try:
    	os.makedirs(os.path.dirname(dest_path))
    except:
    	print("Zip Path Already Exists")

    file_paths = get_all_file_paths(source_path)
    with ZipFile("new_.zip",'w') as zip:
        for file in file_paths:
            zip.write(file)
    shutil.move("new_.zip",dest_path)


def saveImg(json_file,save_dest):
	"""
	Downloads the images from the COCO Formatted JSON File, and saved them in the given destination folder
	@param json_file: Name of the JSON File including the Destination of the File
	@param save_dest: Path of the Destination Folder, where downloaded files would be saved 
	"""
	orig_file = open(json_file,'r')
	root = json.load(orig_file)
	images = root['images']
	orig_file.close()

	try:
		os.makedirs(save_dest)
	except:
		print("Image Path Exists")

	for img in images:
		img_data = requests.get(img['coco_url']).content
		with open(save_dest+img['file_name'],'wb') as handler:
			handler.write(img_data)

	shutil.move(json_file,save_dest)
	zipdir(save_dest,args.zip_name)

saveImg(args.file_name,args.save_img_dir)