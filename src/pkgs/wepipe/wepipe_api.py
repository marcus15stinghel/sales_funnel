import requests
from src.config.env import Env


class Wepipe_Api:
    def __init__(self) -> None:
        self.env = Env()
        self.__url = self.env.wepipe_url
        self.__header = {'Authorization': self.env.wepipe_authorization, 'Token': self.env.wepipe_token}
        self.__user_id = self.env.wepipe_outbound_user_id

    def insert_card(self, card) -> bool:
        """
        Insere card via api do wepipe
        :param card: Estrutura json no padrão de card wepipe
        :return: status de retorno da requisição
        """
        url = self.__generate_url('cards')
        response = requests.post(url=url, headers=self.__header, json=card)
        return response.status_code == 201

    def __generate_url(self, endpoint) -> str:
        return f'{self.__url}/'
