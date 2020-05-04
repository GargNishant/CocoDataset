import os
import json

def saveCocoFormat(info_json, description, licenses, categories, images, annotations, file_name):
	root = {}
	root['info'] = info_json
	root['description'] = description
	root['licenses'] = licenses
	root['images'] = images
	root['annotations'] = annotations

	if type(categories) == list:
		root['categories'] = categories
	else:
		cat_ = []
		cat_.append(categories)
		root['categories'] = cat_

	try:
		os.makedirs(os.path.dirname(file_name))
	except:
		print("Path Already Exists")

	file = open(file_name,'w')
	file.write(json.dumps(root))
	file.close()
