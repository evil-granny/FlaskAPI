from locust import HttpLocust, TaskSet, task
import json


class UserBehavior(TaskSet):
    # runs one time for each user
    def on_start(self):
        self.client.get("/")

    @task(2)  # chance to run 2/3
    def rooms(self):
        self.client.get("rooms/")

    @task(3)  # chance to run 2/3
    def room(self):
        self.client.get("room/6")

    @task(4)
    def create_room(self):
        headers = {'content-type': 'application/json',
                   'Accept-Encoding': 'gzip'}
        self.client.post("/room/", data=json.dumps({
            "title": "changed110", "price": 300001, "description": "Cheap1"
        }),
            headers=headers,
            name="Create a new room")

    @task(5)
    def update_room(self):
        headers = {'content-type': 'application/json',
                   'Accept-Encoding': 'gzip'}
        self.client.put("update/0", data=json.dumps({
            "title": "Estate12",
            "price": 3000002,
            "description": "Luxury"
        }),
            headers=headers,
            name="Update an room")

    @task(6)  # chance to run 2/3
    def delete(self):
        self.client.delete('delete/8')


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = 3000
