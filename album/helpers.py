import os

from flask import url_for


def profile_pic_exists(id_):
    profile_pic_path = os.path.join('album', 'static', 'users', str(id_), 'profileavatar.jpg')
    return os.path.exists(profile_pic_path)


def get_profile_pic_path(current_user):
    if not profile_pic_exists(current_user.id):
        return url_for('static', filename='logos/profileavatar.jpg')
    return url_for('static', filename=f'users/{current_user.id}/profileavatar.jpg')



