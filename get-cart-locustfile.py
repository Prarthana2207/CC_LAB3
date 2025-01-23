from locust import task, run_single_user, FastHttpUser
from insert_product import login


class AddToCartUser(FastHttpUser):
    host = "http://localhost:5000"

    default_headers = {
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "DNT": "1",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    }

    def on_start(self):
        self.token = self.login_user("test123", "test123")

    def login_user(self, username, password):
        cookies = login(username, password)
        token = cookies.get("token")
        if not token:
            raise ValueError("Login failed: No token received.")
        return token

    @task
    def view_cart(self):
        headers = self.get_request_headers()
        with self.client.get("/cart", headers=headers, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed to fetch cart: {response.status_code} - {response.text}")

    def get_request_headers(self):
        headers = self.default_headers.copy()
        headers["Cookies"] = f"token={self.token}"
        headers["Referer"] = f"{self.host}/product/1"
        headers.update({
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
        })
        return headers


if __name__ == "__main__":
    run_single_user(AddToCartUser)
