import json
from unittest import TestCase

from fastapi import status
from starlette.testclient import TestClient

from app.server import app

client = TestClient(app)


class HealthCheckTest(TestCase):
    def test_status(self):
        response = client.request(
            method='GET',
            url='/status',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_status_version(self):
        response = client.request(
            method='GET',
            url='/status/version',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        status_version = json.loads(response.content.decode('utf-8'))
        self.assertIn('version', status_version)
        self.assertIn('branch', status_version)
