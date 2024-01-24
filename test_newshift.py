#!/usr/bin/env python3
import requests as re

host = "http://127.0.0.1:8000/"
url = host + "stustaculon/jobs/1/shift/new/"
login_url = host + "login/"


s = re.Session()
s.get(login_url)

login_data = {
    "username": "felix",
    "password": "felix",
    "next": "",
    "csrfmiddlewaretoken": s.cookies["csrftoken"],
}
s.headers.update(
    {
        "X-CSRFToken": s.cookies["csrftoken"],
        "Content-Type": "application/x-www-form-urlencoded",
    }
)
resp = s.post(login_url, data=login_data)

data = {
    "name": "Suff",
    "begin_0": "2024-01-25",
    "begin_1": "11:00",
    "end_0": "2024-01-25",
    "end_1": "14:00",
    "number": "6",
    "csrfmiddlewaretoken": s.cookies["csrftoken"],
}
x = s.post(url, data=data)
