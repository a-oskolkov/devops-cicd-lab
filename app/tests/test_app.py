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

    def test_greeting_endpoint_uses_old_greeting_by_default(self):
        previous_flag = os.environ.pop("FEATURE_NEW_GREETING", None)

        try:
            response = self.client.get("/greeting")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.get_json(),
                {"greeting": "Hello from the old greeting!"},
            )
        finally:
            if previous_flag is not None:
                os.environ["FEATURE_NEW_GREETING"] = previous_flag

    def test_greeting_endpoint_uses_new_greeting_when_flag_enabled(self):
        previous_flag = os.environ.get("FEATURE_NEW_GREETING")
        os.environ["FEATURE_NEW_GREETING"] = "true"

        try:
            response = self.client.get("/greeting")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.get_json(),
                {"greeting": "Hello from the new greeting!"},
            )
        finally:
            if previous_flag is None:
                os.environ.pop("FEATURE_NEW_GREETING", None)
            else:
                os.environ["FEATURE_NEW_GREETING"] = previous_flag


if __name__ == "__main__":
    unittest.main()
