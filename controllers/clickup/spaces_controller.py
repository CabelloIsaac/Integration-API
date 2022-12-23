import json
from config.config import Config


def get_by_team(team_id: int):
    team = Config.clickup.get_team_by_id(team_id)
    space = team.get_space(Config.CLICKUP_SPACE_ID)
    json_without_slash = json.loads(space._json)

    return json_without_slash
