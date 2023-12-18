
import json
import requests
from src.config import Env
from typing import List
from .response_models.get_leads import DataLeads, Lead
class AplloService():
    def __init__(self) -> None:
        self.__vars = Env()
        self.__url = self.__vars.apollo_url
        self.__key = self.__vars.apollo_master_key
        self.__headers = {"Cache-Control": "no-cache"}

    def get_leads(self, page) -> List[Lead]:
        leads_clickeds = self.__get_leads_clicked(page)
        leads_opened = self.__get_leads_opened(page)
        leads = [lead for lead in (leads_clickeds + leads_opened) if lead.data_contact]
        return leads

    def get_enrichment_lead(self, lead) -> dict:
        contact = self.__get_contact(lead)
        url = self.__generate_endpoint('/people/match')
        body = self.__generate_body_get_enrichment_leads(contact=contact)
        response = requests.post(url=url, headers=self.__headers, json=body)
        enrichment_lead = response.json()
        if enrichment_lead.get('person'):
            person = enrichment_lead['person']
            if person.get('organization'):
                return person
            organization = self.__get_enrichment_organization(contact)
            person['organization'] = organization
            return person

    def __generate_endpoint(self, path: str) -> str:
        return f'{self.__url}/{path}'

    def __generate_body_get_leads(self, status_email: str, opened_number: int, page: int) -> dict:
        """
        :param status_email: Recebe 'opened' ou 'clicked'
        :param opened_number: Número de vezes que o email foi aberto
        :param page: Paginação do apollo
        :return: Corpo da requisição
        """
        return {
            "api_key": self.__key,
            "num_emailer_message_opens_at_least": str(opened_number),
            "emailer_message_stats": status_email,
            "page": page
        }

    def __generate_body_get_enrichment_leads(self, contact) -> dict:
        """
        :param contact: return of self.__get_contact
        :return: Corpo da requisição
        """
        return {
            'first_name': contact['first_name'],
            'last_name': contact['last_name'],
            'email': contact['email'],
            'organization_name': contact['organization']['name'],
            'linkedin_url': contact['linkedin_url'],
            'title': contact['title'],
        }

    def __get_leads_clicked(self, page) -> List[Lead]:
        url = self.__generate_endpoint('emailer_messages/search')
        body = self.__generate_body_get_leads(status_email='clicked', opened_number=2, page=page)
        response = requests.post(url=url, headers=self.__headers, json=body)
        if response.status_code == 429:
            raise Exception(f'Erro: {response.text}')
        response_model: DataLeads = DataLeads(**response.json())
        return [lead for lead in response_model.leads if lead.num_clicks and lead.num_clicks >= 2]

    def __get_leads_opened(self, page) -> List[Lead]:
        url = self.__generate_endpoint('emailer_messages/search')
        body = self.__generate_body_get_leads(status_email='opened', opened_number=3, page=page)
        response = requests.post(url=url, headers=self.__headers, json=body)
        if response.status_code == 429:
            raise Exception(f'Erro: {response.text}')
        return DataLeads(**response.json()).leads

    def __get_enrichment_organization(self, contact) -> dict:
        url = self.__generate_endpoint('organizations/enrich')
        body = {'domain': contact['organization']['primary_domain']}
        response = requests.post(url=url, headers=self.__headers, json=body)
        enrichment_organization = response.json()
        if enrichment_organization.get('organization'):
            return enrichment_organization['organization']

    def __get_contact(self, lead) -> dict:
        url = self.__generate_endpoint('/contacts/search')
        filters = f'{lead["recipients"][0]["raw_name"]}, {lead["recipients"][0]["email"]}'
        body = {'q_keywords': filters}
        response = requests.post(url=url, headers=self.__headers, json=body)
        contacts = response.json()
        if contacts.get('contacts'):
            return json.loads(response.content)['contacts'][0]
