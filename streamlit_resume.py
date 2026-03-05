import uuid

from curl_cffi import requests


class StreamlitClient:
    def __init__(self):
        self.session = requests.Session()
        self._uuid = str(uuid.uuid4())

    def status_request(self):

        burp0_url = "https://juanfrilla.streamlit.app/api/v2/app/status"
        burp0_headers = {
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Accept-Language": "es-ES,es;q=0.9",
            "Accept": "application/json",
            "Sec-Ch-Ua": '"Chromium";v="136", "Not:A-Brand";v="99"',
            "X-Streamlit-Machine-Id": self._uuid,
            "Sec-Ch-Ua-Mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://juanfrilla.streamlit.app/",
            "Accept-Encoding": "gzip, deflate, br",
            "Priority": "u=1, i",
        }
        return self.session.get(
            burp0_url, headers=burp0_headers, impersonate="chrome136"
        )

    def resume_request(self, csrf_token):
        burp0_url = "https://juanfrilla.streamlit.app/api/v2/app/resume"
        burp0_headers = {
            "Sec-Ch-Ua-Platform": '"Windows"',
            "X-Csrf-Token": csrf_token,
            "Accept-Language": "es-ES,es;q=0.9",
            "Sec-Ch-Ua": '"Chromium";v="136", "Not:A-Brand";v="99"',
            "Sec-Ch-Ua-Mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "X-Streamlit-Machine-Id": self._uuid,
            "Origin": "https://juanfrilla.streamlit.app",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://juanfrilla.streamlit.app/",
            "Accept-Encoding": "gzip, deflate, br",
            "Priority": "u=1, i",
        }
        return self.session.post(
            burp0_url, headers=burp0_headers, impersonate="chrome136"
        )

    def resume(self):
        response = self.status_request()
        csrf_token = response.headers.get("X-Csrf-Token")
        response = self.resume_request(csrf_token)


if __name__ == "__main__":
    st_client = StreamlitClient()
    st_client.resume()
