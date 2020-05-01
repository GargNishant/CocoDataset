# CocoFormatter
Contains code which can come in handy when working with coco Dataset. To use this, no need to install COCO API. All work is doneby using basic packages. This repository is an ongoing Repository and new functionality will keep appearing

### File Information
1. CocoReader.py: By using paramters, we can extract annotations of 1 category which is already present in original JSON. This is very useful, when we want to train only 1 class from the COCO Dataset, like Person Detection, etc. A new Annotation file will be generated, which will have only records with given annotation Category. There are even options to skip 1st *n* records and take only first *m* records in consideration
2. CocoZip.py: This is mainly used to create a Zip file, after downloading all the images from the COCO Annotation JSON file. In the zip file the orginal Annotation file would be saved too

### Usage Examples
1. By using CocoReady.py, get the Person Category Annotation file. Either you can take all the annotations of Person category in one file, which would be very big or only take in chucks 1k Images. The chucks can be acheived using *skip* and *upper_bound* parameters.
2. After creating the sub annotation file, using the CocoZip.py create zip files and store in Google Drive. This way we do not need to donwload each and every time, espacially time saving when using Google Colab for training.

### TODO:
- [x] Push my Commits to GitHub
- [x] Update Readme for Explaination.
- [x] Usage Example
- [ ] New File, to combine different Category output from CocoReader.py or CcocZip.py
