import json
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("coco_file",help="Name of the Coco JSON File including path",type=str)
parser.add_argument("yolo_dir",help="Name of the YOLO directory including path. In this directory annotations and Classes file will be stored",type=str)
args = parser.parse_args()

coco_file = open(args.coco_file,"r")
root = json.load(coco_file)
coco_file.close()

def getClassYOLO(root):
	try:
		os.makedirs(args.yolo_dir)
	except:
		print("Yolo Dir exists")

	categories = root['categories']
	dict_id = {}
	index = 0
	file = open(args.yolo_dir+"obj.names","w")
	for cat in categories:
		if index >= 1:
			file.write("\n")
		dict_id[cat['id']] = index
		file.write(cat['name'])
		index += 1

	file.close()
	return dict_id

def changeAnnotCat(root, new_cat_id):
	annotations = root['annotations']
	for annot in annotations:
		annot['category_id'] = new_cat_id[annot['category_id']]
		annot.pop("segmentation",None)
		annot.pop('area',None)
		annot.pop('iscrowd',None)
		annot.pop("id",None)


def getNewImgAnnot(root):
	images = root['images']
	annotations = root['annotations']
	new_images = []
	for img in images:
		new_images.append(img)

	for img in new_images:
		img.pop('license',None)
		img.pop('coco_url',None)
		img.pop('date_captured',None)
		img.pop('flickr_url',None)

		list_annot = []
		for annot in annotations:
			if annot['image_id'] == img["id"]:
				list_annot.append(convertCOCOtoYOLO(img,annot))
		img['annotations'] = list_annot
		break
	return new_images


def convertCOCOtoYOLO(image,annot):
	width = image['width']
	height = image['height']
	cocoBBox = annot['bbox']
	
	yolo_height = cocoBBox[3]/height
	yolo_width = cocoBBox[2]/width
	x = (cocoBBox[0]+cocoBBox[2]/2) /width
	y = (cocoBBox[1]+cocoBBox[3]/2) /height

	return annot['category_id'], x, y, yolo_width, yolo_height

def saveYOLOAnnot(new_img):
	for img in new_img:
		try:
			images = img['annotations']
		except:
			print("Error found at", img)

		bboxes = []
		for annot_tuple in images:
			str_ = ""
			for value in annot_tuple:
				str_ += str(value)+" "
			bboxes.append(str_)

		file = open(args.yolo_dir+img['file_name'][:-3]+"txt",'w')
		for box in bboxes:
			file.write(box.strip())
			file.write("\n")
		file.close()

new_cat_id = getClassYOLO(root)
changeAnnotCat(root,new_cat_id)
new_img = getNewImgAnnot(root)
saveYOLOAnnot(new_img)