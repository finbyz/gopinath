import frappe
from frappe import _
from frappe.utils import flt

def pr_before_validate(self,method):
    pr_cal_rate_qty(self)
    
def pr_cal_rate_qty(self):
	for d in self.items:
		maintain_as_is_stock = frappe.db.get_value("Item",d.item_code,'maintain_as_is_stock')
		if maintain_as_is_stock:
			if not d.supplier_concentration:
				frappe.throw("{} Row: {} Please add supplier concentration".format(d.doctype,d.idx))
			if not d.concentration:
				frappe.throw("{} Row: {} Please add concentration".format(d.doctype,d.idx))
				
		if d.get('packing_size') and d.get('no_of_packages'):
			d.qty = d.received_qty = (d.packing_size * d.no_of_packages)

			if maintain_as_is_stock:
				d.quantity = d.qty * d.concentration / 100
			else:
				d.quantity = d.qty
				
		if d.get('supplier_packing_size') and d.get('supplier_no_of_packages'):
			d.supplier_qty = (d.supplier_packing_size * d.supplier_no_of_packages)

			if maintain_as_is_stock:
				d.supplier_quantity = d.supplier_qty * d.supplier_concentration / 100
			else:
				d.supplier_quantity = d.supplier_qty

		if d.get('accepted_packing_size') and d.get('accepted_no_of_packages'):
			d.accepted_qty = (d.accepted_packing_size * d.accepted_no_of_packages)

			if maintain_as_is_stock:
				d.accepted_quantity = d.accepted_qty * d.accepted_concentration / 100
			else:
				d.accepted_quantity = d.accepted_qty

		if not d.accepted_quantity:
			d.short_quantity = d.quantity - d .supplier_quantity
		else:
			d.short_quantity = d.accepted_quantity - d .supplier_quantity
		d.amount_difference = flt(d.short_quantity) * flt(d.price)