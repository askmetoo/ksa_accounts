# Copyright (c) 2022, Havenir Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils.data import getdate


def execute(filters=None):
	columns, data = get_columns(), get_data(filters)
	return columns, data


def get_data(filters):
	data = []
	# Sales Heading
	grand_total_taxable_amount = 0
	grand_total_taxable_adjustment_amount = 0
	grand_total_tax = 0
	append_data(data, 'VAT on Sales', '', '', '')

	# Getting Sales
	sales_accounts = get_accounts('Sales')
	sales_data = {}
	for account in sales_accounts:
		if account.ksa_account_title in sales_data:
			# Get Amounts and adjustments
			result = get_account_value(filters, account.name)
			sales_data[account.ksa_account_title]['amount'] += result['credit']
			sales_data[account.ksa_account_title]['adjustment'] += result['debit']
		else:
			# Get Amounts and adjustments
			result = get_account_value(filters, account.name)
			sales_data[account.ksa_account_title] = {
				'amount': result['credit'],
				'adjustment': result['debit'],
				'vat': 0
			}

	# Gettings VAT on Sales
	vat_sales_accounts = get_accounts('VAT on Sales')
	for account in vat_sales_accounts:
		if account.ksa_account_title in sales_data:
			# Get VAT
			result = get_account_value(filters, account.name)
			sales_data[account.ksa_account_title]['vat'] += result['credit']
			sales_data[account.ksa_account_title]['vat'] -= result['debit']
		else:
			# Get VAT
			result = get_account_value(filters, account.name)
			sales_data[account.ksa_account_title] = {
				'vat': result['credit']
			}
			sales_data[account.ksa_account_title]['vat'] -= result['debit']

	for key, value in sales_data.items():
		if 'amount' not in value:
			value['amount'] = 0
		if 'adjustment' not in value:
			value['adjustment'] = 0
		if 'vat' not in value:
			value['vat'] = 0

		append_data(data, key, value['amount'], value['adjustment'], value['vat'])
		grand_total_taxable_amount += value['amount']
		grand_total_taxable_adjustment_amount += value['adjustment']
		grand_total_tax += value['vat']

	# Sales Grand Total
	append_data(
		data,
		'Grand Total',
		grand_total_taxable_amount,
		grand_total_taxable_adjustment_amount,
		grand_total_tax)

	# Blank Line
	append_data(data, '', '', '', '')

	# Purchase Heading
	grand_total_taxable_amount = 0
	grand_total_taxable_adjustment_amount = 0
	grand_total_tax = 0
	append_data(data, 'VAT on Purchases', '', '', '')

	# Getting Purchases
	purchases_accounts = get_accounts('Purchases')
	purchases_data = {}
	for account in purchases_accounts:
		if account.ksa_account_title in purchases_data:
			# Get Amounts and adjustments
			result = get_account_value(filters, account.name)
			purchases_data[account.ksa_account_title]['amount'] += result['debit']
			purchases_data[account.ksa_account_title]['adjustment'] += result['credit']
		else:
			# Get Amounts and adjustments
			result = get_account_value(filters, account.name)
			purchases_data[account.ksa_account_title] = {
				'amount': result['debit'],
				'adjustment': result['credit'],
				'vat': 0
			}

	# Gettings VAT on Purchases
	vat_purchases_accounts = get_accounts('VAT on Purchases')
	for account in vat_purchases_accounts:
		if account.ksa_account_title in purchases_data:
			# Get VAT
			result = get_account_value(filters, account.name)
			purchases_data[account.ksa_account_title]['vat'] += result['debit']
			purchases_data[account.ksa_account_title]['vat'] -= result['credit']
		else:
			# Get VAT
			result = get_account_value(filters, account.name)
			purchases_data[account.ksa_account_title] = {
				'vat': result['debit']
			}
			purchases_data[account.ksa_account_title]['vat'] -= result['credit']

	for key, value in purchases_data.items():
		if 'amount' not in value:
			value['amount'] = 0
		if 'adjustment' not in value:
			value['adjustment'] = 0
		if 'vat' not in value:
			value['vat'] = 0

		append_data(data, key, value['amount'], value['adjustment'], value['vat'])
		grand_total_taxable_amount += value['amount']
		grand_total_taxable_adjustment_amount += value['adjustment']
		grand_total_tax += value['vat']

	# Purchase Grand Total
	append_data(
		data,
		'Grand Total',
		grand_total_taxable_amount,
		grand_total_taxable_adjustment_amount,
		grand_total_tax)

	return data


def get_columns():
	return [
		{
			"fieldname": "title",
			"label": _("Title"),
			"fieldtype": "Data",
			"width": 300
		},
		{
			"fieldname": "amount",
			"label": _("Amount (SAR)"),
			"fieldtype": "Currency",
			"width": 150,
		},
		{
			"fieldname": "adjustment_amount",
			"label": _("Adjustment (SAR)"),
			"fieldtype": "Currency",
			"width": 150,
		},
		{
			"fieldname": "vat_amount",
			"label": _("VAT Amount (SAR)"),
			"fieldtype": "Currency",
			"width": 150,
		}
	]


def append_data(data, title, amount, adjustment_amount, vat_amount):
	"""Returns data with appended value."""
	data.append({"title": _(title), "amount": amount, "adjustment_amount": adjustment_amount, "vat_amount": vat_amount})


def get_accounts(type):
	"""Get KSA Accounts of the given type"""
	return frappe.get_list(
		'Account',
		{
			'ksa_account_type': type,
		},
		['name', 'ksa_account_title'],
		order_by='ksa_account_position asc')


def get_account_value(filters, account_name):
	'''(dict, string) => tuple

	Get sum of debit and credit between the given date range
	'''
	from_date = getdate(filters['from_date'])
	to_date = getdate(filters['to_date'])
	result = frappe.db.sql("""
	SELECT
		SUM(debit_in_account_currency) as debit,
		SUM(credit_in_account_currency) as credit
	FROM
		`tabGL Entry`
	WHERE
		company = %(company)s AND
		is_cancelled = 0 AND
		posting_date BETWEEN %(from_date)s and %(to_date)s AND
		account = %(account)s
	""", {
		'company': filters['company'],
		'from_date': from_date,
		'to_date': to_date,
		'account': account_name
	}, as_dict=1)

	return {
		'debit': result[0]['debit'] if result[0]['debit'] is not None else 0,
		'credit': result[0]['credit'] if result[0]['debit'] is not None else 0
	}
