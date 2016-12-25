from kudos import db

class FeedbackRound(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<FeedbackRound {}>'.format(self.name)
