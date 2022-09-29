from email.policy import default
import os
from flask import Blueprint, render_template, flash, request, redirect, url_for, jsonify, current_app
from flask_login import current_user, login_required, login_manager
from flask_uploads import UploadSet, IMAGES

from album.database import Album, Photo, db, User, Comment
from album.forms import AlbumForm, PhotoForm, CommentForm, ProfileForm

album_bp = Blueprint("album", "__name__")
uploaded_images = UploadSet("photos", IMAGES)


@album_bp.route("/")
def index():
    form = AlbumForm(request.form)
    if current_user.is_authenticated:
        albums = current_user.albums
        return render_template("home.html", user=current_user, albums=albums, form=form)
    else:
        return render_template("home.html", user=current_user, albums=None, form=form)

       
@album_bp.route('/<int:user_id>/albums', methods=['POST',])
@login_required
def add_album(user_id):
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
    "/<int:user_id>/albums",
    methods=[
        "GET",
    ],
)
def view_albums(user_id):
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


@album_bp.route('/<int:user_id>/albums/<string:album_name>', methods=['DELETE',])
@login_required
def delete_album(user_id,album_name):
    if current_user.id == user_id:
        album = current_user.albums.filter_by(name=album_name).first()
        db.session.delete(album)
        db.session.commit()
        return '', 204

    else :
        return current_app.login_manager.unauthorized() 

@album_bp.route('/<int:user_id>/albums/<string:album_name>', methods=['GET' ])
def view_album(user_id,album_name):
    form = PhotoForm(request.form )
    if current_user.is_authenticated and current_user.id == user_id:
        album = current_user.albums.filter_by(name=album_name).first_or_404()
        photos = album.photos
        path = 'users/'  + str(current_user.id) + '/' + str(album.name)
        return render_template('photos.html', current_user=current_user, user=current_user, photos=photos, path=path, form = form,album_name = album_name, album=album)

    else:
        user = User.query.get_or_404(user_id)
        album = user.albums.filter_by(name=album_name).first_or_404()
        if album.public:
            photos = album.photos.filter_by(public=True).all()
            path = 'users/'  + str(user.id) + '/' + str(album.name)
            return render_template('photos.html', current_user=current_user, user=user, photos=photos, path=path, form = form,album_name = album_name, album=album)
        else:
            return current_app.login_manager.unauthorized()
        

@album_bp.route('/<int:user_id>/albums/<string:album_name>', methods=['POST'])
@login_required
def add_photo(user_id, album_name):
    album = current_user.albums.filter_by(name=album_name).first_or_404()
    file_path = uploaded_images.save(
        request.files["photo"], f"{current_user.id}/{album_name}"
    )
    file_name = os.path.basename(file_path)
    size = 0
    if album.public == True:
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
            public = False
        )

    db.session.add(photo)
    db.session.commit()
    flash(f"{file_name} added successfully")
    return redirect(
        url_for("album.view_album", user_id=user_id, album_name=album_name)
    )

    
@album_bp.route('/<int:user_id>/albums/<string:album_name>/<string:photo_name>')
def view_photo(user_id,album_name,photo_name):
    photo = None
    if current_user.is_authenticated and current_user.id == user_id :
        album = current_user.albums.filter_by(name=album_name).first_or_404()
        photo = album.photos.filter_by(name = photo_name, album_id=album.id).first_or_404()
        path = 'users/'  + str(current_user.id) + '/' + str(album.name) 
        return render_template('photo.html',photo = photo, current_user=current_user, user = current_user, path = path, album_name=album_name)
    else:
        user = User.query.get_or_404(user_id)
        album = user.albums.filter_by(name=album_name).first_or_404()
        if album.public:
            photo = Photo.query.filter_by(name = photo_name, album_id=album.id).first_or_404()
            if photo.public:
                path = 'users/'  + str(user.id) + '/' + str(album.name) 
                return render_template('photo.html',photo = photo, current_user=current_user, user=user, path=path, description = photo.description, album_name=album_name)
            else:
                return current_app.login_manager.unauthorized()
        else: 
            return current_app.login_manager.unauthorized()


@album_bp.route('/<int:user_id>/albums/<string:album_name>/<string:photo_name>', methods=['DELETE',])
@login_required
def delete_photo(user_id,album_name,photo_name):
    if current_user.id == user_id:
        album = current_user.albums.filter_by(name=album_name).first_or_404()
        photo = album.photos.filter_by(name = photo_name).first()
        db.session.delete(photo)
        db.session.commit()
        return jsonify({'status': 'deleted successfully'}), 204
    else:
        return current_app.login_manager.unauthorized()


@album_bp.route('/<int:user_id>/albums/<string:album_name>/<string:photo_name>', methods=['PUT',])
def update_photo(user_id,album_name,photo_name):
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
        db.session.commit()
        return jsonify({"likes": photo.likes})
    else:
        return current_app.login_manager.unauthorized()


@album_bp.route('/<int:user_id>/albums/<string:album_name>', methods=['PUT',])
def update_album(user_id, album_name):
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


@album_bp.route('/<int:user_id>/albums/<string:album_name>/<string:photo_name>/comment', methods= ['POST',])
def add_comment(user_id, album_name, photo_name):
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
        return jsonify(comment.as_dict())
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
        return jsonify(comment.as_dict())


@album_bp.route('/settings', methods=['POST'])
@login_required
def update_profile():
    if current_user.is_authenticated:
        form = ProfileForm(request.form)
        print(form)
        if form.validate():  
            path_ex=os.path.exists(f"album/static/users/{current_user.id}/profileavtar.jpg")
            path_join=os.path.join(f"album/static/users/{current_user.id}","profileavtar.jpg")
            # print(path_join,"///////////////")
            if path_ex:
                profile_pic_path=path_join
                os.remove(profile_pic_path)
                file_path = uploaded_images.save(
                request.files["photo"], f"{current_user.id}",
                name="profileavtar.jpg"
                )
                photo_name = os.path.basename('users/'+file_path)
                print(photo_name)
                print(file_path)
            else:
                if "photo" in request.files:
                    print(",,./,/.,./,/,./,/")
                file_path = uploaded_images.save(
                request.files["photo"], f"{current_user.id}",
                name="profileavtar.jpg"
                )
                photo_name = os.path.basename('users/'+file_path)
                # print(photo_name)
                # print(file_path)
            # print(profile_pic_path)
            current_user.fname = form.fname.data
            current_user.lname = form.lname.data
            current_user.bio = form.bio.data
            db.session.commit()
            print("user updated successfully")
            return redirect('settings' )
        else:
            
            print(form.errors)
            return redirect('settings' )
    else:
        return current_app.login_manager.unauthorized()

@album_bp.route('/settings', methods=['GET'])
@login_required
def get_settings():
    form = ProfileForm(request.form)
    # print(url_for("static",filename=f"users/{current_user.id}/profileavtar.jpg"))
    c_path=os.getcwd()
    print(c_path)
    path_join=os.path.join(f"album/static/users/{current_user.id}","profileavtar.jpg")
    path_ex=os.path.exists(f"album/static/users/{current_user.id}/profileavtar.jpg")
    # print(path_ex,"path_ex")
    # print(path_join,"path_join")
    if path_ex:
        
        # print("======",path_ex)
        profile_pic_path=(url_for("static",filename=f"users/{current_user.id}/profileavtar.jpg"))
        return render_template('settings.html',form = form,profile_pic_path=profile_pic_path)
    else:
        c_path=os.getcwd()
        # print(c_path,"pppppppppp")
        profile_pic_path = "static/logos/profileavatar.jpg"
        return render_template('settings.html',form = form, profile_pic_path=profile_pic_path)
