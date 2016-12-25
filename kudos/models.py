from sqlalchemy import Column, Integer, String
from kudos.database import Base

class FeedbackRound(Base):
    __tablename__ = 'feedbackRound'
    id = Column(Integer, primary_key=True)
    title = Column(String(150))

    def __init__(self, title=None):
        self.tite = title

    def __repr__(self):
        return '<FeedbackRound {}>'.format(self.title)
