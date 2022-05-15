import frappe


def create_advance_retention_entry(doc, method):
	'''Creates Journal Entry for Retention and Advance Amounts'''
	ksa_accounts_settings = frappe.get_single('KSA Accounts Settings')
	if ksa_accounts_settings.enable_deduction:
		if ksa_accounts_settings.do_not_allow_to_create_sales_invoice_without_project and not doc.project:
			frappe.throw(msg='Select Project in Accounting Dimensions', exc=frappe.MandatoryError)
		if doc.apply_retention_deduction and not doc.retention_deduction_percentage:
			frappe.throw(msg='Add Retention Deduction Percentage', exc=frappe.MandatoryError)
		if doc.apply_advance_deduction and not doc.advance_deduction_percentage:
			frappe.throw(msg='Add Advance Deduction Percentage', exc=frappe.MandatoryError)

		if not doc.apply_retention_deduction or not doc.apply_advance_deduction or method != 'on_submit':
			return

		# Create Journal Entry
		journal_entry = frappe.get_doc({
			'doctype': 'Journal Entry',
			'company': doc.company,
			'entry_type': 'Journal Entry',
			'posting_date': doc.posting_date
		})

		total_amount = 0
		# Deductions Entry
		if doc.apply_retention_deduction:
			retention_amount = doc.net_total * doc.retention_deduction_percentage / 100
			journal_entry.append('accounts', {
				'account': ksa_accounts_settings.retention_account,
				'project': doc.project,
				'debit_in_account_currency': retention_amount,
				'credit_in_account_currency': 0
			})
			total_amount += retention_amount

		if doc.apply_advance_deduction:
			advance_amount = doc.net_total * doc.advance_deduction_percentage / 100
			journal_entry.append('accounts', {
				'account': ksa_accounts_settings.advance_account,
				'project': doc.project,
				'debit_in_account_currency': advance_amount,
				'credit_in_account_currency': 0
			})
			total_amount += advance_amount

		# Debtor Entry
		journal_entry.append('accounts', {
			'account': doc.debit_to,
			'party_type': 'Customer',
			'party': doc.customer,
			'project': doc.project,
			'debit_in_account_currency': 0,
			'credit_in_account_currency': total_amount,
			'reference_type': 'Sales Invoice',
			'reference_name': doc.name,
			'user_remark': 'Retention/Advance Deduction'
		})

		journal_entry.save()
		journal_entry.submit()
