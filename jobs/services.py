from .models import Job, Application

def create_job(data, user_id):
    return Job(
        title=data['title'],
        description=data['description'],
        company=data['company'],
        created_by=user_id
    ).save()

def apply_to_job(job_id, user_id):
    return Application(
        job_id=job_id,
        candidate_id=user_id
    ).save()