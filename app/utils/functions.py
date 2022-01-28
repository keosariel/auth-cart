from hashlib import md5
from time import localtime
from app.error_codes import ERRORS_DESCRIPTION

from flask import current_app
from werkzeug.utils import secure_filename
from PIL import Image
import os

def get_unique_filename():
	"""Generates a random string"""
	prefix = md5(str(localtime()).encode('utf-8')).hexdigest()
	return f"{prefix}_upload"

def save_image(file_obj, sub_dir=""):
    upload_folder = current_app.config.get("UPLOAD_FOLDER")
    
    if sub_dir:
        upload_folder = os.path.join(upload_folder, sub_dir)

    filename = get_unique_filename()
    _, f_ext = os.path.splitext(secure_filename(file_obj.filename))

    filename  = filename + f_ext
    file_path = os.path.join(upload_folder, filename) 
    img = Image.open(file_obj)
    img.save(file_path)

    return filename

def get_upload(filename, sub_dir=""):
	upload_folder = current_app.config.get("UPLOAD_FOLDER")
	if sub_dir:
		upload_folder = os.path.join(upload_folder, sub_dir)

	file_path = os.path.join(upload_folder, filename)

	return file_path

def JSONResponse(data=None, message=None, code=None, status=200):

	if not message and code:
		message = ERRORS_DESCRIPTION.get(code,"")

	if code or status not in [200, 201]:
		return {
			"code": code,
			"message": message,
			"status": status,
			"data":data
		}, status
	else:
		return data

def add_view(request, post, current_user):
	ip_addr = request.remote_addr

	if ip_addr:
		view = View.query.filter_by(
			ip_addr=ip_addr,
			post_id=post.id
		).first()

		if not view:
			view = View(
				ip_addr=ip_addr,
				user_id=current_user.id if current_user else None,
				post_id=post.id
			)

			view.save()
			view.set_public_id()

def get_public_id(unique_id):
	return md5(str(unique_id).encode("UTF-8")).hexdigest()

from app.models import View