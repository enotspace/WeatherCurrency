from settings import *

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    views = db.Column(db.Integer, default=0)
    title = db.Column(db.String(50), nullable=True)
    text = db.Column(db.Text(300), nullable=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    def __repr__(self):
        return '<Article%r>' % self.id