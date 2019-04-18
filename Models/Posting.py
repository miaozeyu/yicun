
# id
# Date
# Job_Title
# City
# Technologies
# Job_Type
# Company
# Links

from Models.Model import Model
from sqlalchemy import Column, String, Date, Integer

class Posting(Model):
    __tablename__ = 'postings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    job_title = Column(String(100), nullable=False)
    company = Column(String(50), nullable=True)
    city = Column(String(50), nullable=True)
    technologies = Column(String(100), nullable=True)
    job_type = Column(String(20), nullable=True)
    links = Column(String(200), nullable=True)
    content = Column(String(1000), nullable=False)


#
# Methods
#
    def serialize(self):
        return {
            "date": self.date.isoformat() if self.date else "",
            "job_title": self.job_title,
            "company": self.company,
            "city": self.city,
            "technologies": self.technologies,
            "job_type": self.job_type,
            "links": self.links,
            "content": self.content
        }