# HANDLES ALL NETWORK COMMUNICATION
import requests as req
from lxml import html


def _log(method, path, data=None):
    print(f"{method}: '{path}', data={data}")


class Session_commander:
    def __init__(self, url, festival_id):
        self.url_dict = {
            "base": url,
            "login": url + "/login/",
            "festival": url + "/" + str(festival_id),
        }
        self.url_dict["jobs"] = self.url_dict["festival"] + "/jobs"
        self.session = req.Session()
        self.session.get(self.url_dict["login"])

    def _post(self, path, data):
        _log("POST", path, data)
        data["csrfmiddlewaretoken"] = self.session.cookies["csrftoken"]
        return self.session.post(path, data)

    def _get(self, path):
        _log("GET", path)
        data = {"csrfmiddlewaretoken": self.session.cookies["csrftoken"]}
        return self.session.get(path, data=data)

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
            f"{self.url_dict['jobs']}/{job_id}/shift/new/", data=data
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
            f"{self.url_dict['jobs']}/new/", data=data)

        if resp.status_code == 200:
            print("Job ADDED")
            return True
        else:
            print(resp)
            return False

    def _get_jobs(self):
        resp = self._get(self.url_dict["jobs"])
        ht = html.document_fromstring(resp.text)
        headings = ht.xpath('//h2')
        return [heading.text.strip() for heading in headings]

    def add_empty_job(self, title, public=True):
        data = {
                "name_de": title,
                "name_en": title,
                "description_de": "<p>Beschreibung</p>\r\n",
                "description_en": "<p>Descrpition</p>\r\n",
                "important_notes_de": "<p>Wichtige Infos</p>\r\n",
                "important_notes_en": "<p>Important Notes</p>\r\n",
                "public": "on" if public else "off",
                "infection_instruction": "on",
                }
        self.add_job(data)

    def add_jobs(self, jobs):
        for job_title in jobs:
            self.add_empty_job(job_title)
        print("Jobs ADDED")
        print("Jobs that are now online:")
        for online_job in self._get_jobs():
            print(online_job)

    def remove_job(self, job_id):
        pass

    def test(self):
        print(self._get_jobs())
        pass

    def end_conncection(self):
        pass

    def get_session_state(self):
        pass
