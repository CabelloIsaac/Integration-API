import json
from config.config import Config


def get_all():
    teams = Config.clickup.teams
    teams_data = []
    for team in teams:
        json_without_slash = json.loads(team._json)
        teams_data.append(json_without_slash)

    return teams_data
