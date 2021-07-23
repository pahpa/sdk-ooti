import random
import string
import time


class TestHelper:
    """ TestHelper class 

    Create all needed object to do tests
    """

    def __init__(self, my_account):
        self.my_account = my_account

    def _create_currency_if_none(self):
        currency_pk = -1
        currencies = self.my_account.Invoicing.get_currencies_list()['data']

        if len(currencies) == 0:
            data_currency = {
                "name": "usd",
                "longname": "United States Dollar",
                "symbol": "$",
            }

            res = self.my_account.Invoicing.create_currency(data_currency)
            currency_pk = res['data']['pk']
        else:
            currency_pk = currencies[0]['pk']

        return currency_pk

    def _create_currency_return_pk(self):
        """
        Generate a currency with random name
        """
        name = ''
        for i in range(6):
            name += random.choice(string.ascii_letters)
            time.sleep(0.1)

        data_currency = {
            "name": name,
            "longname": "longname",
            "symbol": "$",
        }

        res = self.my_account.Invoicing.create_currency(data_currency)
        if res['status'] == 201:
            currency_pk = res['data']['pk']
            return currency_pk
        else:
            self._create_currency_return_pk()

    def _create_client_return_pk(self, team_pk, currency_pk):
        """ Create client and return pk

        :return: client_pk
        """

        data_client = {
            "name": "UNITTEST",
            "number": "0001",
            "currency": currency_pk,
            "team": team_pk,
            "tags": [],
        }

        client = self.my_account.Invoicing.create_client(data_client)
        return client['data']['pk']

    def _create_project_return_pk(self, client_pk, currency_pk):
        """ Create project and return pk
        TODO: 500

        :return: project_pk
        """

        data_project = {
            "client": client_pk,
            "currency": currency_pk,
            "project_title": "UNITTEST-test",
            "start_date": "01-07-2021",
            "end_date": "23-07-2021",
        }

        res = self.my_account.create_project(data_project)
        print(res)
        return res['data']['pk']

    def _create_invoice_return_pk(self, team_pk, project_pk):
        """ Create and return the pk of an invoice 

        It creates 
        """

        invoice = {
            "project": project_pk,
            "invoice_date": '19-04-2021',
            "due_date": '19-05-2021',
            "references": "UNITTEST ref",
            "type": 4
        }

        invoice_pk = self.my_account.Invoicing.create_invoice(team_pk, invoice)['data']['pk']
        return invoice_pk

    def _create_invoice_item_return_pk(self, invoice_pk):
        data_invoice_item = {
            "description": "UNITTEST ITEM",
            "subtitle": "My subtitle",
            "amount": 1000
        }

        res = self.my_account.Invoicing.create_invoice_item(invoice_pk, data_invoice_item)
        return res['data']['pk']

    def _create_payment_return_pk(self, team_pk, invoice_pk, currency_pk):
        """ Create payment
        Create an invoice, an item invoice, validate the invoice and then a payment. 

        :return: pk of payment
        """

        invoice_item = {
            "description": "UNITTEST ITEM",
            "subtitle": "My subtitle",
            "amount": 1000
        }

        res_creation_item = self.my_account.Invoicing.create_invoice_item(invoice_pk, invoice_item)
        self.my_account.Invoicing.validate_invoice(invoice_pk)

        payment = {
            "date": "21-04-2021",
            "amount": 100,
            "currency": currency_pk,
            "invoice": invoice_pk,
            "team": team_pk
        }

        res_creation_payment = self.my_account.Invoicing.create_payment(team_pk, payment)
        payment_pk = res_creation_payment['data']['pk']

        return payment_pk

    def _create_email_return_pk(self):
        """ Create an email template and return the pk """

        email = {
            "name": "UNITTEST",
            "email_subject": "UNITTEST",
            "email_body": "UNITTEST",
            "email_to": "test@ooti.co",
            "email_from": "test@ooti.co",
            "name_from": "Test de OOTI"
        }

        email_pk = self.my_account.Invoicing.create_email(email)['data']['id']
        return email_pk

    def _create_email_smtp_return_pk(self):
        """ Create email smtp and return pk """

        data = {
            "from_name": "UNITTEST",
            "from_email": "UNITTEST",
            "username": "UNITTEST",
            "password": "UNITTEST",
            "protocol": "TLS",
            "host": "UNITTEST",
            "port": 0
        }

        smtp_pk = self.my_account.Invoicing.create_email_smtp(data)['data']['id']
        return smtp_pk

    def _create_folder_return_pk(self, project_pk):
        """ Create a folder and return the pk """

        name = self.create_name()

        folder = {
            "name": name
        }

        folder_pk = self.my_account.Invoicing.create_folder(project_pk, folder)['data']['pk']
        return folder_pk

    def _create_file_return_pk(self, project_pk, folder_pk):
        """ Test that 200 is returned """

        name = self.create_name()

        data = {
            "name": name,
            "file": "README.md",
            "folder": folder_pk,
        }

        res = self.my_account.Invoicing.create_file(project_pk, data)
        if res['status'] == 201:
            return res['data']['pk']
        elif 'non_field_errors' in res['data'] and res['data']['non_field_errors'] == ['The fields folder, name must make a unique set.']:
            self._create_file_return_pk(project_pk, folder_pk)

    def _create_bank_return_pk(self, team_pk, project_pk, currency_pk):

        name = self.create_name()

        data = {
            "name": name,
            "currency": currency_pk,
            "country": "FR",
            "iban": "XXX-{0}".format(name),
            "bic": "XXX-{0}".format(name),
            "rib": "XXX-{0}".format(name),
            "teams": [str(team_pk)],
            "projects": [str(project_pk)]
        }

        res = self.my_account.Invoicing.create_bank(data)
        return res['data']['id']

    def _create_area_return_pk(self, project_pk):
        """ Create an area and return the pk """

        name = self.create_name()

        area = {
            "name": name,
            "project": project_pk,
            "surface_area": 30,
            "zones": []
        }

        res = self.my_account.Deliverables.create_areas(project_pk, area)
        return res['data']['id']

    def _create_zone_return_pk(self, area_pk):
        """ Create a zone and return the pk
        """

        data = {
            "name": self.create_name(),
            "area": area_pk,
            "progress": 0,
            "internal_code": "string",
            "client_code": "string",
            "surface_area": 0,
            "default_surface_price": 0,
            "num_units": 0
        }

        return self.my_account.Deliverables.create_zone(area_pk, data)['data']['id']

    def _create_fee_project_return_pk(self, project_pk):
        """ Create a fee project and return pk """

        data = {
            "title": self.create_name(),
            "project": project_pk
        }

        return self.my_account.Deliverables.create_fee_project(data)['data']['id']

    def _create_phase_return_pk(self, project_pk, fee_project_pk):
        """ Create phase and return pk """

        data = {
            "name": self.create_name(),
            "shortname": "TEST",
            "fee_project": fee_project_pk,
            "pct": 10,
            "dependants": []
        }

        return self.my_account.Deliverables.create_phase(project_pk, data)['data']['id']

    def _create_plan_return_pk(self, project_pk):
        """ Create plan and return pk """

        data = {
            "name_fr": self.create_name(),
            "plan_format": "A1",
            "scale": "1/50e",
            "level": "000",
            "lot": 10,
            "code": "pln",
            "org": self.my_account.org_pk
        }

        return self.my_account.Deliverables.create_plan(project_pk, data)['data']['id']

    def _create_milestone_return_pk(self, project_pk):
        """ Create a milestone and return the pk """

        data = {
            "title": self.create_name(),
            "project": project_pk,
            "date": "30-04-2021",
            "description": "string",
            "in_timeline": True
        }

        return self.my_account.Deliverables.create_milestone(data)['data']['pk']

    def _create_phaseset_return_pk(self, team_pk):
        """ Create a phaseset and return pk """
        data = {
            "is_main": False,
            "title": self.create_name(),
            "team": team_pk
        }

        return self.my_account.Deliverables.create_defaults_phasesets_org(data)['data']['id']

    def _create_defaults_phase_return_pk(self, team_pk, phaseset_pk):
        """ Create a default phase and return it """

        data = {
            "name": "UNITTEST",
            "shortname": "TEST",
            "pct": 10,
            "library": phaseset_pk,
            "team": team_pk
        }

        return self.my_account.Deliverables.create_defaults_phase_org(data)['data']['id']

    def _create_plansets_return_pk(self):
        """ Create a plansets and return pk """

        data = {
            "title": self.create_name()
        }

        return self.my_account.Deliverables.create_defaults_plansets_org(data)['data']['id']

    def _create_defaults_plan_return_pk(self, plansets_pk, zone_pk):
        """ Create a default plan and return it 

        :return: {'pk': pk, "plansets_pk": plansets_pk, "zone_pk": res_zone_pk['pk'], "area_pk": res_zone_pk['area_pk']}
        """

        data = {
            "zone": zone_pk,
            "plan_format": "string",
            "scale": "string",
            "level": "string",
            "name": self.create_name(),
            "library": plansets_pk
        }

        return self.my_account.Deliverables.create_defaults_plan_org(data)['data']['id']

    def _create_contractor_return_pk(self):
        """ Create contractor and return pk """

        data = {
            "name": self.create_name(),
            "tags": []
        }

        return self.my_account.Deliverables.create_contractors(data)['data']['id']

    def _create_contract_return_pk(self, contractor_pk, project_pk, fee_project_pk):
        """ Create contract and return pk """

        data = {
            "contractor": contractor_pk,
            "fee_project": fee_project_pk,
            "type": "sub",
            "description": "string",
            "tax_rate": 1,
            "project": project_pk,
        }

        return self.my_account.Deliverables.create_contract(data)['data']['id']

    def _create_contract_item_return_pk(self, contract_pk):
        """ Create a contract item and return pk """

        data = {
            "contract": contract_pk,
            "fee": 100
        }

        return self.my_account.Deliverables.create_contracts_items(data)['data']['id']

    def _create_contract_month_return_pk(self, contract_pk):
        """ Create contract month return pk """

        data = {
            "contract": contract_pk,
            "year": 2021,
            "month": 5,
            "start_date": "06-05-2021",
            "end_date": "06-05-2021",
            "budget": 0,
            "budget_projected": 0,
            "actual": 0,
            "pct": 0
        }

        return self.my_account.Deliverables.create_contracts_month(data)['data']['id']

    def _create_annex_return_pk(self, project_pk):
        """ Create annexe and return pk """

        data = {
            "title": self.create_name(),
            "annex_type": "time",
            "total_fees": 1,
            "description": "UNITTEST",
            "date": "06-05-2021"
        }

        return self.my_account.Deliverables.create_annexe(project_pk, data)['data']['id']

    def _create_document_return_pk(self, project_pk):
        """ Create a document a return pk """

        data = {
            "name": self.create_name(),
            "price": 10,
            "annexes": []
        }

        return self.my_account.Deliverables.create_document(project_pk, data)['data']['id']

    def _create_fee_return_pk(self, project_pk):
        """ Create a fee and return pk """

        data = {
            "title": self.create_name(),
            "amount_base": 0,
            "amount_current": 0,
            "progress": 0,
            "in_timeline": True
        }

        return self.my_account.Deliverables.create_fee(project_pk, data)['data']['pk']

    def create_name(self):
        name = ''
        for i in range(6):
            name += random.choice(string.ascii_letters)
            time.sleep(0.1)
        name += '_UNITTEST'
        return name
