from schemas.todo import TodoIn
from tests.config import test_client, db_session, engine_session


class TestTodo:
    def setup_class(self):
        self.valid_todo = TodoIn(
            title="Test todo",
            is_completed=False,
        )
        self.valid_todo_updated = TodoIn(
            title="Test todo Updated",
            is_completed=True,
        )

    def test_todo_create(self, test_client):
        response = test_client.post(
            "/todo",
            json=self.valid_todo.model_dump(),
        )
        todo = response.json()

        assert response.status_code == 201
        assert todo["id"] == 1
        assert todo["title"] == self.valid_todo.title
        assert todo["is_completed"] == self.valid_todo.is_completed

    def test_todo_list(self, test_client):
        response = test_client.get("/todo")
        todo_list = response.json()

        assert response.status_code == 200
        assert len(todo_list) == 1

    def test_todo_update(self, test_client):
        response = test_client.put(
            "/todo/1",
            json=self.valid_todo_updated.model_dump(),
        )
        todo = response.json()

        assert todo["id"] == 1
        assert todo["title"] == self.valid_todo_updated.title

    def test_todo_delete(self, test_client):
        response = test_client.delete("/todo/1")

        assert response.status_code == 204

        check_response = test_client.get("/todo/1")

        assert check_response.status_code == 404
