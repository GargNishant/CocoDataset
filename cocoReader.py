
import argparse
import json


parser = argparse.ArgumentParser()
parser.add_argument("--file_name",help = "Name of the Annotation File including the path to the file",default='instances_val2017.json')
parser.add_argument("--new_file",help=" Name of the new file. The default path would be current directory", default = 'new_instances_val2017.json')
parser.add_argument("--category",help="Category to Filter. Default is 'person'",default='person')
parser.add_argument("--skip_first",help="Skip 1st given count of images in category",default=0,type=int)
parser.add_argument("--upper_bound",help = "Limit of Images in category",default = 99999999, type=int)

args = parser.parse_args()

file_name = args.file_name
CATEGORY = args.category
low_bound = args.skip_first
upper_bound = args.upper_bound
new_name = args.new_file


orig_file = open(file_name,'r')
root = json.load(orig_file)
info_json = root['info']
description = info_json['description']
licenses = root['licenses']
categories = root['categories']
images = root['images']
annotations = root['annotations']
orig_file.close()



def getCatJson(category, CATEGORY):
	for cat in category:
		if cat['name'] == CATEGORY:
			return cat


def getCatAnnot(cat_id, annotations, low_bound = 0, up_bound = 9999999):
	img_id = []
	for annot in annotations:
		if annot['category_id'] == cat_id:
			img_id.append(annot['image_id'])

	img_id = list(set(img_id))
	img_id = rmListEntry(img_id,low_bound,up_bound)

	cat_annot = []
	for annot in annotations:
		im_id = annot['image_id']
		if annot['category_id'] == cat_id and im_id in img_id and annot['iscrowd'] == 0:
			annot.pop("segmentation",None)
			cat_annot.append(annot)

	return cat_annot, img_id


def rmListEntry(entry_list,low_bound, up_bound):
	if type(entry_list) == list:
		count = 0
		new_ = []
		for entry in entry_list:
			if count >= up_bound:
				break
			if count < low_bound:
				count += 1
				continue
			new_.append(entry)
			count += 1
		return new_


def getImgForIds(img_id,images):
	img_list = []

	if type(img_id) == list:
		for img in images:
			if img['id'] in img_id:
				img_list.append(img)

	elif type(img_id) == int:
		for img in images:
			if img['id'] == img_id:
				img_list.append(img)

	return img_list


def saveCocoFormat(info_json, description, licenses, categories, images, annotations, file_name):
	root = {}
	root['info'] = info_json
	root['description'] = description
	root['licenses'] = licenses
	root['images'] = images
	root['annotations'] = annotations

	if type(categories) == list:
		root_dict['categories'] = categories
	else:
		cat_ = []
		cat_.append(categories)
		root['categories'] = cat_

	file = open(file_name,'w')
	file.write(json.dumps(root))
	file.close()

category = getCatJson(categories,CATEGORY)
cat_annot , img_id = getCatAnnot(category['id'],annotations,low_bound = low_bound, up_bound= upper_bound)
img_list = getImgForIds(img_id,images)
saveCocoFormat(info_json,description,licenses,category,img_list,cat_annot,new_name)