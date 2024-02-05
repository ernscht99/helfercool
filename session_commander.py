# HANDLES ALL NETWORK COMMUNICATION
import requests as req


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

        # TODO: check if it worked

    def add_shift(self, data,festival_id,job_id):
        # Add token
        data.update({"csrfmiddlewaretoken": self.session.cookies["csrftoken"]})

        # Send Request
        resp = self.session.post(f"{self.url_dict['base']}{festival_id}/jobs/{job_id}/shift/new/", data=data)
        print(resp)

    def end_conncection(self):
        pass

    def get_session_state(self):
        pass
