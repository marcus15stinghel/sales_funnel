from src.pkgs.apollo import AplloService, Lead
from src.pkgs.wepipe import Wepipe_Api #, Wepipe_card
from src.config import Log
import logging as log
from typing import List
import json


class ApolloSendLeads:
    def __init__(self):
        Log.configurator()
        self.__old_leads_path = 'src/integrators/apollo_send_leads/leads.json'
        self.__apollo_api = AplloService()
        self.__wepipe_api = Wepipe_Api()
        self.__get_old_leads()
        self.__leads_to_integrate: list[dict] = []

    def run(self) -> None:
        log.info('Início do progrma. \n')
        page = 0
        leads_per_page = 25
        while leads_per_page >= 25:
            page += 1
            leads = self.__get_new_leads(page=page)
            for lead in leads:
                # Enriquecer lead e enviar para o wepipe

                self.__add_lead_to_integrate(lead=lead)
            self.__update_old_leads()
            self.__leads_to_integrate.clear()
        log.info('Fim do programa.')

    def __get_old_leads(self) -> None:
        with open(self.__old_leads_path, 'r', encoding='utf-8') as data:
            self.__integrated_leads: list[str] = [lead['contact_id'] for lead in json.load(data)]

    def __get_new_leads(self, page: int) -> list[Lead]:
        leads: List[Lead] = self.__apollo_api.get_leads(page)
        log.info(f'Pack de leads pego. Página: {page}, Total: {len(leads)} \n')
        return [lead for lead in leads if lead.data_contact[0].id not in self.__integrated_leads]

    def __add_lead_to_integrate(self, lead: Lead):
        self.__integrated_leads.append(lead.data_contact[0].id)
        self.__leads_to_integrate.append(self.__generate_integrated_lead(lead=lead))
        log.info(f'Card {lead.data_contact[0].id} Adicionado à lista de leads antigos.')

    def __update_old_leads(self) -> None:
        with open(self.__old_leads_path, 'r', encoding='utf-8') as data:
            old_leads: list[dict] = json.load(data)
        with open(self.__old_leads_path, 'w', newline='\n', encoding='utf-8') as data:
            json.dump(old_leads + self.__leads_to_integrate, data, indent=4, ensure_ascii=False)
        log.info('\nLista de leads já integrados atualizada.')

    @staticmethod
    def __generate_integrated_lead(lead: Lead) -> dict:
        return {
            "name": lead.data_contact[0].name,
            "contact_id": lead.data_contact[0].id
        }


# Falta configurar o arquivo main para receber args


# enrichment_lead = apollo_api.get_enrichment_lead(lead=lead)
# log.info(f'Lead {lead["id"]} enriquecido.')
# card = Wepipe_card(enrichment_lead)
# integrated = wepipe_api.insert_card(card.data)
# if integrated:
#     log.info(f'Card {lead["id"]} enviado para Ountbound.')
# else:
#     log.info(f'Card {lead["id"]} não intgrado, contato inexistente.')
