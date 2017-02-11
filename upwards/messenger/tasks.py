from __future__ import absolute_import
import requests
from . services import email_service, otp_service
from upwards.celery import app


@app.task
def send_verification_mail(email_verify_data):
    email_service.send_verification_mail(email_verify_data)


@app.task
def update_email_models(email_object_updated):
    email_service.update_email_models(email_object_updated)


# @app.task
# def send_otp(otp_data):
#     otp_service.send_otp(otp_data)
