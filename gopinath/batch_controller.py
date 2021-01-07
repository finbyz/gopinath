import frappe
from chemical.chemical.report.batch_wise_balance_chemical.batch_wise_balance_chemical import execute
from frappe.utils import nowdate, nowtime

@frappe.whitelist()
def get_batch_data():
	data = execute(filters={'to_date':nowdate()})[1]
	for row in data:
		if row['as_is_qty'] < 0.009:
			se = frappe.new_doc("Stock Entry")
			se.stock_entry_type = "Material Issue"
			se.purpose = "Material Issue"
			se.company = row['company']
			se.set_posting_time = 1
			se.posting_date = nowdate()
			se.posting_time = nowtime()
			se.remarks = "Auto created Entry. Stock less than 0.009"
			se.append("items",{
				'item_code': row['item_code'],
				's_warehouse': row['warehouse'],
				'packaging_material': row['packaging_material'],
				'batch_no': row['batch_no'],
				'packing_size': row['packing_size'],
				'concentration': row['concentration'],
				'no_of_packages': row['packages'],
				'lot_no': row['lot_no'],
				'qty': row['as_is_qty'],
				'cost_center': frappe.db.get_value("Company",row['company'],'cost_center')
			})
			se.save()
			se.submit()
	frappe.db.commit()