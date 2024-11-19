import requests


class KakaoAPI:
    def __init__(self, access_token):
        self.access_token = access_token
        self.user_info_url = "https://kapi.kakao.com/v2/user/me"

    def get_user_info(self):
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(self.user_info_url, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch user info from Kakao: {response.json()}")
        return response.json()
