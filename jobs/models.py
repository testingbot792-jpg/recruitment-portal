from mongoengine import Document, StringField, FileField

class Job(Document):
    title = StringField(required=True)
    job_id = StringField()
    department = StringField()
    company = StringField()
    location = StringField()
    employment_type = StringField()
    reports_to = StringField()

    job_summary = StringField()
    role_purpose = StringField()
    responsibilities = StringField()
    duties = StringField()

    required_qualifications = StringField()
    preferred_qualifications = StringField()
    certifications = StringField()

    technical_skills = StringField()
    soft_skills = StringField()
    competencies = StringField()

    experience_years = StringField()
    industry_experience = StringField()

    working_hours = StringField()
    travel_requirements = StringField()
    physical_requirements = StringField()

    compensation = StringField()
    benefits = StringField()

    about_company = StringField()
    company_culture = StringField()

    how_to_apply = StringField()
    deadline = StringField()
    contact_info = StringField()

    kpis = StringField()
    career_growth = StringField()
    equal_opportunity = StringField()
    background_check = StringField()

    logo = FileField()
    description = StringField()
    created_by = StringField()

from mongoengine import *

class Application(Document):
    user_id = StringField(required=True)
    job_id = StringField(required=True)
    status = StringField(default="Applied") 

class SavedJob(Document):
    user_id = StringField(required=True)
    job_id = StringField(required=True)