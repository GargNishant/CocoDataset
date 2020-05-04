import os
import json
import argparse
import cocoSaver

parser = argparse.ArgumentParser()
parser.add_argument("file_1",help="JSON File_1 name and path", type=str)
parser.add_argument("file_2",help="JSON File 2 name and path", type=str)
parser.add_argument("new_file",help="Name of the Merged JSON File including path",type=str)

args = parser.parse_args()


file_1 = open(args.file_1,'r')
root_1 = json.load(file_1)
file_1.close()

file_2 = open(args.file_2,'r')
root_2 = json.load(file_2)
file_2.close()


def mergeLicenses(root_1, root_2):
	"""
	Merges the Licences json of the 2 JSON objects, and returns the merged License JSON
	"""
	# license_1 = root_1['licenses']
	# license_2 = root_2['licenses']
	# final_id = []
	# dict_id = {}

	# for l1 in license_1:
	# 	final_id.append(l1['id'])
	# 	dict_id[l1['id']] = l1

	# for l2 in license_2:
	# 	final_id.append(l2['id'])
	# 	dict_id[l2['id']] = l2

	# final_id = list(set(final_id))
	# final_id.sort()

	# final_license = []
	# for id_ in final_id:
	# 	final_license.append(dict_id[id_])

	return mergeLists(root_1['licenses'], root_2['licenses'])

def mergeImages(root_1, root_2):
	return mergeLists(root_1['images'], root_2['images'])


def mergeAnnot(root_1, root_2):
	return mergeLists(root_1['annotations'], root_2['annotations'])

def mergeCategory(root_1,root_2):
	return mergeLists(root_1['categories'], root_2['categories'])

def mergeLists(list_1, list_2):
	final_id = []
	dict_id = {}

	for item in list_1:
		final_id.append(item['id'])
		dict_id[item['id']] = item

	for item in list_2:
		final_id.append(item['id'])
		dict_id[item['id']] = item

	final_id = list(set(final_id))
	final_id.sort()

	final_list = []
	for id_ in final_id:
		final_list.append(dict_id[id_])

	return final_list

cocoSaver.saveCocoFormat(root_1['info'], root_1['description'], mergeLicenses(root_1, root_2), mergeCategory(root_1, root_2), mergeImages(root_1,root_2), mergeAnnot(root_1,root_2), args.new_file)
root = {}
root['info'] = root_1['info']
root['description'] = root_1['description']
root['licenses'] = mergeLicenses(root_1, root_2)
root['images'] = mergeImages(root_1,root_2)
root['annotations'] = mergeAnnot(root_1,root_2)
root['categories'] = mergeCategory(root_1, root_2)