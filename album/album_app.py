from flask import Blueprint, render_template, flash, request

from flask_login import current_user
from flask_uploads import UploadSet, IMAGES

from album.database import Album

album_bp = Blueprint('album', '__name__')
uploaded_images = UploadSet('photos', IMAGES)

@album_bp.route('/')
def index():
    list_of_albums = current_user.albums 

    print(list_of_albums)
    print(current_user.id)
    return render_template('home.html', user=current_user, albums = list_of_albums)



@album_bp.route('/upload', methods=['POST', 'GET'])
def test_upload():
    current_album = 3
    if request.method == 'POST':
        print(request.files['photo'])
        file_path = uploaded_images.save(request.files['photo'], f"{current_user.id}/{current_album}")
        
        return render_template('upload_form.html')
    return render_template('upload_form.html')


