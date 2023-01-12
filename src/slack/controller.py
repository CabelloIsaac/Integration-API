from .service import slack_client


def test_connection():
    return slack_client.test_connection()

