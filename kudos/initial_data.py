import random

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
        feedback = models.Feedback(name=' '.join(fake.words(nb=3)),
                                   options=emoticons.options,
                                   description=fake.text(),
                                   ends_at=fake.date_time_between(start_date="-5d", end_date="+5d", tzinfo=None))

        db.session.add(feedback)
        db.session.commit()

        for __ in range(0, random.randint(0, 25)):
            vote = models.Vote(feedback_id=feedback.id,
                               option=feedback.options[random.randint(0, 1)].description,
                               text=fake.text())

            db.session.add(vote)

    db.session.commit()
