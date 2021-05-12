""" Email helper """
from django.conf import settings
from django.core import mail
from django.core.mail import EmailMessage


def send_email(subject, body, receivers):
    """ Sends an email to given receivers.

    Parameters
    ----------

    subject: str
        Email subject

    body: str
        Email content to send

    receivers: list/str
        Email receiver/s

    """
    if isinstance(receivers, str):
        receivers = [receivers]
    try:
        msg = EmailMessage(subject, body, settings.EMAIL_HOST_USER, receivers)
        msg.content_subtype = "html"
        msg.send()
        return True
    except:
        return False