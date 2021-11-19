from flask_testing import TestCase
from application import app
from os import getenv
from flask import url_for
from application import app, db
from application.models import Tasks

class TestBase(TestCase):

    def create_app(self):
        # Defines the flask object's configuration for the unit tests
        app.config.update(
            SQLALCHEMY_DATABASE_URI=getenv("DATABASE_URI"),
            DEBUG=True,
            WTF_CSRF_ENABLED=False
            )
        return app
        
    def setUp(self):
        # Will be called before every test
        db.create_all()
        db.session.add(Tasks(name="Run unit test"))
        db.session.commit()


    def tearDown(self):
        # Will be called after every test
        db.session.remove()
        db.drop_all()


class TestViews(TestBase):
    def test_home_get(self):
        response = self.client.get(url_for('home'))
        self.assert200(response)

    def test_add_get(self):
        response = self.client.get(url_for('add'))
        self.assert200(response)

    def test_read_get(self):
        response = self.client.get(url_for('read'))
        self.assert200(response)        
    
    def test_total_tasks_get(self):
        response = self.client.get(url_for('total_tasks'))
        self.assert200(response)

    def test_update_task_get(self):
        response = self.client.get(url_for('update_task', id=1))
        self.assert200(response)

    # def test_delete_get(self):
    #     response = self.client.get(url_for('delete'))
    #     self.assert200(response.)

    # def test_completed_task_get(self):
    #     response = self.client.get(url_for('completed'))
    #     self.assert200(response)

    # def test_incomplete_task_get(self):
    #     response = self.client.get(url_for('incompleted'))
    #     self.assert200(response)


class TestRead(TestBase):
    def test_read_home_tasks(self):
        response = self.client.get(url_for('home'))
        self.assertIn(b'Run unit test', response.data)

    def test_read_tasks_dictionary(self):
        response = self.client.get(url_for('read'))
        self.assertIn(b'Run unit test', response.data)

class TestCreate(TestBase):
    def test_create_task(self):
        response = self.client.post(
            url_for('add'),
            data={"name": "Testing create function"}, 
            follow_redirects=True
        )
        self.assertIn(b"Testing create function", response.data)