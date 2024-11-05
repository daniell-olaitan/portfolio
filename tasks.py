from portfolio import celery
from typing import Dict


@celery.task
def send_async_email(email_data: Dict) -> None:
    """
    Background task to send email for user authentication
    """
    from app import mail
    from portfolio import app
    from flask_mail import Message

    msg = Message(
        subject=email_data['subject'],
        sender=email_data['sender'],
        recipients=email_data['recipients']
    )

    msg.body = email_data['msg_body']
    with app.app_context():
        mail.send(msg)
