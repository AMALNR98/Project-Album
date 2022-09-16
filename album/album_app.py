import logging
import os
from unicodedata import name
from flask import Blueprint, render_template, flash, request

from flask import Blueprint, render_template, flash, request, redirect
from flask_login import current_user
from flask_uploads import UploadSet, IMAGES
from flask_login import login_required

from album.database import Album, Photo, User, db

album_bp = Blueprint('album', '__name__')
uploaded_images = UploadSet('photos', IMAGES)

@album_bp.route('/')
def index():
    list_of_albums = current_user.albums 
    # print(list_of_albums)
    # print(current_user.id)
    return render_template('home.html', user=current_user, albums = list_of_albums)



@album_bp.route('/upload', methods=['POST', 'GET'])
def test_upload():
    current_album = 4
    if request.method == 'POST':
        # print(request.files['photo'])
        file_path = uploaded_images.save(request.files['photo'], f"{current_user.id}/{current_album}")
        
        return render_template('upload_form.html')
    return render_template('upload_form.html')

# @album_bp.route('/<string:album_name>')
# def album(album_name):
#     # list_of_photos = Photo.query.filter_by(name = album_name).all()
#     album = current_user.albums.filter_by(name=album_name).first()
#     if album == None:
#         flash("Nothing to diplay")
#         photos = []
#     else:
#         photos = album.photos
#     path = 'users/'  + str(current_user.id) + '/' + str(album.name)
#     return render_template('photos.html',user=current_user, photos = photos,  path=path)


@album_bp.route('/<int:user_id>/<string:album_name>')
def album(user_id,album_name):
    if current_user.is_authenticated:
        if current_user.id == user_id:
            album = current_user.albums.filter_by(name=album_name).first()
            if album:
                photos = album.photos
                path = 'users/'  + str(current_user.id) + '/' + str(album.name)
            else:
                flash ('no such album')
                path = None
                return '404'
            return render_template('photos.html', user=current_user, photos=photos, path=path)
        else:
            album = current_user.album.filter_by(name=album_name).first()
            if album:
                if album.public:
                    photos = album.photos
                    path = 'users/'  + str(current_user.id) + '/' + str(album.name)
                else:
                    flash ('this is a private album')
                    photos = []
                    path = None
            else:
                photos = []
                flash("no such album")
                path = None
            return render_template('photos.html', user=current_user, photos=photos)


@album_bp.route('/add_album', methods=['POST', 'GET'])
@login_required
def add_album():
    if request.method == 'POST':
        album_name = request.form.get('name')
        description = request.form.get('description')
        album = Album(name=album_name, description=description, user_id=current_user.id)
        db.session.add(album)
        db.session.commit()
        flash("album added successfully")
    return render_template('add_album.html', user=current_user)


@album_bp.route('/<string:album_name>/add_photo', methods=['POST', 'GET'])
@login_required
def add_photo(album_name):
    if request.method == 'POST':
        album = current_user.albums.filter_by(name=album_name).first()
        if album:
            file_path = uploaded_images.save(request.files['photo'], f"{current_user.id}/{album_name}")
            file_name = os.path.basename(file_path)
            size = 0
            photo = Photo(name=file_name, size=size, album_id=album.id)
            db.session.add(photo)
            db.session.commit()
        else:
            flash("no such albums found")


    return render_template('add_photo.html', user=current_user)

# @album_bp.route('/<int:user_id>/<string:album_name>/<string:photo_name>')
# @login_required
# def view_photo(user_id, album_name,photo_name):
#     if current_user.is_authenticated:
#         album = current_user.albums.filter_by(name=album_name).first()
#         print(album.id)
#         photo = Photo.filter_by(name= photo_name).first()
#         print(photo.id)
#         return render_template('photo.html', user = current_user )

#     else:
#         flash("photo is private")        
#         return render_template('photo.html')
    
@album_bp.route('/<int:user_id>/<string:album_name>/photos/<string:photo_name>')
def view_photo(user_id,album_name,photo_name):
        photo = None
        print("user id =",user_id)
        # print(current_user)
        print("current_user.id",current_user.id)
        if current_user.is_authenticated and current_user.id == user_id :
            album = current_user.albums.filter_by(name=album_name).first()
            print(current_user)
            print(album.id)            
            photo = album.photos.filter_by(name = photo_name).first()
            path = 'users/'  + str(current_user.id) + '/' + str(album.name) 
            print('path =',path)
            print("photo.name=",photo.name)
            print("photo id =",photo.id)
            return render_template('photo.html',photo = photo,user = current_user, path = path)
        else:
            flash("photo is private")        
              
            return "text"
            # return render_template('photo.html', user = current_user , photo_name=photo.name)

        