// Copyright (c) 2016, FinByz Tech Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Batch Wise Party Balance Chemical"] = {
	"filters": [
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "80",
			"default": frappe.datetime.get_today()
		},
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"width": "80",
		},
		{
			"fieldname": "item_code",
			"label": __("Item"),
			"fieldtype": "Link",
			"options": "Item",
			"width": "80",
		},
		{
			"fieldname": "warehouse",
			"label": __("Warehouse"),
			"fieldtype": "Link",
			"options": "Warehouse",
			"width": "80",
		},
		{
			"fieldname":"party_type",
			"label": __("Party Type"),
			"fieldtype": "Link",
			"options": "DocType",
			"get_query" : function(){
				return {
					"filters": {
						"name": ["in", ["Customer", "Supplier","Company"]],
					},
				}
			}
		},
		{
			"fieldname": "party",
			"label": __("Party"),
			"fieldtype": "Dynamic Link",
			"options": "party_type"
		},

		
	]
}
function view_stock_leder_report(item_code, company, from_date, to_date, batch_no) {
	window.open(window.location.href.split("#")[0] + "#query-report/Stock Ledger Chemical" + "/?" + "item_code=" + item_code + "&" +  "company="+company + "&" + "from_date=" + from_date + "&" + "to_date=" + to_date + "&" + "batch_no=" + batch_no,"_blank")	
}
