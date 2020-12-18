# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt, cint, getdate

def execute(filters=None):
	if not filters: filters = {}

	float_precision = cint(frappe.db.get_default("float_precision")) or 3

	columns = get_columns(filters)
	item_map = get_item_details(filters)
	iwb_map = get_item_warehouse_batch_map(filters, float_precision)
	iwb_map_without_group = get_item_warehouse_batch_map_without_group(filters, float_precision)

	data = []
	for company in sorted(iwb_map):
		for item in sorted(iwb_map[company]):
			for wh in sorted(iwb_map[company][item]):
				for batch in sorted(iwb_map[company][item][wh]):
					qty_dict = iwb_map[company][item][wh][batch]
					try:
						qty_dict_without_group = iwb_map_without_group[company][item][wh][batch]
					except KeyError:
						frappe.msgprint(str(company + ' ' + item))
					if qty_dict.opening_qty or qty_dict.in_qty or qty_dict.out_qty or qty_dict.bal_qty:
						lot_no, packaging_material, packing_size, concentration, valuation_rate = frappe.db.get_value("Batch", batch, ["lot_no", "packaging_material","packing_size","concentration","valuation_rate"])
						# data.append([item, wh, batch, lot_no, concentration, packaging_material, packing_size
						# 	flt(qty_dict.bal_qty, float_precision),
						# 	 item_map[item]["stock_uom"]
						# ])
					
						if item_map[item]["maintain_as_is_stock"]:
							data.append({
								'posting_date':qty_dict_without_group.posting_date,
								'item_code': item,
								'item_group': item_map[item]["item_group"],
								'warehouse': wh,
								'batch_no': batch,
								'lot_no': lot_no,
								'voucher_type': qty_dict_without_group.voucher_type,
								'voucher_no': qty_dict_without_group.voucher_no,
								'concentration': concentration,
								'packaging_material': packaging_material,
								'packing_size': packing_size,
								'company':qty_dict_without_group.company,
								'packages': flt(qty_dict.bal_qty/packing_size,0) if packing_size else 0,
								'bal_qty': flt(qty_dict.bal_qty*concentration/100, float_precision),
								'amount': flt((qty_dict.bal_qty*concentration/100) * flt(valuation_rate*100/concentration) , float_precision),
								'as_is_qty': flt(qty_dict.bal_qty, float_precision),
								'valuation_rate':flt(valuation_rate*100/concentration,float_precision),
								'uom': item_map[item]["stock_uom"],
								'party_type':qty_dict_without_group.party_type,
								'party':qty_dict_without_group.party,
							})
						else:
							data.append({
								'posting_date':qty_dict_without_group.posting_date,
								'item_code': item,
								'item_group': item_map[item]["item_group"],
								'warehouse': wh,
								'batch_no': batch,
								'lot_no': lot_no,
								'voucher_type': qty_dict_without_group.voucher_type,
								'voucher_no': qty_dict_without_group.voucher_no,
								'concentration': concentration,
								'packaging_material': packaging_material,
								'packing_size': packing_size,
								'company':qty_dict_without_group.company,
								'packages': flt(qty_dict.bal_qty/packing_size,0) if packing_size else 0,
								'bal_qty': flt(qty_dict.bal_qty, float_precision),
								'amount': flt(qty_dict.bal_qty*valuation_rate, float_precision),
								'as_is_qty': flt(qty_dict.bal_qty, float_precision),
								'valuation_rate':valuation_rate,
								'uom': item_map[item]["stock_uom"],
								'party_type':qty_dict_without_group.party_type,
								'party':qty_dict_without_group.party,
							})
	filter_company = filters.get("company")
	from_date = frappe.db.get_value("Fiscal Year","2019-2020","year_start_date")
	to_date = filters.get('to_date')
	for row in data:
		item_code = row['item_code']
		batch_no = row['batch_no']
		company = row['company']
		row['stock_ledger'] = f"""<button style='margin-left:5px;border:none;color: #fff; background-color: #5e64ff; padding: 3px 5px;border-radius: 5px;'
			target="_blank" item_code='{item_code}' company='{company}' from_date='{from_date}' to_date='{to_date}' batch_no='{batch_no}'
			onClick=view_stock_leder_report(this.getAttribute('item_code'),this.getAttribute('company'),this.getAttribute('from_date'),this.getAttribute('to_date'),this.getAttribute('batch_no'))>View Stock Ledger</button>"""

	return columns, data

def get_columns(filters):
	"""return columns based on filters"""
	columns = [
		{
			"label": _("Posting Date"),
			"fieldname": "posting_date",
			"fieldtype": "Date",
			"width": 80
		},
		{
			"label": _("Item Code"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 180
		},
		{
			"label": _("Warehouse"),
			"fieldname": "warehouse",
			"fieldtype": "Link",
			"options": "Warehouse",
			"width": 120
		},
		{
			"label": _("Batch"),
			"fieldname": "batch_no",
			"fieldtype": "Link",
			"options": "Batch",
			"width": 120
		},
		{
			"label": _("Lot No"),
			"fieldname": "lot_no",
			"fieldtype": "Data",
			"width": 80
		},
		{
			"label": _("Receipt Document"),
			"fieldname": "voucher_no",
			"fieldtype": "Dynamic Link",
			"options": "voucher_type",
			"width": 140
		},
		{
			"label": _("Qty"),
			"fieldname": "bal_qty",
			"fieldtype": "Float",
			"width": 90
		},
	]
	columns +=[
		{
			"label": _("Packages"),
			"fieldname": "packages",
			"fieldtype": "Int",
			"width": 50
		},
		{	
			"label": _("Party Type"),
			"fieldname": "party_type",
			"fieldtype": "Data",
			"width": 80,
			"align":"center"
		},
		{	
			"label": _("Party"),
			"fieldname": "party",
			"fieldtype": "Dynamic Link",
			"options":"party_type",
			"width": 140,
			"align":"left"
		},	
		{
			"label": _("Packaging Material"),
			"fieldname": "packaging_material",
			"fieldtype": "Link",
			"options": "Packaging Material",
			"width": 70
		},	
		{
			"label": _("Size"),
			"fieldname": "packing_size",
			"fieldtype": "Data",
			"width": 50
		},
		{
			"label": _("Price"),
			"fieldname": "valuation_rate",
			"fieldtype": "Currency",
			"width": 80
		},
		{
			"label": _("Amount"),
			"fieldname": "amount",
			"fieldtype": "Currency",
			"width": 80
		},
		{
			"label": _("As is Qty"),
			"fieldname": "as_is_qty",
			"fieldtype": "Float",
			"width": 100
		},
		{
			"label": _("Concentration"),
			"fieldname": "concentration",
			"fieldtype": "Percent",
			"width": 80
		},		
		{
			"label": _("UOM"),
			"fieldname": "uom",
			"fieldtype": "Link",
			"options": "UOM",
			"width": 40
		},
		{
			"label": _("Company"),
			"fieldname": "company",
			"fieldtype": "Link",
			"options": "Company",
			"width": 120
		},
				{
			"label": _("Voucher Type"),
			"fieldname": "voucher_type",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": _("Stock Ledger"),
			"fieldname": "stock_ledger",
			"fieldtype": "button",
			"width": 120
		}
	]

	return columns

def get_conditions(filters):
	conditions = ""
	if filters.get("to_date"):
		conditions += " and sle.posting_date <= '%s'" % filters["to_date"]
	else:
		frappe.throw(_("'To Date' is required"))

	if filters.get("company"):
		conditions += " and sle.company = '%s'" % filters["company"]

	if filters.get("warehouse"):
		conditions += " and sle.warehouse = '%s'" % filters["warehouse"]

	if filters.get("item_code"):
		conditions += " and sle.item_code = '%s'" % filters["item_code"]

	return conditions

#get all details
def get_stock_ledger_entries(filters):

	conditions = get_conditions(filters)
	return frappe.db.sql("""
		select sle.posting_date, sle.item_code, sle.batch_no, sle.warehouse, sle.posting_date,sle.company, sum(sle.actual_qty) as actual_qty
		from `tabStock Ledger Entry` as sle
		where sle.docstatus < 2 and ifnull(sle.batch_no, '') != '' %s
		group by sle.voucher_no, sle.batch_no, sle.item_code, sle.warehouse
		order by sle.company,sle.item_code, sle.warehouse, sle.batch_no""" %
		conditions, as_dict=1)

def get_item_warehouse_batch_map(filters, float_precision):
	sle = get_stock_ledger_entries(filters)
	iwb_map = {}

	from_date = getdate(filters["to_date"])
	to_date = getdate(filters["to_date"])

	for d in sle:
		iwb_map.setdefault(d.company, {}).setdefault(d.item_code, {}).setdefault(d.warehouse, {})\
			.setdefault(d.batch_no, frappe._dict({
				"opening_qty": 0.0, "in_qty": 0.0, "out_qty": 0.0, "bal_qty": 0.0
			}))
		qty_dict = iwb_map[d.company][d.item_code][d.warehouse][d.batch_no]
		if d.posting_date < from_date:
			qty_dict.opening_qty = flt(qty_dict.opening_qty, float_precision) \
				+ flt(d.actual_qty, float_precision)
		elif d.posting_date >= from_date and d.posting_date <= to_date:
			if flt(d.actual_qty) > 0:
				qty_dict.in_qty = flt(qty_dict.in_qty, float_precision) + flt(d.actual_qty, float_precision)
			else:
				qty_dict.out_qty = flt(qty_dict.out_qty, float_precision) \
					+ abs(flt(d.actual_qty, float_precision))
		qty_dict.bal_qty = flt(qty_dict.bal_qty, float_precision) + flt(d.actual_qty, float_precision)

	return iwb_map

def get_stock_ledger_entries_without_group(filters):
	conditions = get_conditions(filters)

	party_condition = ''
	if filters.get('party') and filters.get('party_type'):
		if filters.get('party').find("'") > 0:
			party = filters.get('party').replace("'","''")
		else:
			party = filters.get('party')
		if filters.get('party_type') == 'Supplier':
			party_condition = """ and (pi.supplier = '{supplier}' or pr.supplier = '{supplier}' or se.party = '{supplier}') """.format(supplier=party)
		elif filters.get('party_type') == 'Customer':
			party_condition = """ and (si.customer = '{customer}' or dn.customer = '{customer}') """.format(customer=party)
		elif filters.get('party_type') == 'Company':
			party_condition = """ and (se.party = '{se_party}') """.format(se_party=party)

	return frappe.db.sql("""
		select sle.item_code, sle.batch_no, sle.warehouse, sle.posting_date,sle.company, sle.actual_qty, sle.voucher_type,sle.voucher_no,
			CASE WHEN sle.voucher_type in ('Purchase Receipt','Purchase Invoice') THEN 'Supplier'
			WHEN sle.voucher_type in ('Delivery Note','Sales Invoice') THEN 'Customer'
			WHEN sle.voucher_type in ('Stock Entry') THEN se.party_type
			END AS party_type,
			IFNULL(pr.supplier, IFNULL(pi.supplier,IFNULL(dn.customer,IFNULL(si.customer,se.party)))) as party
		from `tabStock Ledger Entry` as sle
			LEFT JOIN `tabStock Entry` as se on se.name = sle.voucher_no
			LEFT JOIN `tabPurchase Receipt` as pr on pr.name = sle.voucher_no
			LEFT JOIN `tabPurchase Invoice` as pi on pi.name = sle.voucher_no
			LEFT JOIN `tabDelivery Note` as dn on dn.name = sle.voucher_no
			LEFT JOIN `tabSales Invoice` as si on si.name = sle.voucher_no
		where sle.docstatus < 2 and ifnull(sle.batch_no, '') != '' and sle.actual_qty > 0 {party_condition} %s
		order by sle.company,sle.item_code, sle.warehouse,sle.batch_no""".format(party_condition=party_condition) %
		(conditions), as_dict=1)

def get_item_warehouse_batch_map_without_group(filters, float_precision):
	sle = get_stock_ledger_entries_without_group(filters)
	iwb_map_without_group = {}

	for d in sle:
		iwb_map_without_group.setdefault(d.company, {}).setdefault(d.item_code, {}).setdefault(d.warehouse, {})\
			.setdefault(d.batch_no, frappe._dict({
				"voucher_type":'',"voucher_no":''
			}))
		qty_dict_without_group = iwb_map_without_group[d.company][d.item_code][d.warehouse][d.batch_no]
		qty_dict_without_group.company = d.company
		qty_dict_without_group.voucher_type = d.voucher_type
		qty_dict_without_group.voucher_no = d.voucher_no
		qty_dict_without_group.party_type = d.party_type
		qty_dict_without_group.party = d.party
		qty_dict_without_group.posting_date = d.posting_date

	return iwb_map_without_group


def get_item_details(filters):
	item_map = {}
	for d in frappe.db.sql("select name, item_name, description, stock_uom, item_group, maintain_as_is_stock from tabItem", as_dict=1):
		item_map.setdefault(d.name, d)

	return item_map
