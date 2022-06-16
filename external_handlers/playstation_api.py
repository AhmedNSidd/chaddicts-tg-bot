import datetime
import humanize
from models.player import Player
from psnawp_api import psnawp


class PlaystationApi:
    # REVIEW: To implement object class here or not? why or why not?

    def __init__(self, npsso) -> None:
        # REVIEW: Is client an appropriate name for this obj. variable?
        self.client = psnawp.PSNAWP(npsso)

    def get_players(self, ids, names):
        player_list = []
        for x in range(len(ids)):
            resp = self.client.user(account_id=ids[x]).get_presence()
            is_user_online = PlaystationApi._parse_is_online(resp)
            player = Player(ids[x], names[x], is_user_online,
                PlaystationApi._parse_current_title(resp),
                PlaystationApi._parse_last_seen(resp) if not is_user_online else None
            )
            player_list.append(player)

        return player_list

    # REVIEW: I don't see why these shouldn't be static methods
    # but at the same time, I see no use case for these methods
    # being called outside of inside this API. 
    # 
    # Should private helper methods be static?
    @staticmethod
    def _parse_is_online(resp):
        return resp["availability"] == "availableToPlay"

    @staticmethod
    def _parse_current_title(resp):
        return (resp["gameTitleInfoList"]["titleName"]
                if "gameTitleInfoList" in resp
                else None)

    @staticmethod
    def _parse_last_seen(resp):
        if not 'lastAvailableDate' in resp:
            return None
        last_seen = humanize.naturaltime(datetime.datetime.fromisoformat(resp["lastAvailableDate"][:23]) - datetime.datetime.utcnow())
        last_seen = last_seen.replace("from now", "ago")

        return last_seen
