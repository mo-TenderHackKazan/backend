import requests
from celery import shared_task
from django.utils.timezone import now

from error_handler.errors.models import Error, ErrorType
from error_handler.errors.services import extract_params
from error_handler.utils.generators import generate_charset

ML_HOST = "http://10.9.67.133:8000/"


@shared_task
def process_error(body: str):
    res = requests.post(ML_HOST + "error", json={"log": body})
    if res.status_code != 200:
        raise res.status_code
    resp = res.json()["label_text"]
    er_t = ErrorType.objects.get_or_create(name=resp)[0]
    Error.objects.create(
        eid=generate_charset(32),
        type=er_t,
        params=extract_params(body),
        created=now(),
        body=body,
    )
