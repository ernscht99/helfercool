# HANDLES ALL NETWORK COMMUNICATION
import requests as req
from lxml import html


class Session_commander:
    def __init__(self, url):
        self.url_dict = {"base": url, "login": url + "login/"}
        self.session = req.Session()
        self.session.get(self.url_dict["login"])

    def login_server(self, user_name, password):
        login_data = {
            "username": user_name,
            "password": password,
            "next": "",
            "csrfmiddlewaretoken": self.session.cookies["csrftoken"],
        }

        self.session.headers.update(
            {
                "X-CSRFToken": self.session.cookies["csrftoken"],
                "Content-Type": "application/x-www-form-urlencoded",
            }
        )

        # send login request
        resp = self.session.post(self.url_dict["login"], data=login_data)
        ht = html.document_fromstring(resp.text)
        if ht.xpath("//ul[contains(@class, 'text-danger')]"):
            raise Exception("Wrong credentials")

    def add_shift(self, data, festival_id, job_id):
        # Add token
        data.update({"csrfmiddlewaretoken": self.session.cookies["csrftoken"]})

        # Send Request
        resp = self.session.post(
            f"{self.url_dict['base']}{festival_id}/jobs/{job_id}/shift/new/",
            data=data
        )

        if resp.status_code == 200:
            print("Shift ADDED")
            return True
        else:
            print(resp)
            return False

    def add_job(self, data, festival_id):
        # Add token
        data.update({"csrfmiddlewaretoken": self.session.cookies["csrftoken"]})

        # Send Request
        resp = self.session.post(
            f"{self.url_dict['base']}{festival_id}/jobs/new/", data=data
        )

        if resp.status_code == 200:
            print("Job ADDED")
            return True
        else:
            print(resp)
            return False

    def end_conncection(self):
        pass

    def get_session_state(self):
        pass
