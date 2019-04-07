from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_

import datetime

from Models import Posting
from Models.InitDB import init_database

class DataProviderService:
    def __init__(self, engine):
        """
        :param engine: The engine route and login details
        :return: a new instance of DAL class
        :type engine: string
        """
        if not engine:
            raise ValueError("DB Engine string is not specified.")

        self.engine = engine
        db_engine = create_engine(engine)
        db_session = sessionmaker(bind=db_engine)
        self.session = db_session()


    def init_database(self):
        """
        Initialize database tables and relationships()
        :return: None
        """
        init_database(self.engine)


    def add_posting(self, date, job_title, company, city="", technologies="", job_type="", links=""):
        """
        :param date:
        :param job_title:
        :param company:
        :param city:
        :param technologies:
        :param job_type:
        :param links:
        :return: The id of the new Posting
        """
        new_posting = Posting(date=date,
                              job_title=job_title,
                              company=company,
                              city=city,
                              technologies=technologies,
                              job_type=job_type,
                              links=links)
        self.session.add(new_posting)
        self.session.commit()

        return new_posting.id

    def get_posting(self, id=None, serialize=False, job_title="", city="", technologies=""):
        """
        If the one or more parameters are defined then it looks up the postings with the given parameters,
        otherwise it loads all the postings
        :param id:
        :param serialize:
        :param job_title:
        :param city:
        :param technologies:
        :return: The posting or postings ordered by date
        """
        all_postings = []
        if id is None and job_title == "" and city == "" and technologies == "":
            all_postings = self.session.query(Posting).order_by(Posting.date).all()
        else:
            all_postings = self.session.query(Posting).filter(or_(Posting.id == id,
                                                                  Posting.job_title.like('%{}%'.format(job_title)),
                                                                  Posting.city.like('%{}%'.format(city)),
                                                                  Posting.technologies.like('%{}%'.format(technologies)))).all()
        if serialize:
            return [posting.serialize() for posting in all_postings]
        else:
            return all_postings

