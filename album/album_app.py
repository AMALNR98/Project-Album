import os
from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import current_user, login_required
from flask_uploads import UploadSet, IMAGES

from album.database import Album, Photo, db, User
from album.forms import AlbumForm, PhotoForm

album_bp = Blueprint('album', '__name__')
uploaded_images = UploadSet('photos', IMAGES)

@album_bp.route('/')
def index():
    form = AlbumForm(request.form)
    if current_user.is_authenticated:
        albums = current_user.albums
        return render_template('home.html', user=current_user, albums = albums, form=form)
    else:
        return render_template('home.html', user=current_user, albums = None, form=form)


@album_bp.route('/<int:user_id>/albums/<string:album_name>')
def album(user_id,album_name):
    if current_user.is_authenticated:
        form = PhotoForm(request.form)
        if current_user.id == user_id:
            album = current_user.albums.filter_by(name=album_name).first()
            if album:
                photos = album.photos
                path = 'users/'  + str(current_user.id) + '/' + str(album.name)
            else:
                flash ('no such album')
                path = None
                return '404',404
            return render_template('photos.html', current_user=current_user, user=current_user, photos=photos, path=path, form=form)
        else:
            album = current_user.album.filter_by(name=album_name).first()
            if album:
                if album.public:
                    photos = album.photos
                    path = 'users/'  + str(current_user.id) + '/' + str(album.name)
                    return render_template('photos.html', current_user=current_user,user=current_user, photos=photos)
                else:
                    photos = []
                    path = None
                    return '403', 403
            else:
                photos = []
                flash("no such album")
                path = None
                return '404', 404




       
@album_bp.route('/<int:user_id>/albums', methods=['POST',])
@login_required
def add_album(user_id):
    form = AlbumForm(request.form)
    if form.validate():
        print(form.status)
        if form.status.data == "Public":
            public = True
        else:
            public = False
        album = Album(name=form.name.data, description=form.description.data, user_id=current_user.id, public = public)
        db.session.add(album)
        db.session.commit()
        print('album added successfully')
        flash("album added successfully")
    return redirect(url_for('album.index'))


@album_bp.route('/<int:user_id>/albums', methods=['GET',])
def view_albums(user_id):
    form = AlbumForm(request.form)
    if current_user.is_authenticated and current_user.id == user_id:
        albums = current_user.albums
        return render_template('albums.html', current_user=current_user, user=current_user, albums=albums, form=form)

    else:
        user = User.query.get(user_id)
        if user:
            albums = user.albums.filter_by(public=True).all()
            return render_template('albums.html', current_user=current_user, user=user, albums=albums)
        else:
            return render_template('404.html')

@album_bp.route('/<int:user_id>/albums/<string:album_name>', methods=['GET' ])
def view_album(user_id,album_name):
    form = PhotoForm(request.form )
    if current_user.is_authenticated and current_user.id == user_id:
        album = current_user.albums.filter_by(name=album_name).first()
        if album:
            photos = album.photos
            path = 'users/'  + str(current_user.id) + '/' + str(album.name)
            return render_template('photos.html', current_user=current_user, user=current_user, photos=photos, path=path, form = form,album_name = album_name)
        else:
            return render_template('404.html'), 404
        
    else:
        user = User.query.get(user_id)
        if user:
            album = user.albums.filter_by(name=album_name).first()
            if album:
                if album.public:
                    photos = album.photos.filter_by(public=True).all()
                    path = 'users/'  + str(user.id) + '/' + str(album.name)
                    return render_template('photos.html', current_user=current_user, user=user, photos=photos, path=path, form = form,album_name = album_name)
                else:
                    flash ('this is a private album')
                    photos = []
                    path = None
                    return render_template('photos.html', current_user=current_user, user=user, photos=photos, path=path, form = form,album_name = album_name)
            else:
                return render_template('404.html'), 404
        else:
            return render_template('404.html')



@album_bp.route('/<int:user_id>/albums/<string:album_name>', methods=['POST'])
@login_required
def add_photo(user_id, album_name):
    album = current_user.albums.filter_by(name=album_name).first()
    if album:
        file_path = uploaded_images.save(request.files['photo'], f"{current_user.id}/{album_name}")
        file_name = os.path.basename(file_path)
        size = 0
        photo = Photo(name=file_name, size=size, album_id=album.id, description=request.form.get('description'))
        db.session.add(photo)
        db.session.commit()
        flash(f"{file_name} added successfully")
        return redirect(url_for('album.view_album', user_id=user_id, album_name=album_name))
    else:
        return render_template('404.html'), 404


@album_bp.route('/<int:user_id>/albums/<string:album_name>/<string:photo_name>')
def view_photo(user_id,album_name,photo_name):
        photo = None
        if current_user.is_authenticated and current_user.id == user_id :
            album = current_user.albums.filter_by(name=album_name).first()
            if album:           
                photo = album.photos.filter_by(name = photo_name).first()
                if photo:
                    path = 'users/'  + str(current_user.id) + '/' + str(album.name) 
                   
                    return render_template('photo.html',photo = photo, current_user=current_user, user = current_user, path = path, album_name=album_name)
                else:
                    return "photo not found"
            else:
                return "album not found"
        else:
            user = User.query.get(user_id)
            album = user.albums.filter_by(name=album_name).first()
            if album:
                if album.public:
                    photo = Photo.query.filter_by(name = photo.name)
                    if photo:
                        if photo.public:
                            path = 'users/'  + str(user.id) + '/' + str(album.name) 
                            return render_template('photo.html',photo = photo, current_user=current_user, user=user, path=path, description = photo.description)
                        else:
                            return '404', 404
                    else:
                        return "Photos is private"
                else: 
                    return '404', 404
            else:
                return '404', 404