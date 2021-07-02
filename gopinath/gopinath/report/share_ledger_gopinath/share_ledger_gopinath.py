# Copyright (c) 2013, FInByz Tech Pvt Ltd and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cstr, cint, getdate
from frappe import msgprint, _

def execute(filters=None):
	if not filters: filters = {}

	if not filters.get("date"):
		frappe.throw(_("Please select date"))

	columns = get_columns(filters)

	date = filters.get("date")

	data = []

	transfers = get_all_transfers(date, filters)
	if transfers:
		for transfer in transfers:
			if transfer.from_shareholder:
				transfer.no_of_shares = (-transfer.no_of_shares)
				transfer.amount = (-transfer.amount)
				row = [transfer.from_shareholder, transfer.date, transfer.transfer_type,
					transfer.share_type, transfer.no_of_shares, transfer.share_certificate_no,transfer.rate, transfer.amount,
					transfer.company, transfer.name]

				if filters.get('from_shareholder') and filters.from_shareholder == transfer.from_shareholder:
					data.append(row)
				elif not (filters.get('from_shareholder') or filters.get('to_shareholder')):
					data.append(row)

			if transfer.to_shareholder:
				transfer.no_of_shares = abs(transfer.no_of_shares)
				transfer.amount = abs(transfer.amount)
				row = [transfer.to_shareholder, transfer.date, transfer.transfer_type,
					transfer.share_type, transfer.no_of_shares, transfer.share_certificate_no,transfer.rate, transfer.amount,
					transfer.company, transfer.name]

				if filters.get('to_shareholder') and filters.to_shareholder == transfer.to_shareholder:
					data.append(row)
				elif not (filters.get('from_shareholder') or filters.get('to_shareholder')):
					data.append(row)

	return columns, data

def get_columns(filters):
	columns = [
		_("Shareholder") + ":Link/Shareholder:150",
		_("Date") + ":Date:100",
		_("Transfer Type") + "::140",
		_("Share Type") + "::90",
		_("No of Shares") + "::90",
		_("Certificate No") + "::100",
		_("Rate") + ":Currency:90",
		_("Amount") + ":Currency:90",
		_("Company") + "::150",
		_("Share Transfer") + ":Link/Share Transfer:150"
	]
	return columns

def get_all_transfers(date, filters):
	condition = ' '
	if filters.get('from_shareholder'):
		condition = " and (from_shareholder = '{0}')".format(filters.get('from_shareholder'))
	if filters.get('to_shareholder'):
		condition += " and (to_shareholder = '{0}')".format(filters.get('to_shareholder'))
	query  = frappe.db.sql("""SELECT * FROM `tabShare Transfer`
		WHERE DATE(date) <='{date}' {condition}
		ORDER BY date""".format(date=date,condition=condition),as_dict=1)
	
	if query:
		return query
