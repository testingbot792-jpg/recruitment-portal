from django.core.mail import send_mail

def send_application_email(to_email):
    send_mail(
        "Job Application",
        "You successfully applied!",
        "your@email.com",
        [to_email],
        fail_silently=True,
    )