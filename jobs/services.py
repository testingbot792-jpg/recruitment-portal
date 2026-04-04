from .models import Job, Application, SavedJob

from .models import Job

def create_job(data, user_id, files=None, job=None):

    if not job:
        job = Job()

    job.title = data.get('title')
    job.job_id = data.get('job_id')
    job.department = data.get('department')
    job.company = data.get('company')
    job.location = data.get('location')

    job.job_summary = data.get('job_summary')
    job.responsibilities = data.get('responsibilities')
    job.required_qualifications = data.get('required_qualifications')

    job.experience_years = data.get('experience_years')
    job.compensation = data.get('compensation')

    if files and files.get('logo'):
        job.logo.put(files['logo'], filename=files['logo'].name)

    job.save()
    return job

def apply_to_job(job_id, user_id):
    # 🔒 Prevent duplicate application
    existing = Application.objects(job_id=job_id, user_id=user_id).first()

    if existing:
        return  # already applied

    Application(
        job_id=job_id,
        user_id=user_id,
        status="applied"
    ).save()



def save_job(user_id, job_id):
    if not SavedJob.objects(user_id=user_id, job_id=job_id).first():
        SavedJob(user_id=user_id, job_id=job_id).save()