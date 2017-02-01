from kudos import db, app
from kudos import models
from faker import Factory

fake = Factory.create(locale='de_DE')


def init_db():
    app.logger.debug("create seed data")
    like = models.Option(':)')
    dislike = models.Option(':(')
    emoticons = models.OptionSet("Emoticons", [like, dislike])

    db.session.add(like)
    db.session.add(dislike)
    db.session.add(emoticons)

    for _ in range(0, 15):
        feedback = models.Feedback(' '.join(fake.words(nb=3)), emoticons.options, fake.sentence(),
                                   ends_at=fake.date_time_between(start_date="-5d", end_date="+5d", tzinfo=None))
        db.session.add(feedback)
    db.session.commit()
