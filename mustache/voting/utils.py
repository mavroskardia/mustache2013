# utils.py
import os

from django.core.files import File
from PIL import Image
from io import BytesIO


def create_thumbnail_name(original_name):
	splits = os.path.splitext(os.path.split(original_name)[-1])
	return splits[0] + '_resized' + splits[1]

def create_thumbnail(image_file):
	'''Take a Django ImageField and return a new ImageField that contains a thumbnailed version'''

	fakefile = BytesIO()
	try:
		img = Image.open(image_file)
		img.thumbnail((200,200), Image.ANTIALIAS)
		img.save(fakefile, format=img.format)
	except:
		print(image_file)

	return File(fakefile)

