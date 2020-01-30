__author__ = 'Ivashko'
import locale
enc = locale.getpreferredencoding()
from erp.employee_management.models import Employee
from erp.customer_management.models import Customer
from django import template
register = template.Library()

@register.filter(name='count_of_employees')
def count_of_employees(value):
    """
    Count of employees
    """
    return Employee.objects.all().count()

@register.filter(name='count_of_customers')
def count_of_customers(value):
    """
    Count of customers
    """
    return Customer.objects.all().count()