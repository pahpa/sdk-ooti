from requests.models import Response
from ooti import ooti

OOTI_USERNAME = 'root@root.com'
OOTI_PASSWORD = 'root'

sdk = ooti.Auth(OOTI_USERNAME, OOTI_PASSWORD)
sdk.connect()


def UserFactory():
    response = sdk.get_profile_details()
    return response['data']['user']


def OrguserFactory(user=None):
    """
    if not user:
        user = UserFactory()
    payload = {
        'email': 'test@test.fr',
        'timeoff_validators': [],
        'time_validators': [],
        'expenses_validators': [],
        'tags': [],
    }
    response = sdk.create_orguser(payload)
    if response['status'] == 201:
        return response['data']
    else:
        print(response)
        return None
    """
    return {'id': 2}


def TeamFactory():
    response = sdk.get_profile_details()
    return response['data']['selected_team']


def CostFactory(team_pk=None):
    if not team_pk:
        team_pk = TeamFactory()
    payload = {
        'amount_actual': 10,
        'amount_budgeted': 0,
        'description': 'string',
        'type': 'monthly',
        'title': 'string',
        'year': 0,
        'team': team_pk,
        'months': []
    }
    response = sdk.Costs.create_cost(payload)
    if response['status'] == 201:
        return response['data']
    else:
        return None


def CostMonthFactory(team_pk=None, cost_id=None):
    if not team_pk:
        team_pk = TeamFactory()
        cost_id = CostFactory(team_pk)['id']
    elif not cost_id:
        cost_id = CostFactory(team_pk)
    payload = {
        'fixed_cost': cost_id,
        'team': team_pk,
        'amount_budgeted': 120,
        'amount_actual': 100,
        'year': 2020,
        'month': 3
    }
    response = sdk.Costs.create_costs_month(payload)
    if response['status'] == 201:
        return response['data']
    else:
        return None


def EmployeeContractFactory(orguser_pk=None, team_pk=None):
    if not orguser_pk:
        orguser_pk = OrguserFactory()['id']
    if not team_pk:
        team_pk = TeamFactory()
    payload = {
        'orguser': orguser_pk,
        'team': team_pk,
        'status': 'active',
        'end_date': '20-10-2022',
    }
    response = sdk.Costs.create_employees_contract(payload)
    if response['status'] == 201:
        return response['data']
    else:
        return None


def EmployeePeriodFactory(employee_contract_pk=None):
    if not employee_contract_pk:
        employee_contract_pk = EmployeeContractFactory()['id']
    payload = {
        'contract': employee_contract_pk,
        'notes': 'some notes',
        'start_date': '09-05-2021',
        'end_date': '20-05-2021',
        'status': 'active',
        'salary_daily_gross': 100,
        'salary_hourly_gross': 10,
        'salary_gross_coefficent': 1,
        'salary_monthly_net': 1200,
        'salary_monthly_gross': 1500,
        'salary_loaded_coefficent': 0,
        'weekly_hours_limit': 30,
        'daily_hours_limit': 5,
        'overtime_enabled': True,
        'overtime_hours_limit': 5,
        'days_per_week': 6
    }
    response = sdk.Costs.create_employees_period(payload)
    if response['status'] == 201:
        return response['data']
    else:
        return None


def FreelancerFactory():
    payload = {
        'name': 'test freelancer'
    }
    response = sdk.Costs.create_freelancer(payload)
    if response['status'] == 201:
        return response['data']
    else:
        return None


def ExpenseGroupFactory(team_pk):
    if not team_pk:
        team_pk = TeamFactory()
    payload = {
        'description': 'expense group test'
    }
    response = sdk.Costs.create_expenses_group(payload, team_pk=team_pk)
    if response['status'] == 201:
        return response['data']
    else:
        return None
