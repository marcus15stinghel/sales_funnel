from src.pkgs.wepipe import wepipe_api

class Wepipe_card:
    def __init__(self, enrichment_lead: dict) -> dict:
        try: self.lead = enrichment_lead
        except: pass
        try: self.contact = self.lead['contact']
        except: pass
        try: self.organization = self.lead['organization']
        except: pass
        try: self.__card_data = {}
        except: pass
        try: self.assembler_card()
        except: pass

    @property
    def data(self) -> dict:
        return self.__card_data

    def assembler_card(self):
        self.assembler_card_infos()
        self.assembler_card_custom_fields()
        
    def assembler_card_infos(self):
        user = self.define_user()
        try: self.__card_data["user_id"] = int(user)
        except: pass
        try: self.__card_data["pipeline_id"] = 1623 # Outbound
        except: pass
        try: self.__card_data["pipeline_stage_id"] = 13479 # Qualificado
        except: pass
        try: self.__card_data["name"] = self.organization['name']
        except: pass
        try: self.__card_data["tags"] = ["🟡 Morno"]
        except: pass

    def assembler_card_custom_fields(self):
        self.__custom_fields = {}
        try: self.__custom_fields['cf_link_do_apollo'] = f'https://app.apollo.io/#/contacts/{self.lead["contact_id"]}'
        except: pass
        try: self.__custom_fields["cf_industria"] = self.organization['industry']
        except: pass
        try: self.__custom_fields["cf_total_de_colaboradores"] = self.organization['estimated_num_employees']
        except: pass
        try: self.__custom_fields["cf_website"] = self.organization['website_url']
        except: pass
        try: self.__custom_fields["cf_linkedin_da_empresa"] = self.organization['linkedin_url']
        except: pass
        try: self.__custom_fields["cf_nome"] = self.contact['first_name']
        except: pass
        try: self.__custom_fields["cf_sobrenome"] = self.contact['last_name']
        except: pass
        try: self.__custom_fields["cf_telefone"] = self.contact['phone_numbers'][0]['raw_number']
        except: pass
        try: self.__custom_fields["cf_departamento"] = ''
        except: pass
        try: self.__custom_fields["cf_cargo"] = self.contact['title']
        except: pass
        try: self.__custom_fields["cf_email"] = self.contact['email']
        except: pass
        try: self.__custom_fields["cf_linkedin_do_contato"] = self.contact['linkedin_url']
        except: pass
        try: self.__custom_fields["cf_motivo_de_perda"] = ''
        except: pass
        try: self.__card_data["custom_fields"] = [self.__custom_fields]
        except: pass

    def define_user(self):
        wepipe = wepipe_api.Wepipe_Api()
        self.__user = wepipe.get_ountbound_user_id()
        return self.__user
