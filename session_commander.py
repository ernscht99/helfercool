# HANDLES ALL NETWORK COMMUNICATION
import requests as req
from lxml import html


class Session_commander:
    def __init__(self, url, festival_id):
        self.url_dict = {
            "base": url,
            "login": url + "login/",
            "festival": url + str(festival_id),
            "jobs": url + "jobs/",
        }
        self.session = req.Session()
        self.session.get(self.url_dict["login"])

    def _post(self, path, data):
        data["csrfmiddlewaretoken"] = self.session.cookies["csrftoken"]
        return self.session.post(path, data)

    def _get(self, path, data):
        data["csrfmiddlewaretoken"] = self.session.cookies["csrftoken"]
        return self.session.get(path, data)

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

    def add_shift(self, data, job_id):
        # Send Request
        resp = self._post(
            f"{self.url_dict['festival']}/jobs/{job_id}/shift/new/", data=data
        )

        if resp.status_code == 200:
            print("Shift ADDED")
            return True
        else:
            print(resp)
            return False

    def add_job(self, data):
        # Send Request
        resp = self._post(
            f"{self.url_dict['festival']}/jobs/new/", data=data)

        if resp.status_code == 200:
            print("Job ADDED")
            return True
        else:
            print(resp)
            return False

    def remove_job(self, job_id):
        pass

    def end_conncection(self):
        pass

    def get_session_state(self):
        pass
