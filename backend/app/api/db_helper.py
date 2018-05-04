import datetime
from collections import Counter

from app import logger, db
from ..models import Class, Performance, Question


def activate(cls_id):

    cls = Class.query.get(cls_id)
    if cls is None:
        return False
    cls.active = True
    db.session.add(cls)
    db.session.commit()
    return True


def deactivate(cls_id):

    cls = Class.query.get(cls_id)
    if cls is None:
        return False
    cls.active = False
    db.session.add(cls)
    db.session.commit()
    return True


def delete_question(cls_id):

    cls = Class.query.get(cls_id)
    if cls is None:
        return False
    for question in cls.questions:
        for perf in question.performances:
            db.session.delete(perf)
        db.session.delete(question)
    db.session.delete(cls)
    db.session.commit()
    return True


def insert_performance(data):

    if data is None:
        return None
    for key in data:
        q = Question.query.get(int(key.replace('id-','')))
        p = Performance(score=str(data[key]))
        q.performances.append(p)
        db.session.commit()


def get_all_performance():

    data = {}
    data['classes'] = []
    for cls in Class.query.all():
        perf = get_performance(cls.id)
        if perf is None: 
            break
        data['classes'].append(perf)
    return data


def get_all_questions():
    data = {}
    data['questions'] = []
    for cls in Class.query.all():
        ques = get_question(cls.id)
        if ques is None:
            break
        data['questions'].append(ques)
    return data


def get_performance(cls_id):

    cls = Class.query.get(cls_id)
    if cls is None:
        return None
    data = dict()
    data['class_id'] = cls_id
    for question in cls.questions:
        key = 'question' + str(question.qnum)
        data[key] = dict()
        if question.widget == 'radio':
            scores = [int(x.score) for x in question.performances]
            if len(scores) == 0:
                return None
            avg = sum(scores) / float(len(scores))
            dist = dict(Counter(scores))
            data[key]['scores'] = scores
            data[key]['avg'] = avg
            data[key]['dist'] = dist
        elif question.widget == 'textarea':
            data[key]['text'] = [x.score for x in question.performances]
    return data


def check_activated(cls_id):

    obj = Class.query.get(cls_id)
    return obj.active


def get_question(cls_id):

    cls = Class.query.get(cls_id)
    if cls is None:
        return None
    data = dict()
    data['class_id'] = cls_id
    data['active'] = cls.active
    data['ui_schema'] = {}
    data['form_schema'] = {}
    data['form_schema']['title'] = cls.title
    data['form_schema']['description'] = cls.description
    data['form_schema']['type'] = 'object'
    data['form_schema']['properties'] = {}
    for question in cls.questions:
        key = 'Question' + str(question.qnum)
        data['ui_schema'][key] = {}
        data['ui_schema'][key]['ui:widget'] = question.widget
        data['form_schema']['properties'][key] = {}
        data['form_schema']['properties'][key]['type'] = question.jtype
        data['form_schema']['properties'][key]['title'] = question.title
        data['form_schema']['properties'][key]['id'] = str(question.id)
        if question.extra is not None:
            if ',' in question.extra:
                data['form_schema']['properties'][key]['enum'] = question.extra.split(',')
    return data


class Json2db(object):

    def __init__(self, json_data):

        self.data = json_data
        self.class_id = json_data['class_id']
        self.time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.title = json_data['form_schema']['title']
        self.description = json_data['form_schema']['description']
        logger.info('in __init__  {0}, {1}, {2}, {3}'.
                    format(self.class_id, self.time, self.title, self.description))

    def insert_cls(self):

        # delete any previous entries
        if not Class.query.get(self.class_id) is None:
            logger.info("inserting class: class id already exists")
            query_obj = Class.query.get(self.class_id)
            db.session.delete(query_obj)
            db.session.commit()

        # create new entries
        cls = Class(id=self.class_id, date=self.time, title=self.title, description=self.description)
        db.session.add(cls)
        db.session.commit()
        return self

    def insert_question(self):

        # delete previous entries, look for orphaned entries too (marked NULL)
        if not Question.query.filter_by(class_id=self.class_id).all() == [] or \
                not Question.query.filter_by(class_id=None).all() == []:
            logger.info('inserting question: class id already exists')
            query_obj = Question.query.filter_by(class_id=None).all()
            for obj in query_obj:
                db.session.delete(obj)
            db.session.commit()

        idx = 1
        while True:
            key = 'Question' + str(idx)
            if key not in self.data['ui_schema']:
                break
            widget = self.data['ui_schema'][key]['ui:widget']
            title = self.data['form_schema']['properties'][key]['title']
            jtype = self.data['form_schema']['properties'][key]['type']
            extra = ','.join(self.data['form_schema']['properties'][key]['enum']) \
                if 'enum' in self.data['form_schema']['properties'][key] \
                else ""
            question = Question(qnum=idx, widget=widget, jtype=jtype, title=title, extra=extra)
            Class.query.get(self.class_id).questions.append(question)
            #db.session.add(question)
            db.session.commit()
            idx += 1
        return self





