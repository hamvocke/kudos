from kudos import db, app
from kudos import models


def init_db():
    options = models.Option.query.all()
    if len(options) == 0:
        app.logger.debug("create seed data")
        like = models.Option(':)')
        dislike = models.Option(':(')
        emoticons = models.OptionSet("Emoticons", [like, dislike])
        db.session.add(like)
        db.session.add(dislike)
        db.session.add(emoticons)
        db.session.commit()
