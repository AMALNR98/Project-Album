import os
from flask import Blueprint, render_template, flash, request, url_for

from flask import Blueprint, render_template, flash, request, redirect
from flask_login import current_user
from flask_uploads import UploadSet, IMAGES
from flask_login import login_required

from album.database import Album, Photo, db, User
from album.forms import AlbumForm

album_bp = Blueprint('album', '__name__')
uploaded_images = UploadSet('photos', IMAGES)

@album_bp.route('/')
def index():
    form = AlbumForm(request.form)
    albums = current_user.albums 
    return render_template('home.html', user=current_user, albums = albums, form=form)



       
@album_bp.route('/<int:user_id>/albums', methods=['POST',])
@login_required
def add_album(user_id):
    form = AlbumForm(request.form)
    if form.validate():
        if form.status == "Public":
            public = True
        else:
            public = False
        album = Album(name=form.name.data, description=form.description.data, user_id=current_user.id, public = public)
        db.session.add(album)
        db.session.commit()
        flash("album added successfully")
    return redirect(url_for('album.index'))


@album_bp.route('/<int:user_id>/albums', methods=['GET',])
def view_albums(user_id):
    if current_user.is_authenticated and current_user.id == user_id:
        albums = current_user.albums
        return render_template('albums.html', user=current_user, albums=albums)
    else:
        user = User.query.get(user_id)
        if user:
            albums = user.filter_by(public=True)
            return render_template('albums.html', user=user, albums=albums)
        else:
            return render_template('404.html')

    

@album_bp.route('/<int:user_id>/albums/<string:album_name>/photos', methods=['GET' ])
def view_album(user_id,album_name):
    if current_user.is_authenticated and current_user.id == user_id:
        album = current_user.albums.filter_by(name=album_name).first()
        if album:
            photos = album.photos
            path = 'users/'  + str(current_user.id) + '/' + str(album.name)
            return render_template('photos.html', user=current_user, photos=photos, path=path)
        else:
            return render_template('404.html'), 404
        
    else:
        user = User.query.get(user_id)
        album = user.album.filter_by(name=album_name).first()
        if album:
            if album.public:
                photos = album.photos.filter_by(public=True)
                path = 'users/'  + str(current_user.id) + '/' + str(album.name)
            else:
                flash ('this is a private album')
                photos = []
                path = None
        else:
            return render_template('404.html'), 404
            
 





@album_bp.route('/<int:user_id>/albums/<string:album_name>/photos', methods=['POST'])
@login_required
def add_photo(user_id, album_name):
    album = current_user.albums.filter_by(name=album_name).first()
    if album:
        file_path = uploaded_images.save(request.files['photo'], f"{current_user.id}/{album_name}")
        file_name = os.path.basename(file_path)
        size = 0
        photo = Photo(name=file_name, size=size, album_id=album.id)
        db.session.add(photo)
        db.session.commit()
        flash(f"{file_name} added successfully")
        return redirect(url_for('album.view_album', user_id=user_id, album_name=album_name))
    else:
        return render_template('404.html'), 404



@album_bp.route('/add_photo')
def test_upload():
    return render_template('upload_form.html', user_id=1, album_name="cooking")
