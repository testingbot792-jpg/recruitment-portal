from mongoengine import Document, StringField

class Job(Document):
    title = StringField()
    description = StringField()
    company = StringField()
    created_by = StringField()


class Application(Document):
    job_id = StringField()
    candidate_id = StringField()
    status = StringField(default="pending")