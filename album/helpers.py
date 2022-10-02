import json
import os

from flask import url_for

from album.database import User, Album, Comment, Photo


def profile_pic_exists(id_):
    profile_pic_path = os.path.join('album', 'static', 'users', str(id_), 'profileavatar.jpg')
    return os.path.exists(profile_pic_path)


def get_profile_pic_path(user):
    if not user:
        return url_for('static', filename='logos/profileavatar.jpg')
    if not profile_pic_exists(user.id):
        return url_for('static', filename='logos/profileavatar.jpg')
    return url_for('static', filename=f'users/{user.id}/profileavatar.jpg')


def parse_id_from_slug(slug: str) -> int:
    '''get id from slug'''
    try:
        return int(slug.split('-')[-1])
    except Exception as e:
        print(e)
        return 0


def format_notification(notification, current_user):
    details = json.loads(notification.details)
    if details['type'] == 'like':
        notified_user = User.query.get(details['who'])
        photo = Photo.query.get(details['type_id'])
        album = Album.query.get(photo.album_id)
        photo_url = url_for('album.view_photo', user_id=current_user.id, album_name=album.name, photo_name=photo.name)
        return dict(
            notification=f"{notified_user.fname} {notified_user.lname} reacted to your photo" if notified_user else 'guest user liked your photo',
            photo_url=photo_url,
        )

    if details['type'] == 'comment':
        notified_user = User.query.get(details['who'])
        comment = Comment.query.get(details['type_id'])
        photo = Photo.query.get(comment.photo_id)
        album = Album.query.get(photo.album_id)
        photo_url = url_for('album.view_photo', user_id=current_user.id, album_name=album.name, photo_name=photo.name)
        return dict(
            notification=f"{notified_user.fname} {notified_user.lname} commented on your photo" if notified_user else 'guest user commented on your photo',
            photo_url=photo_url
        )
