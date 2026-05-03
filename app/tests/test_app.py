import os
import sys
import unittest
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from app import app  # noqa: E402


class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_health_endpoint_returns_ok(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})

    def test_index_endpoint_returns_service_metadata(self):
        response = self.client.get("/")
        payload = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(payload["service"], "devops-lab")
        self.assertIn("hostname", payload)
        self.assertTrue(payload["hostname"])

    def test_index_endpoint_uses_default_version(self):
        previous_version = os.environ.pop("APP_VERSION", None)

        try:
            response = self.client.get("/")
            self.assertEqual(response.get_json()["version"], "1.0.0")
        finally:
            if previous_version is not None:
                os.environ["APP_VERSION"] = previous_version


if __name__ == "__main__":
    unittest.main()
