# Copyright (c) 2013, FInByz Tech Pvt Ltd and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import msgprint, _

def execute(filters=None):
	if not filters: filters = {}

	columns = get_columns(filters)


	data = []

	share_holder, share_type, no_of_shares, rate, amount = 0,1, 2, 3, 4

	all_shares = get_all_shares(filters)
	for share_entry in all_shares:
		# share_entry = frappe.get_doc("Shareholder",share_doc.name)
		row = False
		for datum in data:
			if datum[share_type] == share_entry.share_type and share_entry.parent == datum[share_holder]:
				datum[no_of_shares] += share_entry.no_of_shares
				datum[amount] += share_entry.amount
				if datum[no_of_shares] == 0:
					datum[rate] = 0
				else:
					datum[rate] = datum[amount] / datum[no_of_shares]
				row = True
				break
		# new entry
		if not row:
			row = [share_entry.parent,
				share_entry.share_type, share_entry.no_of_shares, share_entry.rate, share_entry.amount]

			data.append(row)

	return columns, data

def get_columns(filters):
	columns = [
		_("Shareholder") + ":Link/Shareholder:150",
		_("Share Type") + "::90",
		_("No of Shares") + "::90",
		_("Average Rate") + ":Currency:90",
		_("Amount") + ":Currency:90"
	]
	return columns

def get_all_shares(filters):
	condition = ' '
	if filters.get('shareholder'):
		return frappe.db.get_list("Share Balance",{"parent":filters.get("shareholder")},"*")
	else:
		return frappe.db.get_list("Share Balance",{},"*")