import os
from dotenv import load_dotenv


class Env:

    def __init__(self) -> None:
        load_dotenv()

    @property
    def apollo_url(self) -> str:
        return os.environ['APOLLO_URL']

    @property
    def apollo_master_key(self) -> str:
        return os.environ['APOLLO_MASTER_KEY']

    @property
    def wepipe_url(self) -> str:
        return os.environ['WEPIPE_URL']

    @property
    def wepipe_authorization(self) -> str:
        return os.environ['WEPIPE_AUTHORIZATION']

    @property
    def wepipe_token(self) -> str:
        return os.environ['WEPIPE_TOKEN']

    @property
    def wepipe_outbound_user_id(self) -> int:
        return int(os.environ['WEPIPE_OUTBOUND_USER_ID'])
