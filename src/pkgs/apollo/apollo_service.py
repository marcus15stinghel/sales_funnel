import requests
from src.config import Env
from typing import List
from src.pkgs.apollo.models.responses.get_leads import DataLeads, Lead
from src.pkgs.apollo.models.responses.get_enrichment_contact import EnrichmentContact
from src.pkgs.apollo.models.responses.get_enrichment_organization import EnrichmentOrganization
from src.pkgs.apollo.models.responses.get_enrichment_lead import EnrichmentLead


class AplloService:
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

    def get_enrichment_lead(self, lead) -> EnrichmentLead:
        contact = self.__get_enrichment_contact(lead=lead)
        body = self.__generate_body_get_enrichment_lead(contact=contact)
        url = self.__generate_endpoint('/people/match')
        response = requests.post(url=url, headers=self.__headers, json=body)
        enrichment_lead = EnrichmentLead(**response.json())
        if not enrichment_lead.data.organization:
            organization = self.__get_enrichment_organization(contact=contact)
            enrichment_lead.data.organization = organization
        return enrichment_lead

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

    def __get_enrichment_contact(self, lead: Lead) -> EnrichmentContact:
        url: str = self.__generate_endpoint('/contacts/search')
        body: dict = self.__generate_body_get_enrichment_contact(lead=lead)
        response = requests.post(url=url, headers=self.__headers, json=body)
        if response.status_code == 429:
            raise Exception(f'Erro: {response.text}')
        return EnrichmentContact(**response.json())

    def __get_enrichment_organization(self, contact: EnrichmentContact) -> EnrichmentOrganization:
        url: str = self.__generate_endpoint('organizations/enrich')
        body: dict = self.__generate_body_get_enrichment_organization(contact)
        response = requests.post(url=url, headers=self.__headers, json=body)
        if response.status_code == 429:
            raise Exception(f'Erro: {response.text}')
        return EnrichmentOrganization(**response.json())

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

    def __generate_body_get_enrichment_contact(self, lead: Lead) -> dict:
        return {
            "api_key": self.__key,
            'q_keywords': f'{lead.data_contact[0].name}, {lead.data_contact[0].email}'
        }

    def __generate_body_get_enrichment_organization(self, contact: EnrichmentContact) -> dict:
        return {
            'api_key': self.__key,
            'domain': contact.data.organization.web_domain
        }

    def __generate_body_get_enrichment_lead(self, contact: EnrichmentContact) -> dict:
        """
        :param contact: return of self.__get_contact
        :return: Corpo da requisição
        """
        return {
            'api_key': self.__key,
            'first_name': contact.data.first_name,
            'last_name': contact.data.last_name,
            'email': contact.data.email,
            'organization_name': contact.data.organization.name,
            'linkedin_url': contact.data.linkedin_url,
            'title': contact.data.job_title,
        }

    def __generate_endpoint(self, path: str) -> str:
        return f'{self.__url}/{path}'
