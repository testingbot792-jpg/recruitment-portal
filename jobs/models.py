from mongoengine import Document, StringField

class Job(Document):
    title = StringField(required=True)
    description = StringField(required=True)
    company = StringField()
    created_by = StringField()


class Application(Document):
    job_id = StringField()
    candidate_id = StringField()
    status = StringField(default="pending")