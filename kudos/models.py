from kudos import db

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Feedback {}>'.format(self.name)
