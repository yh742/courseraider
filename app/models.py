from app import db


class Class(db.Model):
    """
    Create a table for Class
    """

    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True, nullable=False)
    title = db.Column(db.String(256), index=True)
    description = db.Column(db.String(256))
    questions = db.relationship('Question', backref='class', lazy='dynamic')
    performances = db.relationship('Performance', backref='class', lazy='dynamic')

    def __repr__(self):
        return '<Class: {0}>'.format(self.id)


class Performance(db.Model):
    """
    Create a table for Performance
    """

    __tablename__ = 'performances'
    id = db.Column(db.Integer, primary_key=True)
    score = db.column(db.Integer)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))

    def __repr__(self):
        return '<Performance: {0},{1},{2}>'.format(self.id, self.qnum, self.score)



class Question(db.Model):
    """
    Create a table for Questions
    """

    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    qnum = db.Column(db.Integer)
    widget = db.Column(db.String(128))
    jtype = db.Column(db.String(256))
    title = db.Column(db.String(1028))
    extra = db.Column(db.String(256))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    performances = db.relationship('Performance', backref='question', lazy='dynamic')
    # TODO Add answer field if necessary

    def __repr__(self):
        return '<Question: {0},{1},{2}>'.format(self.id, self.qnum, self.title)



