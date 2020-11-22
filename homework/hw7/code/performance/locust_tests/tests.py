import json

from locust import HttpUser, task, between, TaskSet


class UnAuthorizedScenario(TaskSet):

    @task
    def index(self):
        self.client.get("/")

    @task
    def products_1(self):
        self.client.get("/products/1")

    @task
    def products_1(self):
        self.client.get("/contacts")

    @task
    def products_1(self):
        self.client.get("/products/4")


class AuthorizedScenario(TaskSet):
    def on_start(self):
        response = self.client.get('/profile', auth=('vova', '123'))
        self.client.headers.update({'Authorization': response.request.headers.get('Authorization')})

    def on_stop(self):
        self.client.get('/logout')

    @task
    def index(self):
        self.client.get("/")

    @task
    def profile(self):
        self.client.get("/profile")


class PostScenario(TaskSet):
    def on_start(self):
        response = self.client.get('/profile', auth=('yarik', '12345'))
        self.client.headers.update({'Authorization': response.request.headers.get('Authorization')})
        assert 200 == response.status_code

    def on_stop(self):
        self.client.get('/logout')

    @task
    def contact_post(self):
        data = {'name': 'volodimir', "body": "hi"}
        self.client.post('/contacts', data=json.dumps(data))

    @task
    def contact_auth_post(self):
        data = {"body": "hi"}
        self.client.post('/contacts', data=json.dumps(data))


class WebSiteUser(HttpUser):
    tasks = [UnAuthorizedScenario, AuthorizedScenario, PostScenario]
    wait_time = between(1, 2)
