import timeago
import datetime

def fromnow(date):
        return timeago.format(date, datetime.datetime.now())



def add_filter(app):
    app.jinja_env.filters['fromnow'] = fromnow