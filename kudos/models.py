from kudos import db

options_feedback = db.Table('feedback_options',
                            db.Column('feedback_id', db.Integer, db.ForeignKey('feedback.id')),
                            db.Column('option_id', db.Integer, db.ForeignKey('option.id')))


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(1000))
    votes = db.relationship('Vote', backref='feedback')
    options = db.relationship('Option', secondary=options_feedback, backref=db.backref('feedbacks', lazy='dynamic'))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'options': [option.serialize() for option in self.options],
            'votes': [vote.serialize() for vote in self.votes]
        }

    def __init__(self, name, options=[], description=None):
        self.name = name
        self.options = options
        self.description = description

    def __repr__(self):
        return '<Feedback {}>'.format(self.name)


class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    feedback_id = db.Column(db.Integer, db.ForeignKey('feedback.id'))
    option = db.Column(db.String(50))
    text = db.Column(db.String(250))

    def serialize(self):
        return {
            'option': self.option
        }

    def __init__(self, feedback_id, option, text=None):
        self.feedback_id = feedback_id
        self.option = option
        self.text = text

    def __repr__(self):
        return '<Vote {}>'.format(self.option)


class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    feedback_id = db.Column(db.Integer, db.ForeignKey('option_set.id'))
    description = db.Column(db.String(50), unique=True)

    def serialize(self):
        return {
            'id': self.id,
            'description': self.description
        }

    def __init__(self, description):
        self.description = description

    def __repr__(self):
        return '<Option {}>'.format(self.description)


class OptionSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    options = db.relationship('Option')

    def __init__(self, name, options):
        self.name = name
        self.options = options

    def __repr__(self):
        return '<OptionSet {}>'.format(self.name)
