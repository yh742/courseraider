import datetime

from app import logger, db
from ..models import Class, Performance, Question

class Db2json(object):

    def get_question(self, cls_id):

        cls = Class.query.get(cls_id)
        if cls == None:
            return None
        data = {}
        data['class_id'] = cls_id
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
            if not question.extra == None:
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
        if not Class.query.get(self.class_id) == None:
            logger.info("inserting class: class id already exists")
            query_obj = Class.query.get(self.class_id)
            db.session.delete(query_obj)
            db.session.commit()

        # create new entries
        cls = Class(id=self.class_id, date=self.time, title=self.title, description=self.description)
        db.session.add(cls)
        db.session.commit()

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
            qnum = idx
            widget = self.data['ui_schema'][key]['ui:widget']
            title = self.data['form_schema']['properties'][key]['title']
            jtype = self.data['form_schema']['properties'][key]['type']
            extra = ','.join(self.data['form_schema']['properties'][key]['enum']) \
                if 'enum' in self.data['form_schema']['properties'][key] \
                else ""
            question = Question(qnum=idx, widget=widget, jtype=jtype, title=title, extra=extra)
            Class.query.get(self.class_id).questions.append(question)
            db.session.add(question)
            db.session.commit()
            idx += 1




