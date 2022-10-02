import datetime

import timeago

from album.helpers import get_profile_pic_path
from album.database import User


def fromnow(date):
    return timeago.format(date, datetime.datetime.utcnow())


def photo(user):
    if type(user) == int:
        return get_profile_pic_path(User.query.get(user))
    return get_profile_pic_path(user)


def add_filter(app):
    app.jinja_env.filters["fromnow"] = fromnow
    app.jinja_env.filters["photo"] = photo
