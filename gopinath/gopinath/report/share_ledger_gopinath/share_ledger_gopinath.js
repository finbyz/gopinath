// Copyright (c) 2016, FInByz Tech Pvt Ltd and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Share Ledger Gopinath"] = {
	"filters": [
		{
			"fieldname":"date",
			"label": __("Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		},
		{
			"fieldname":"shareholder",
			"label": __("Shareholder"),
			"fieldtype": "Link",
			"options": "Shareholder"
		}
	]
};
