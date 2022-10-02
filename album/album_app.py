import os
import datetime

from flask import Blueprint, render_template, flash, request, redirect, url_for, jsonify, current_app
from flask_login import current_user, login_required
from flask_uploads import UploadSet, IMAGES

from album.database import Album, Photo, db, User, Comment, Notification
from album.forms import AlbumForm, PhotoForm, ProfileForm
from album.helpers import parse_id_from_slug, get_profile_pic_path
from album import helpers

album_bp = Blueprint("album", "__name__")
uploaded_images = UploadSet("photos", IMAGES)


@album_bp.route("/")
def index():
    form = AlbumForm(request.form)
    if current_user.is_authenticated:
        albums = current_user.albums
        return render_template("home.html", user=current_user, albums=albums, form=form)
    else:
        return render_template("guest_home.html", user=current_user, albums=None, form=form)

       
@album_bp.route('/<string:user_id>/albums', methods=['POST', ])
@login_required
def add_album(user_id):
    user_id = parse_id_from_slug(user_id)
    form = AlbumForm(request.form)
    if form.validate():
        if form.status.data == "Public":
            public = True
        else:
            public = False
        album = Album(
            name=form.name.data,
            description=form.description.data,
            user_id=current_user.id,
            public=public,
        )
        db.session.add(album)
        db.session.commit()
        flash("album added successfully")
    return redirect(url_for("album.index"))


@album_bp.route(
    "/<string:user_id>/albums",
    methods=[
        "GET",
    ],
)
def view_albums(user_id):
    user_id = parse_id_from_slug(user_id)
    form = AlbumForm(request.form)
    if current_user.is_authenticated and current_user.id == user_id:
        albums = current_user.albums
        return render_template(
            "albums.html",
            current_user=current_user,
            user=current_user,
            albums=albums,
            form=form,

        )
    else:
        user = User.query.get_or_404(user_id)
        albums = user.albums.filter_by(public=True).all()
        return render_template(
            "albums.html", current_user=current_user, user=user, albums=albums
        )


@album_bp.route('/<string:user_id>/albums/<string:album_name>', methods=['DELETE', ])
@login_required
def delete_album(user_id,album_name):
    user_id = parse_id_from_slug(user_id)
    if current_user.id == user_id:
        album = current_user.albums.filter_by(name=album_name).first()
        db.session.delete(album)
        db.session.commit()
        return '', 204

    else:
        return current_app.login_manager.unauthorized() 


@album_bp.route('/<string:user_id>/albums/<string:album_name>', methods=['GET', ])
def view_album(user_id, album_name):
    user_id = parse_id_from_slug(user_id)
    form = PhotoForm(request.form )
    if current_user.is_authenticated and current_user.id == user_id:
        album = current_user.albums.filter_by(name=album_name).first_or_404()
        photos = album.photos
        path = f'users/{current_user.id}/{album.name}'
        return render_template('photos.html',
                               current_user=current_user, user=current_user, photos=photos, path=path,
                               form=form, album_name=album_name, album=album)

    else:
        user = User.query.get_or_404(user_id)
        album = user.albums.filter_by(name=album_name).first_or_404()
        if album.public:
            photos = album.photos.filter_by(public=True).all()
            # path = 'users/'  + str(user.id) + '/' + str(album.name)
            path = f'users/{user.id}/{album.name}'
            return render_template('photos.html', current_user=current_user, user=user, photos=photos, path=path, form = form,album_name = album_name, album=album)
        else:
            return current_app.login_manager.unauthorized()
        

@album_bp.route('/<string:user_id>/albums/<string:album_name>', methods=['POST'])
@login_required
def add_photo(user_id, album_name):
    user_id = parse_id_from_slug(user_id)
    album = current_user.albums.filter_by(name=album_name).first_or_404()
    file_path = uploaded_images.save(
        request.files["photo"], f"{current_user.id}/{album_name}"
    )
    file_name = os.path.basename(file_path)
    size = 0

    if album.public:
        photo = Photo(
            name=file_name,
            size=size,
            album_id=album.id,
            description=request.form.get("description"),
            public = True
        )
    else:
        photo = Photo(
            name=file_name,
            size=size,
            album_id=album.id,
            description=request.form.get("description"),
            public=False
        )

    db.session.add(photo)
    db.session.commit()
    flash(f"{file_name} added successfully")
    return redirect(
        url_for("album.view_album", user_id=user_id, album_name=album_name)
    )

    
@album_bp.route('/<string:user_id>/albums/<string:album_name>/<string:photo_name>')
def view_photo(user_id, album_name, photo_name):
    user_id = parse_id_from_slug(user_id)
    photo = None
    if current_user.is_authenticated and current_user.id == user_id :
        album = current_user.albums.filter_by(name=album_name).first_or_404()
        photo = album.photos.filter_by(name=photo_name, album_id=album.id).first_or_404()
        # path = 'users/' + str(current_user.id) + '/' + str(album.name)
        path = os.path.join('users', str(current_user.id), album.name)
        return render_template('photo.html', photo=photo, current_user=current_user, user=current_user, path=path, album_name=album_name)
    else:
        user = User.query.get_or_404(user_id)
        album = user.albums.filter_by(name=album_name).first_or_404()
        if album.public:
            photo = Photo.query.filter_by(name=photo_name, album_id=album.id).first_or_404()
            if photo.public:
                # path = 'users/'  + str(user.id) + '/' + str(album.name)
                path = os.path.join('users', str(user.id), album.name)
                return render_template('photo.html', photo=photo, current_user=current_user, user=user, path=path, description = photo.description, album_name=album_name)
            else:
                return current_app.login_manager.unauthorized()
        else: 
            return current_app.login_manager.unauthorized()


@album_bp.route('/<string:user_id>/albums/<string:album_name>/<string:photo_name>', methods=['DELETE', ])
@login_required
def delete_photo(user_id, album_name, photo_name):
    user_id = parse_id_from_slug(user_id)
    if current_user.id == user_id:
        album = current_user.albums.filter_by(name=album_name).first_or_404()
        photo = album.photos.filter_by(name=photo_name).first()
        db.session.delete(photo)
        db.session.commit()
        return jsonify({'status': 'deleted successfully'}), 204
    else:
        return current_app.login_manager.unauthorized()


@album_bp.route('/<string:user_id>/albums/<string:album_name>/<string:photo_name>', methods=['PUT', ])
def update_photo(user_id, album_name, photo_name):
    user_id = parse_id_from_slug(user_id)
    json = request.get_json()
    if 'like' in json:
        user = User.query.get_or_404(user_id)
        album = user.albums.filter_by(name=album_name).first_or_404()
        photo = album.photos.filter_by(name=photo_name).first_or_404()
        if json['like']:
            photo.likes += 1
        else:
            photo.likes -= 1
            if photo.likes < 0:
                photo.likes = 0
        who_id = current_user.id if current_user.is_authenticated else None
        user.add_notification(notification_type='like', type_id=photo.id, who_id=who_id)
        db.session.commit()
        return jsonify({"likes": photo.likes})
    else:
        return current_app.login_manager.unauthorized()


@album_bp.route('/<string:user_id>/albums/<string:album_name>', methods=['PUT',])
def update_album(user_id, album_name):
    user_id = parse_id_from_slug(user_id)
    json = request.get_json()
    if current_user.is_authenticated and current_user.id == user_id:
        if 'publish' in json:
            user = User.query.get_or_404(user_id)
            album = user.albums.filter_by(name=album_name).first_or_404()
            album.public = True
            for photo in album.photos:
                photo.public = True
            db.session.commit()
            return jsonify({"status": "success"}), 204
    else:
        return current_app.login_manager.unauthorized()


@album_bp.route('/<string:user_id>/albums/<string:album_name>/<string:photo_name>/comment', methods=['POST', ])
def add_comment(user_id, album_name, photo_name):
    user_id = parse_id_from_slug(user_id)
    json = request.get_json()
    if current_user.is_authenticated: 
        user = User.query.get_or_404(user_id)
        album = user.albums.filter_by(name=album_name).first_or_404()
        photo = album.photos.filter_by(name=photo_name).first_or_404()
        comment = Comment(
            display_name=f"{current_user.fname} {current_user.lname}",
            photo_id=photo.id,
            user_id=current_user.id,
            comment=json['comment']
        )
        db.session.add(comment)
        db.session.commit()
        db.session.refresh(comment)
        who_id = current_user.id if current_user.is_authenticated else None
        user.add_notification(notification_type='comment', type_id=comment.id, who_id=who_id)
        resp_json = comment.as_dict()
        resp_json['pic'] = get_profile_pic_path(user)
        print(resp_json)
        return jsonify(resp_json)
    else:
        user = User.query.get_or_404(user_id)
        album = user.albums.filter_by(name=album_name).first_or_404()
        photo = album.photos.filter_by(name=photo_name).first_or_404()
        comment = Comment(
            display_name=f"anon",
            photo_id=photo.id,
            comment=json['comment']
        )
        db.session.add(comment)
        db.session.commit()
        db.session.refresh(comment)
        who_id = current_user.id if current_user.is_authenticated else None
        user.add_notification(notification_type='comment', type_id=comment.id, who_id=who_id)
        resp_json = comment.as_dict()
        resp_json['pic'] = get_profile_pic_path(None)
        return jsonify(resp_json)


@album_bp.route('/settings', methods=['POST'])
@login_required
def update_profile():
    form = ProfileForm(request.form)
    if form.validate():
        current_user.fname = form.fname.data
        current_user.lname = form.lname.data
        current_user.bio = form.bio.data
        current_user.public = form.public.data
        db.session.commit()
        current_app.logger.debug(f'update_profile: details updated successfully')
        if request.files['photo'].filename != "":
            default_pro_pic_path = os.path.join('album', 'static', 'users', str(current_user.id), 'profileavatar.jpg')
            if os.path.exists(default_pro_pic_path):
                os.remove(default_pro_pic_path)
            file_path = uploaded_images.save(
                request.files["photo"], f"{current_user.id}",
                name="profileavatar.jpg"
            )
        return redirect(url_for('album.get_settings'))


@album_bp.route('/settings', methods=['GET'])
@login_required
def get_settings():
    form = ProfileForm(request.form)
    return render_template('settings.html', form=form, )


@album_bp.route('/users', methods=['GET', ])
def get_public_users():
    query = request.args.get('q')
    users = User.query.filter(User.fname.like(f'%{query}%'), User.public==True).all()
    return jsonify(dict(users=[dict(name=f"{user.fname} {user.lname}", url=url_for('album.view_albums', user_id=user.id)) for user in users]))


@album_bp.route('/notifications', methods=['GET', ])
@login_required
def get_notifications():
    notifications = current_user.notifications.filter(Notification.timestamp > current_user.notification_last_read).all()
    current_user.notification_last_read = datetime.datetime.now()
    db.session.commit()
    return jsonify([helpers.format_notification(notification, current_user) for notification in notifications])
