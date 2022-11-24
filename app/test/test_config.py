import unittest
from flask import current_app

from app.main.config import CONNECTION_STR
from manage import app


class TestDevelopmentConfig(unittest.TestCase):
    @staticmethod
    def create_app(self):
        app.config.from_object("app.main.config.DevelopmentConfig")
        return app

    def test_app_is_development(self):
        self.assertFalse(app.config["SECRET_KEY"] == "my_precious")
        self.assertTrue(app.config["DEBUG"] is True)
        self.assertFalse(current_app is None)
        self.assertTrue(app.config["SQLALCHEMY_DATABASE_URI"] == CONNECTION_STR)


class TestTestingConfig(unittest.TestCase):
    @staticmethod
    def create_app(self):
        app.config.from_object("app.main.config.TestingConfig")
        return app

    def test_app_is_testing(self):
        self.assertFalse(app.config["SECRET_KEY"] == "my_precious")
        self.assertTrue(app.config["DEBUG"])
        self.assertTrue(app.config["SQLALCHEMY_DATABASE_URI"] == CONNECTION_STR)


class TestProductionConfig(unittest.TestCase):
    @staticmethod
    def create_app():
        app.config.from_object("app.main.config.ProductionConfig")
        return app

    def test_app_is_production(self):
        self.assertTrue(app.config["DEBUG"])


if __name__ == "__main__":
    unittest.main()
