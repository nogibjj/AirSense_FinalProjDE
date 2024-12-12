from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):
    @task(1)
    def home(self):
        self.client.get("/")

    @task(1)
    def explorer(self):
        self.client.get("/explorer")

    @task(1)
    def chat(self):
        self.client.get("/chat")

    @task(1)
    def about(self):
        self.client.get("/about")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)
