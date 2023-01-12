from .service import slack_client


def test_connection(send_alert: bool = False):
    return slack_client.test_connection(send_alert=send_alert)


def send_alert(message: str):
    return slack_client.send_alert(message)