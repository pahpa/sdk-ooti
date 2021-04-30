import requests
import json


class Auth(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.base_url = 'https://ooti-staging-3.herokuapp.com/api/'  # "https://app.ooti.co/api/"
        self.org_pk = None
        self.teams_pk = None
        self.access_token = None
        self._csrf_token = None
        self.headers = None

    def connect(self):
        self.__get_csrf_token()
        self.__get_token()
        self.__get_org()

##### HELPER #####

    def process_response(self, response, results=None):
        """ Process the response and return it

        :param: reponse is the reponse from the API
        :param: results is saying if we just want the results field of the reponse

        :return: {status, data} or {status} if data is not JSON serializable
        """
        try:
            if(results == None):
                return {'status': response.status_code, 'data': json.loads(response.content)}
            else:
                return {'status': response.status_code, 'data': json.loads(response.content)['results']}
        except ValueError:
            return {'status': response.status_code}
        except KeyError:
            return {'status': response.status_code, 'data': json.loads(response.content)}


##### AUTH #####

    ##### Projects #####


    def get_project_details(self, pk):
        """Get the project details
        Keyword arguments:
        pk -- the pk of the project
        """

        route = 'v1/projects/{0}/'.format(pk)
        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return {'status': response.status_code, 'data': json.loads(response.content)}

    def update_project_details(self, pk, data):
        """Update the project details
        Keyword arguments:
        pk -- the pk of the project
        """

        route = 'v1/projects/{0}/'.format(pk)
        response = requests.patch('{0}{1}'.format(self.base_url, route), headers=self.headers, data=json.dumps(data))
        return {'status': response.status_code, 'data': json.loads(response.content)}

    def get_projects_list(self):
        """Get the project list"""

        route = 'v1/projects/list/{0}/'.format(self.org_pk)
        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return {'status': response.status_code, 'data': json.loads(response.content)['results']}

    #### Organizations ####

    def get_organization_details(self):
        """ Get organization details """

        route = 'v1/organizations/membership/'
        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return {'status': response.status_code, 'data': json.loads(response.content)}

    def __get_org(self):
        """ Set the organization id of the user """

        route = 'v1/organizations/membership/'
        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        self.org_pk = json.loads(response.content)['organizations'][0]['id']
        teams = json.loads(response.content)['organizations'][0]['teams']
        self.teams_pk = []
        for team in range(len(teams)):
            self.teams_pk.append({key: teams[team][key] for key in ('id', 'title')})
        return response.status_code

    #### Token ####

    def __get_token(self):
        route = 'v1/token-auth/'
        headers = {
            'Accept': 'application/json'
        }
        data = {
            'username': self.username,
            'password': self.password
        }
        response = requests.post('{0}{1}'.format(self.base_url, route), headers=headers, data=data)
        self.access_token = json.loads(response.content)['token']
        self.headers = {
            'Authorization': 'JWT {0}'.format(self.access_token),
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-CSRF-Token': self._csrf_token
        }
        return response.status_code

    def __get_csrf_token(self):
        client = requests.session()
        # Retrieve the CSRF token first
        client.get("https://app.ooti.co/accounts/login/")  # sets cookie
        if 'csrftoken' in client.cookies:
            csrftoken = client.cookies['csrftoken']
        else:
            csrftoken = client.cookies['csrf']

        self._csrf_token = csrftoken

    def __refresh_token(self):
        """ Refresh the access token """

        route = 'v1/token-refresh/'
        data = {
            'token': self.access_token
        }
        response = requests.post('{0}{1}'.format(self.base_url, route), headers=self.headers, data=json.dumps(data))
        if response == 201:
            self.headers['Authorization'] = 'JWT {0}'.format(self.access_token)
        return response.status_code

    def __verify_token(self):
        """ Verify if the access token is still valid """

        route = 'v1/token-verify/'
        data = {
            'token': self.access_token
        }
        response = requests.post('{0}{1}'.format(self.base_url, route), headers=self.headers, data=json.dumps(data))
        return response.status_code


##### DELIVERABLES #####

    #### Phases ####


    def get_phase_details(self, pk):
        """Get the phase details
        Keyword arguments:
        pk -- the pk of the phase
        data -- data to update
        """

        route = 'v1/phases/{0}/'.format(pk)
        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return {'status': response.status_code, 'data': json.loads(response.content)}

    def update_phase_details(self, pk, data):
        """Update the phase details
        Keyword arguments:
        pk -- the pk of the phase
        data -- data to update
        """

        route = 'v1/phases/{0}/'.format(pk)
        response = requests.patch('{0}{1}'.format(self.base_url, route), headers=self.headers, data=json.dumps(data))
        return {'status': response.status_code, 'data': json.loads(response.content)}

    def get_phases_list(self, project_pk):
        """Get the phase list
        Keyword arguments:
        project_pk -- the pk of the project
        """

        route = 'v1/phases/list/{0}/'.format(project_pk)
        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return {'status': response.status_code, 'data': json.loads(response.content)['results']}

    #### Annexes ####

    def get_annexes_list(self, project_pk):
        """Get the annexes list

        Keyword arguments:
        project_pk -- the pk of the project
        """

        route = 'v1/annexes/list/{0}/'.format(project_pk)
        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return {'status': response.status_code, 'data': json.loads(response.content)['results']}

    def get_annexe_details(self, pk):
        """Get the annexe details

        Keyword arguments:
        pk -- the pk of the annexe
        """

        route = 'v1/annexes/{0}/'.format(pk)
        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return {'status': response.status_code, 'data': json.loads(response.content)['results']}

    def create_annexe(self, project_pk, data):
        """Create an payment

        Keyword arguments:
        project_pk -- the pk of the project
        data -- data to create
        """

        route = 'v1/annexes/list/{0}/'.format(project_pk)
        parameters = '?phase='
        response = requests.post('{0}{1}'.format(self.base_url, route), headers=self.headers, data=json.dumps(data))

    def update_annexe(self, pk, data):
        """Update the annexe details

        Keyword arguments:
        pk -- the pk of the project
        """

        route = 'v1/annexes/{0}/'.format(pk)
        response = requests.patch('{0}{1}'.format(self.base_url, route), headers=self.headers, data=json.dumps(data))
        return {'status': response.status_code, 'data': json.loads(response.content)}


##### INVOICING #####

    #### Invoices ####


    def get_invoice_details(self, pk):
        """Get the invoice details
        Keyword arguments:
        pk -- the pk of the invoice
        """

        route = 'v1/invoices/{0}/'.format(pk)
        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response)

    def get_invoices_list(self):
        """Get the invoice list"""

        route = 'v1/invoices/list/{0}/?page_size=999999'.format(self.org_pk)
        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response, True)

    def get_invoices_sent_valid_list(self, team_pk):
        """ Get the sent and valid invoice list

        Keyword arguments:

        team_pk -- pk of the team
        """

        route = 'v1/invoices/list/{0}/?team={1}&page_size=999999&q=&is_sent=true&is_valid=true'.format(
            self.org_pk, team_pk)
        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response, True)

    def update_invoice(self, pk, data):
        """Create an invoice
        Keyword arguments:
        pk -- the pk of the invoice
        data -- data to create :
            {
                "invoice_date": "DD-MM-YYYY",
                "billing_option": 0,
                "bank": 0,
                "purchase_order": "string",
                "references": "string",
                "is_valid": Boolean,
                "is_sent": Boolean,
                "multi_tax_enabled": Boolean (if invoice items have multi tax rates)
            }
        """

        route = 'v1/invoices/{0}/'.format(pk)
        response = requests.patch('{0}{1}'.format(self.base_url, route), headers=self.headers, data=json.dumps(data))
        return self.process_response(response)

    def create_invoice(self, team_pk, data):
        """Create an invoice
        Keyword arguments:
        team_pk -- the pk of the team
        data -- data to create :
            {
                "project": 0,
                "type": 0,
                "invoice_date": "DD-MM-YYYY",
                "due_date": "DD-MM-YYYY"
                "client_name": "string",
                "client_address": "string",
                "references": "string"
                "team": 0
            }

            Note that for type 4 (other), project is not mandatory
        """

        route = 'v1/invoices/list/{0}/'.format(self.org_pk)
        parameters = '?team={0}'.format(team_pk)
        response = requests.post('{0}{1}{2}'.format(self.base_url, route, parameters),
                                 headers=self.headers, data=json.dumps(data))
        return self.process_response(response)

    def validate_invoice(self, pk):
        """Validate an invoice
        Keyword arguments:
        pk -- the pk of the invoice
        """
        data = {"is_valid": True}

        route = 'v1/invoices/{0}/'.format(pk)
        response = requests.patch('{0}{1}'.format(self.base_url, route), headers=self.headers, data=json.dumps(data))
        return self.process_response(response)

    def send_invoice(self, pk):
        """Send an invoice
        Keyword arguments:
        pk -- the pk of the invoice
        """
        data = {"is_sent": True}

        route = 'v1/invoices/{0}/'.format(pk)
        response = requests.patch('{0}{1}'.format(self.base_url, route), headers=self.headers, data=json.dumps(data))
        return self.process_response(response)

    def cancel_invoice(self, pk):
        """Cancel an invoice and create a credit note
        Keyword arguments:
        pk -- the pk of the invoice
        """
        data = {"is_closed": True}

        route = 'v1/invoices/{0}/'.format(pk)
        response = requests.patch('{0}{1}'.format(self.base_url, route), headers=self.headers, data=json.dumps(data))

        if(response.status_code == 200):
            response_data = json.loads(response.content)
            credit_note_pk = response_data['credit_note_url'].split('/')[4]
            return {'status': response.status_code, 'data': credit_note_pk}

        return self.process_response(response)

    def get_invoice_items(self, pk):
        """ Get invoice's items

        Keyword arguments:

        pk -- invoice pk
        """

        route = 'v1/invoices/items/{0}/'.format(pk)
        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response)

    def create_invoice_item(self, pk, data):
        """ Create invoice's item

        Keyword Arguments:

        pk -- pk of the invoice
        data -- data to create :
            {
                "descritpion": "string" (title of the item),
                "subtitle": "string" (description of the item),
                "amount": 0,
                "tax_rate": 0.0 (if invoice.multi_tax_rate = True)
                "tax": 0.0 (tax amount, if invoice.multi_tax_rate = True)
            }
        """

        route = 'v1/invoices/items/{0}/'.format(pk)
        response = requests.post('{0}{1}'.format(self.base_url, route), headers=self.headers, data=json.dumps(data))
        return self.process_response(response)

    def update_invoice_item(self, pk, data):
        """ Update invoice's item

        Keyword Arguments:

        pk -- pk of the item
        data -- data to update :
            {
                "descritpion": "string" (title of the item),
                "subtitle": "string" (description of the item),
                "amount": 0
            }
        """

        route = 'v1/invoices/item/{0}/'.format(pk)
        response = requests.patch('{0}{1}'.format(self.base_url, route), headers=self.headers, data=json.dumps(data))
        return self.process_response(response)

    def delete_invoice_item(self, pk):
        """ Update invoice's item

        Keyword Arguments:

        pk -- pk of the item
        """

        route = 'v1/invoices/item/{0}/'.format(pk)
        response = requests.delete('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response)

    #### Credit notes ####

    def get_credit_notes_list(self):
        """Get the invoice list"""

        route = 'v1/invoices/list/{0}/?page_size=999999&type=9'.format(self.org_pk)
        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response, True)

    def get_credit_notes_sent_valid_list(self, team_pk):
        """ Get the sent and valid invoice list

        Keyword arguments:

        team_pk -- pk of the team
        """

        route = 'v1/invoices/list/{0}/?team={1}&page_size=999999&q=&is_sent=true&is_valid=true&type=9'.format(
            self.org_pk, team_pk)
        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response, True)

    #### Payments ####

    def get_payment_details(self, pk):
        """Get the payment details
        Keyword arguments:
        pk -- the pk of the payment
        """

        route = 'v1/payments/{0}'.format(pk)
        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response)

    def get_payments_list(self):
        """Get the payment list"""

        route = 'v1/payments/list/{0}/'.format(self.org_pk)
        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response, True)

    def update_payment(self, pk, data):
        """Create an payment
        Keyword arguments:
        pk -- the pk of the payment
        data -- data to create :
            {
                "date": "DD-MM-YYYY",
                "amount": 0,
                "currency": "string" (currency_pk),
                "currency_rate": 0,
                "type": "string",
                "invoice": "string" (invoice_pk)
                "team": "string" (team_pk),
                "project": "string" (project_pk)
            }
        """

        route = 'v1/payments/{0}/'.format(pk)
        response = requests.patch('{0}{1}'.format(self.base_url, route), headers=self.headers, data=json.dumps(data))
        return self.process_response(response)

    def update_payment_invoice(self, pk, data):
        """ Update payment's amount on invoice

        Please do not call this function before update_payment.
        To make an update on a payment, first use the "update_payment" method.
        Then, update the amount on the invoice with this method.

        Keyword arguments :

        pk -- pk of payment
        data -- data to update :
            {
                "amount": 0
            }
        """
        route = 'v1/payments/invoice/{0}/'.format(pk)
        response = requests.patch('{0}{1}'.format(self.base_url, route), headers=self.headers, data=json.dumps(data))
        return self.process_response(response)

    def create_payment(self, team_pk, data):
        """Create an payment
        Keyword arguments:
        team_pk -- the pk of the team
        data -- data to create :
            {
                "date": "DD-MM-YYYY",
                "amount": 0,
                "currency": "string" (currency_pk),
                "type": "string",
                "invoice": "string" (invoice_pk)
                "team": "string" (team_pk),
                "project": "string" (project_pk) (no need of project for invoices of type 4)
            }
        """

        route = 'v1/payments/list/{0}/'.format(self.org_pk)
        parameters = '?team={0}'.format(team_pk)
        response = requests.post('{0}{1}{2}'.format(self.base_url, route, parameters),
                                 headers=self.headers, data=json.dumps(data))
        return self.process_response(response)

    ##### Clients #####

    def get_clients_list(self, team_pk):
        """Get the clients list

        Keyword arguments:

        pk -- the pk of the team

        """

        route = 'v1/clients/list/{0}/'.format(self.org_pk)
        parameters = '?page_size=999999&team={0}'.format(team_pk)

        response = requests.get('{0}{1}{2}'.format(self.base_url, route, parameters), headers=self.headers)
        return self.process_response(response, True)

    def get_clients_details(self, pk):
        """Get the client details

        Keyword arguments:

        pk -- the pk of the client
        """

        route = 'v1/clients/{0}/'.format(pk)

        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response)

    def create_client(self, data):
        """ Create client

        Keyword arguments:
        data -- data to create, required fields :
            {
                "company_name": "string",
                "number": "string",
                "currency": "string" (currency_pk)
                "billing_address": "string",
                "team": "string",
                "tags": []
            }

        """

        route = 'v1/clients/list/{0}/'.format(self.org_pk)

        response = requests.post('{0}{1}'.format(self.base_url, route), headers=self.headers, data=json.dumps(data))
        return self.process_response(response)

    def update_client(self, pk, data):
        """ Update client

        Keyword arguments:
        pk -- pk of the client
        data -- data to create, required fields :
            {
                "company_name": "string",
                "currency": "string" (currency_pk),
                "number": "string",
                "business_vat_id: "string",
                "billing_address": "string",
                "group": "?"
                "address: "string"
            }
        """
        route = 'v1/clients/{0}/'.format(pk)

        response = requests.patch('{0}{1}'.format(self.base_url, route), headers=self.headers, data=json.dumps(data))
        return self.process_response(response)

    def delete_client(self, pk):
        """ Delete client

        Keyword arguments:
        pk -- pk of the client
        """
        route = 'v1/clients/{0}/'.format(pk)

        response = requests.delete('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response)

    ##### Currencies #####

    def get_currencies_list(self):
        """Get the currencies list """

        route = 'v1/currencies/list/?page_size=200'
        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response, True)

    def get_currency_details(self, pk):
        """ Get the currency details
        Keyword arguments:
        pk -- the pk of the currency
        """

        route = 'v1/currencies/{0}'.format(pk)
        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response)

    def delete_currency(self, pk):
        """ Delete a currency
        Keyword arguments:
        pk -- the pk of the currency
        """

        route = 'v1/currencies/{0}'.format(pk)
        response = requests.delete('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response)

    def create_currency(self, data):
        """ Create a currency

        Keyword arguments:

        data -- data to create, required fields :
            {
                "name": "string",
                "longname": "string",
                "decimal_points": 0,
                "symbol": "string"
            }
        """

        route = 'v1/currencies/list/'
        response = requests.post('{0}{1}'.format(self.base_url, route), headers=self.headers, data=json.dumps(data))
        return self.process_response(response)

    def update_currency(self, pk, data):
        """ Update a currency

        Keyword arguments:

        data -- data to create, required fields :
            {
                "name": "string",
                "longname": "string",
                "decimal_points": 0,
                "symbol": "string"
            }

        pk -- the pk of the currency
        """

        route = 'v1/currencies/{0}/'.format(pk)
        response = requests.patch('{0}{1}'.format(self.base_url, route), headers=self.headers,
                                  data=json.dumps(data))
        return self.process_response(response)

    #### Emails ####

    ### Classic ###

    def get_emails_list(self):
        """Get the emails list"""

        route = 'v1/emails/list/{0}/?page_size=999999'.format(self.org_pk)
        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response, True)

    def get_email_details(self, pk):
        """Get the email details
        Keyword arguments:
        pk -- the pk of the email
        """

        route = 'v1/emails/{0}/'.format(pk)
        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response)

    def create_email(self, team_pk, data):
        """ Create an email

        Keyword arguments:

        team_pk -- the pk of the team
        data -- data to create, fields :
            {
                "team": 0,
                "name": "string", (name of the template)
                "type": "", ('invoice', 'followup' or 'contractor_notification')
                "email_to": "string",
                "email_from": "string",
                "name_from": "string",
                "email_cc": "string",
                "email_bcc": "string",
                "email_subject": "string",
                "email_body": "string",
                "smtp_setting": 0,
                "projects": [],
                "invoices": []
            }

        Note that there is no required fields to create the email template.
        """

        route = 'v1/emails/list/{0}/'.format(self.org_pk)
        response = requests.post('{0}{1}'.format(self.base_url, route), headers=self.headers, data=json.dumps(data))
        return self.process_response(response)

    def update_email(self, pk, data):
        """ Update an email

        Keyword arguments:

        pk -- the pk of the email template
        data -- data to create, fields :
            {
                "team": 0,
                "name": "string", (name of the template)
                "type": "", ('invoice', 'followup' or 'contractor_notification')
                "email_to": "string",
                "email_from": "string",
                "name_from": "string",
                "email_cc": "string",
                "email_bcc": "string",
                "email_subject": "string",
                "email_body": "string",
                "smtp_setting": 0 ,
                "projects": [],
                "invoices": []
            }

        Note that there is no required fields to create the email template.
        """

        route = 'v1/emails/{0}/'.format(pk)
        response = requests.patch('{0}{1}'.format(self.base_url, route), headers=self.headers, data=json.dumps(data))
        return self.process_response(response)

    def delete_email(self, pk):
        """Delete an email

        Keyword arguments:

        pk -- pk of the email
        """
        route = 'v1/emails/{0}'.format(pk)
        response = requests.delete('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response)

    def send_test_email(self, pk):
        """ Send test email to the email of the account

        Keyword arguments:

        pk -- the pk of the email template
        """

        route = 'v1/emails/{0}/send-test/'.format(pk)
        response = requests.post('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response)

    def apply_email(self, pk):
        """ Apply the template to related projects and unsent invoices

        Keyword arguments:

        pk -- pk of the email template
        """
        route = 'v1/emails/{0}/apply/'.format(pk)
        response = requests.post('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response)

    ### smtp ###

    def get_emails_smtp_list(self):
        """Get the emails list"""

        route = 'v1/emails/smtp/list/{0}/?page_size=999999'.format(self.org_pk)
        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response, True)

    def get_email_smtp_details(self, pk):
        """Get the email smtp details
        Keyword arguments:
        pk -- the pk of the email smtp
        """

        route = 'v1/emails/smtp/{0}/'.format(pk)
        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response)

    def create_email_smtp(self, data):
        """ Create an email SMTP

        Keyword Arguments:

        data -- data to create: fields :
           {
               "from_name": "string",
               "from_email": "string",
               "username": "string",
               "password": "string",
               "protocol": "TLS" or "SSL",
               "host": "string",
               "port": 0
           }
        """
        route = 'v1/emails/smtp/list/{0}/'.format(self.org_pk)
        response = requests.post('{0}{1}'.format(self.base_url, route), headers=self.headers, data=json.dumps(data))
        return self.process_response(response)

    def update_email_smtp(self, pk, data):
        """ Update an email SMTP

        Keyword arguments:

        pk -- the pk of the email smtp
        data -- data to create: fields :
           {
               "from_name": "string",
               "from_email": "string",
               "username": "string",
               "password": "string",
               "protocol": "TLS" or "SSL",
               "host": "string",
               "port": 0
           }
        """

        route = 'v1/emails/smtp/{0}/'.format(pk)
        response = requests.patch('{0}{1}'.format(self.base_url, route), headers=self.headers, data=json.dumps(data))
        return self.process_response(response)

    def delete_email_smtp(self, pk):
        """Delete an email smtp

        Keyword arguments:

        pk -- pk of the email smtp
        """
        route = 'v1/emails/smtp/{0}'.format(pk)
        response = requests.delete('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response)

    def send_test_email_smtp(self, pk):
        """ Verify the status of the smtp

        Keyword arguments:

        pk -- the pk of the email template
        """

        route = 'v1/emails/smtp/{0}/send-test/'.format(pk)
        response = requests.post('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response)

    #### Files ####

    ### Folders ###

    def get_folder_list(self, project_pk):
        """Get the folder list

        Keyword arguments:

        project_pk -- pk of the project
        """

        route = 'v1/files/folder/list/{0}/?page_size=999999'.format(project_pk)
        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response, True)

    def get_folder_details(self, pk):
        """Get the folder details

        Keyword arguments:

        pk -- pk of the folder
        """

        route = 'v1/files/folder/{0}/'.format(pk)
        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response)

    def create_folder(self, project_pk, data):
        """ Create a folder

        Keyword arguments:

        project_pk -- pk of the project
        data -- data to be created :
            {
                "name": "string",
                "name_en": "string",
                "name_fr": "string",
                "parent": 0
            }
        """
        route = 'v1/files/folder/list/{0}/'.format(project_pk)
        response = requests.post('{0}{1}'.format(self.base_url, route), headers=self.headers, data=json.dumps(data))
        return self.process_response(response)

    def update_folder(self, pk, data):
        """ Update a folder

        Keyword arguments:

        pk -- pk of the folder
        data -- data to be updated :
            {
                "name": "string",
                "name_en": "string",
                "name_fr": "string",
                "parent": 0
            }
        """
        route = 'v1/files/folder/{0}/'.format(pk)
        response = requests.patch('{0}{1}'.format(self.base_url, route), headers=self.headers, data=json.dumps(data))
        return self.process_response(response)

    def delete_folder(self, pk):
        """ Delete a folder

        Keyword arguments:

        pk -- pk of the folder
        """
        route = 'v1/files/folder/{0}/'.format(pk)
        response = requests.delete('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response)

    ### Files ###

    def get_files_list(self, project_pk):
        """Get the files list

        Keyword arguments:

        project_pk -- pk of the project
        """

        route = 'v1/files/list/{0}/?page_size=999999'.format(project_pk)
        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response, True)

    def get_file_details(self, pk):
        """Get the file details

        Keyword arguments:

        pk -- pk of the file
        """

        route = 'v1/files/{0}/'.format(pk)
        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response)

    def delete_file(self, pk):
        """ Delete a file

        Keyword arguments:

        pk -- pk of the file
        """

        route = 'v1/files/{0}/'.format(pk)
        response = requests.delete('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response)

    #### Banks ####

    def get_banks_list(self):
        """Get the banks list """

        route = 'v1/banks/list/{0}/?page_size=999999'.format(self.org_pk)
        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response, True)

    def get_bank_details(self, pk):
        """Get the bank details

        Keyword arguments:

        pk -- pk of the bank
        """

        route = 'v1/banks/{0}/'.format(pk)
        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response)

    def create_bank(self, data):
        """ Create a bank

        Keyword arguments:

        data -- data to be created :
            {
                "name": "string",
                "currency": 0,
                "country": "string",
                "iban": "string",
                "bic": "string",
                "rib": "string",
                "teams": ["string"]
                "projects": ["string"]
            }
        """
        route = 'v1/banks/list/{0}/'.format(self.org_pk)
        response = requests.post('{0}{1}'.format(self.base_url, route), headers=self.headers, data=json.dumps(data))
        return self.process_response(response)

    def update_bank(self, pk, data):
        """ Create a bank

        Keyword arguments:

        data -- data to be created :
            {
                "name": "string",
                "currency": 0,
                "country": "string",
                "iban": "string",
                "bic": "string",
                "rib": "string",
                "teams": ["string"]
                "projects": ["string"]
            }
        """
        route = 'v1/banks/{0}/'.format(pk)
        response = requests.patch('{0}{1}'.format(self.base_url, route), headers=self.headers, data=json.dumps(data))
        return self.process_response(response)

    def delete_bank(self, pk):
        """ Create a bank

        Keyword arguments:

        pk -- pk of the bank
        """
        route = 'v1/banks/{0}/'.format(pk)
        response = requests.delete('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response)

    #### Reports ####

    ### Reports ###

    def get_reports_list(self):
        """Get the reports list """

        route = 'v1/reports/list/{0}/?page_size=999999'.format(self.org_pk)
        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response, True)

    def get_reports_project_list(self, project_pk):
        """Get the reports list for a project"""

        route = 'v1/reports/list/{0}/?page_size=999999&project={1}'.format(self.org_pk, project_pk)
        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response, True)

    def get_report_details(self, pk):
        """Get the report details

        Keyword arguments:

        pk -- pk of the report
        """

        route = 'v1/reports/{0}/'.format(pk)
        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response)

    def create_report(self, data):
        """ Create a report

        Keyword arguments:

        data -- data to be created :
        {
            "name": "string", (required)
            "project": 0, (required)
            "type": "string", (required)
            "status": "string",
            "styleguide": 0,
            "lang": "string",
            "orientation": "string",
            "filter_team": 0,
            "footer_team": 0,
            "font_size": 0,
            "margin_left": 0,
            "margin_right": 0,
            "cover_body_template": "string",
            "report_body_template": "string",
            "use_cover_page": true,
            "year": 0,
            "date_range": "string",
            "is_custom_date_range": true,
            "start_date": "string",
            "end_date": "string",
            "phase": 0,
            "annex": 0,
            "orguser": 0,
            "scheduled_recipients": [
                "string"
            ],
            "scheduled_guests": "string",
            "scheduled_sent_at": "string",
            "scheduled_start_date": "string",
            "scheduled_next_date": "string",
            "scheduled_last_sent": "string",
            "scheduled_count": 0,
            "scheduled_frequency": 0,
            "hide_currency": true,
            "notes": "string"
        }

        Note: You can create a report without "type", but this will create a blank page.
        """
        route = 'v1/reports/list/{0}/'.format(self.org_pk)
        response = requests.post('{0}{1}'.format(self.base_url, route), headers=self.headers, data=json.dumps(data))
        return self.process_response(response)

    def update_report(self, pk, data):
        """ Update a report

        Keyword arguments:

        pk -- pk of the report
        data -- data update:
        {
            "name": "string", (required)
            "styleguide": 0,
            "lang": "string",
            "orientation": "string",
            "footer_team": 0,
            "font_size": 0,
            "margin_left": 0,
            "margin_right": 0,
            "use_cover_page": true,
            "scheduled_recipients": [
                "string"
            ],
            "scheduled_start_date": "string",
            "scheduled_frequency": 0,
        }

        Note: You can create a report without "type", but this will create a blank page.
        """
        route = 'v1/reports/{0}/'.format(pk)
        response = requests.patch('{0}{1}'.format(self.base_url, route), headers=self.headers, data=json.dumps(data))
        return self.process_response(response)

    def delete_report(self, pk):
        """ Delete a report

        Keyword arguments:

        pk -- pk of the report
        """
        route = 'v1/reports/{0}/'.format(pk)
        response = requests.delete('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response)

    def generate_report(self, data):
        """ Generate a report (already created)

        Keyword arguments:

        data -- data to be created:
            {
                "pk": 0 (pk of the report),
                "project": 0 (project linked to the report)
            }
        """
        route = 'v1/reports/generate/{0}'.format(self.org_pk)
        response = requests.post('{0}{1}'.format(self.base_url, route), headers=self.headers, data=json.dumps(data))
        return self.process_response(response)

    ### Templates ###

    def get_templates_list(self, team_pk):
        """ Get list of templates

        Keyword arguments:

        team_pk -- pk of the team
        """

        route = 'v1/reports/templates/list/{0}/'.format(team_pk)
        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response, True)

    def get_template_details(self, pk):
        """Get the template details

        Keyword arguments:

        pk -- pk of the template
        """

        route = 'v1/reports/templates/{0}/'.format(pk)
        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response)

    def create_template(self, team_pk, data):
        """ Create a template

        Keyword arguments:

        team_pk -- pk of the team
        data -- data create:
            {
                "name": "string", (required)
                "type": "string", (required: "proprosal" or "progress")
                "styleguide": 0,
                "lang": "string", (required: "fr", "en", "it") 
                "orientation": "string", (portrait, landscape)
                "font_size": 0,
                "margin_top": 0,
                "margin_bottom": 0,
                "margin_left": 0,
                "margin_right": 0
            }
            """

        route = 'v1/reports/templates/list/{0}/'.format(team_pk)
        response = requests.post('{0}{1}'.format(self.base_url, route), headers=self.headers, data=json.dumps(data))
        return self.process_response(response)

    def update_template(self, pk, data):
        """ Update a template

        Keyword arguments:

        pk -- pk of the template
        data -- data update:
            {
                "name": "string", (required)
                "type": "string", (required: "proprosal" or "progress")
                "styleguide": 0,
                "lang": "string", (required: "fr", "en", "it") 
                "orientation": "string", (portrait, landscape)
                "font_size": 0,
                "margin_top": 0,
                "margin_bottom": 0,
                "margin_left": 0,
                "margin_right": 0
            }
            """

        route = 'v1/reports/templates/{0}/'.format(pk)
        response = requests.patch('{0}{1}'.format(self.base_url, route), headers=self.headers, data=json.dumps(data))
        return self.process_response(response)

    def delete_template(self, pk):
        """ Delete a template

        Keyword arguments:

        pk -- pk of the template
         """

        route = 'v1/reports/templates/{0}/'.format(pk)
        response = requests.delete('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response)

    def duplicate_template(self, pk):
        """ Duplicate a template

        Keyword arguments:

        pk -- pk of the template
         """

        route = 'v1/reports/templates/duplicate/{0}/'.format(pk)
        response = requests.post('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response)

    #### Revenue ####
    # TODO : To be completed later
    def get_revenue_list(self):
        """Get the revenue list """

        route = 'v1/revenue/list/{0}/?page_size=999999'.format(self.org_pk)
        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response, True)

    def get_revenue_details(self, pk):
        """Get the revenue details

        Keyword arguments:

        pk -- pk of the revenue
        """

        route = 'v1/revenue/{0}/'.format(pk)
        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response)

    def create_revenue(self, data):
        """ Create a template

        Keyword arguments:

        team_pk -- pk of the team
        data -- data create:
            {
                "amount_actual": 0,
                "amount_budgeted": 0,
                "description": "string",
                "type": "string",
                "month": 0,
                "title": "string",
                "year": 0,
                "team": 0,
                "project": 0,
                "months": [
                    "string"
                ]
            }
            """

        route = 'v1/revenue/list/{0}/'.format(self.org_pk)
        response = requests.post('{0}{1}'.format(self.base_url, route), headers=self.headers, data=json.dumps(data))
        return self.process_response(response)

    #### Styleguides ####

    def get_styleguides_list(self):
        """Get the styleguide list """

        route = 'v1/styleguides/list/{0}/?page_size=999999'.format(self.org_pk)
        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response, True)

    def get_styleguide_details(self, pk):
        """Get the styleguide details

        Keyword arguments:

        pk -- pk of the styleguide
        """

        route = 'v1/styleguides/{0}/'.format(pk)
        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response)

    def create_styleguide(self, data):
        """ Create a styleguide

        Keyword arguments:

        data -- data create:
            {
                "name": "string"
            }
        """

        route = 'v1/styleguides/list/{0}/'.format(self.org_pk)
        response = requests.post('{0}{1}'.format(self.base_url, route), headers=self.headers, data=json.dumps(data))
        return self.process_response(response)

    def update_styleguide(self, pk, data):
        """ Update a styleguide

        Keyword arguments:

        pk -- pk of the styleguide
        data -- data create:
            {
                "name": "string",
                "type": "string" ("all", "report", "invoice", "proposal"),
                "font_color": "string",
                "font": "string",
                "font_size": "string",
                "margin_left": 0,
                "margin_right": 0
            }
        """

        route = 'v1/styleguides/{0}/'.format(pk)
        response = requests.patch('{0}{1}'.format(self.base_url, route), headers=self.headers, data=json.dumps(data))
        return self.process_response(response)

    def delete_styleguide(self, pk):
        """ Delete a styleguide

        Keyword arguments:

        pk -- pk of the styleguide
        """

        route = 'v1/styleguides/{0}/'.format(pk)
        response = requests.delete('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return self.process_response(response)


##### COSTS #####

    #### Expenses ####

    def get_expenses_list(self):
        """ Get the expenses list """

        route = 'v1/expenses/list/{0}/'.format(self.org_pk)
        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return {'status': response.status_code, 'data': json.loads(response.content)['results']}

    def get_expenses_details(self, pk):
        """Get the expense details

        Keyword arguments:

        pk - - the pk of the expense
        """

        route = 'v1/expenses/{0}'.format(pk)
        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return {'status': response.status_code, 'data': json.loads(response.content)}


##### COLLABORATION #####

    #### Contact ####

    def get_contacts_list(self, project_pk=None):
        """ Get the contacts list

        project_pk - - the pk of the contacts' project(optional)
        """

        route = 'v1/contacts/list/{0}/'.format(self.org_pk)
        if project_pk is not None:
            route += '{0}/'.format(project_pk)
        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return {'status': response.status_code, 'data': json.loads(response.content)['results']}

    def get_contact_details(self, pk):
        """ Get the contact details

        Keywords arguments:
        pk - - the pk of the contact
        """

        route = 'v1/contacts/{0}/'.format(pk)
        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return {'status': response.status_code, 'data': json.loads(response.content)}

    def update_contact_details(self, pk, data):
        """ Update the contact details

        Keywords arguments:
        pk - - the pk of the contact
        data - - data to update, example value:
        {
            "name": "string",
            "first_name": "string",
            "last_name": "string",
            "email": "string",
            "mobile_phone": "string",
            "office_phone": "string",
            "home_phone": "string",
            "fax": "string",
            "website": "string",
            "street1": "string",
            "postal_code1": "string",
            "city1": "string",
            "province1": "string",
            "country1": "string",
            "job_title": "string",
            "client": [(ids of the clients associated with this contact)
                "string"
            ]
        }
        """

        route = 'v1/contacts/{0}/'.format(pk)
        response = requests.patch('{0}{1}'.format(self.base_url, route), headers=self.headers, data=json.dumps(data))
        return {"status": response.status_code, "data": json.loads(response.content)}

    def create_contact(self, data, project_pk=None):
        """ Create contact

        Keywords arguments:
        project_pk - - the pk of the contact's project(optional)
        data - - data to create:
            {
                "name": "string" (required),
                "first_name": "string" (optional),
                "last_name": "string" (optional),
                "email": "string" (optional),
                "mobile_phone": "string" (optional),
                "job_title": "string" (optional)
            }
        """

        route = 'v1/contacts/list/{0}/'.format(self.org_pk)
        if project_pk is not None:
            route += '{0}/'.format(project_pk)
        response = requests.post('{0}{1}'.format(self.base_url, route), headers=self.headers, data=json.dumps(data))
        if(response.status_code != 500):
            return {'status': response.status_code, 'data': json.loads(response.content)['results']}
        else:
            return {'status': response.status_code}

    def delete_contact(self, pk):
        """ Delete the contact

        Keywords arguments:
        pk - - the pk of the contact
        """

        route = 'v1/contacts/{0}/'.format(pk)
        response = requests.delete('{0}{1}'.format(self.base_url, route), headers=self.headers)
        if(response.status_code == 204):
            return {'status': response.status_code, 'data': 'Contact deleted'}
        else:
            return {'status': response.status_code, 'data': json.loads(response.content)}

    #### Task ####

    def get_tasks_list(self):
        """ Get the tasks list """

        route = 'v1/tasks/list/{0}/'.format(self.org_pk)
        response = requests.get('{0}{1}'.format(self.base_url, route), headers=self.headers)
        return {'status': response.status_code, 'data': json.loads(response.content)}


##### TIME #####


##### SETTINGS #####


##### RANDOM #####
