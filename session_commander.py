# HANDLES ALL NETWORK COMMUNICATION
import requests as req
from lxml import html
from regex import search

LOCALE = "de-DE,de;q=0.5"


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
        self.url_dict["helpers"] = self.url_dict["festival"] + "/helpers"
        self.session = req.Session()
        self.session.get(self.url_dict["login"])
        self._cached_jobs = {}
        self._cached_jobs_dirty = True

    def _post(self, path, data={}):
        _log("POST", path, data)
        data["csrfmiddlewaretoken"] = self.session.cookies["csrftoken"]
        data["Accept-Language"] = LOCALE
        return self.session.post(path, data)

    def _get(self, path):
        _log("GET", path)
        data = {
            "csrfmiddlewaretoken": self.session.cookies["csrftoken"],
            "Accept-Language": LOCALE,
        }
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

    def add_shift(self, row, visable=True):
        data = {
            "name": row["subtask"],
            "begin_0": row["start_datetime"].date().isoformat(),
            "begin_1": row["start_datetime"].time().isoformat(),
            "end_0": row["end_datetime"].date().isoformat(),
            "end_1": row["end_datetime"].time().isoformat(),
            "number": str(row["num_helpers"]),
        }

        if not visable:
            data["hidden"] = "on"

        if not row["task"] in self.get_jobs():
            self.add_empty_job(row["task"])
        job_id = self.get_jobs()[row["task"]]

        # Send Request
        resp = self._post(
            f"{self.url_dict['jobs']}/{job_id}/shift/new/", data=data)

        if resp.status_code == 200:
            print("Shift ADDED")
            return True
        else:
            print(resp)
            print(f"{row['subtask']} rejected")
            return False

    def add_shifts(self, shifts_df):
        for _, row in shifts_df.iterrows():
            self.add_shift(row)

            # Work with not visable/internal jobs
            if "num_intern_helpers" in row:
                if row["num_intern_helpers"] > 0:
                    row["num_helpers"] = row["num_intern_helpers"]
                    self.add_shift(row, visable=False)

    def add_job(self, data):
        # Send Request
        resp = self._post(f"{self.url_dict['jobs']}/new/", data=data)

        if resp.status_code == 200:
            print("Job ADDED")
            self._cached_jobs_dirty = True
            return True
        else:
            print(resp)
            return False

    def get_jobs(self):
        if self._cached_jobs and not self._cached_jobs_dirty:
            return self._cached_jobs
        resp = self._get(self.url_dict["helpers"])
        ht = html.document_fromstring(resp.text)
        headings = [h.text.strip() for h in ht.xpath("//h2")]
        links = ht.xpath("/html/body/div/div/p/a")
        ids = [search(r"job/(\d+)", li.get("href")).group(1) for li in links]
        self._cached_jobs = {h: i for h, i in zip(headings, ids)}
        self._cached_jobs_dirty = False
        return self._cached_jobs

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
        existing_jobs = self.get_jobs()
        for job_title in [j for j in jobs if j not in existing_jobs]:
            self.add_empty_job(job_title)
        print("Jobs ADDED")
        print("Jobs that are now online:")
        for online_job in self.get_jobs():
            print(online_job)

    def remove_job(self, job_id):
        self._post(self.url_dict["jobs"] + f"/{job_id}/delete/")

    def remove_all_jobs(self):
        for job_id in self.get_jobs().values():
            self.remove_job(job_id)

    def test(self):
        print(self.get_jobs())
        pass

    def end_conncection(self):
        pass

    def get_session_state(self):
        pass
