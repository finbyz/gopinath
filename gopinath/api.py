import frappe
from frappe import _
from frappe.utils import flt, cint, getdate
from erpnext.accounts.utils import get_fiscal_year
import datetime
import re

@frappe.whitelist()
def rename_se(existing_name, series_value, naming_series):
	naming_series_len = len([i.start() for i in re.finditer('#',naming_series)]) # Find # length in naming_series
	new_name = re.findall("^(.*[\\\/])",existing_name)[0] # Before Slash
	last_digits = re.findall("[^\/]+$",existing_name)[0] # After Slash
	len_last_digits = len(last_digits) # After Slash
	if series_value:
		if len(series_value) > naming_series_len:
			frappe.throw("Please Enter {naming_series_len} Digit Series Value".format(naming_series_len=naming_series_len))
		temp_digits = last_digits.replace(last_digits,series_value)
		if len(temp_digits)!=naming_series_len:
			temp_digits = temp_digits.rjust((naming_series_len-len(temp_digits)) + len(temp_digits),'0')
		new_name += temp_digits
		if new_name != existing_name:
			frappe.rename_doc("Stock Entry", existing_name, new_name, force=True)
			frappe.db.set_value("Stock Entry",new_name,"series_value",series_value)
			return new_name
# def pr_before_validate(self,method):
# 	pr_cal_rate_qty(self)
	
# def pr_cal_rate_qty(self):
# 	for d in self.items:
# 		maintain_as_is_stock = frappe.db.get_value("Item",d.item_code,'maintain_as_is_stock')
# 		if maintain_as_is_stock:
# 			if not d.supplier_concentration:
# 				frappe.throw("{} Row: {} Please add supplier concentration".format(d.doctype,d.idx))
# 			if not d.concentration:
# 				frappe.throw("{} Row: {} Please add concentration".format(d.doctype,d.idx))
				
# 		if d.get('packing_size') and d.get('no_of_packages'):
# 			if d.tare_weight:
# 				d.qty = d.received_qty = ((d.packing_size - d.tare_weight) * d.no_of_packages)
# 			else:
# 				d.qty = d.received_qty = (d.packing_size * d.no_of_packages)

# 			if maintain_as_is_stock:
# 				d.quantity = d.qty * d.concentration / 100
# 			else:
# 				d.quantity = d.qty
				
# 		if d.get('supplier_packing_size') and d.get('supplier_no_of_packages'):
# 			d.supplier_qty = (d.supplier_packing_size * d.supplier_no_of_packages)

# 			if maintain_as_is_stock:
# 				d.supplier_quantity = d.supplier_qty * d.supplier_concentration / 100
# 			else:
# 				d.supplier_quantity = d.supplier_qty

# 		if d.get('accepted_packing_size') and d.get('accepted_no_of_packages'):
# 			d.accepted_qty = (d.accepted_packing_size * d.accepted_no_of_packages)

# 			if maintain_as_is_stock:
# 				d.accepted_quantity = d.accepted_qty * d.accepted_concentration / 100
# 			else:
# 				d.accepted_quantity = d.accepted_qty

# 		if not d.accepted_quantity:
# 			d.short_quantity = d.quantity - d .supplier_quantity
# 		else:
# 			d.short_quantity = d.accepted_quantity - d .supplier_quantity
# 		d.supplier_amount = flt(d.supplier_quantity * d.price)
# 		d.rate = flt(d.supplier_amount / d.qty)
# 		d.amount_difference = flt(d.short_quantity) * flt(d.price)
def before_naming(self, method):
	if not self.get('amended_from') and not self.get('name'):
		date = self.get("transaction_date") or self.get("posting_date") or  self.get("manufacturing_date") or  self.get("date") or getdate()

		fiscal = get_fiscal(date)
		self.fiscal = fiscal
		
		month = str(datetime.datetime.strptime(str(date),'%Y-%m-%d').month)
		
		self.month = month

		if not self.get('company_series'):
			self.company_series = None
		if self.get('series_value'):
			if self.series_value > 0:
				name = naming_series_name(self.naming_series, fiscal, self.company_series, self.month)
				check = frappe.db.get_value('Series', name, 'current', order_by="name")
				#frappe.msgprint(str(check))
				if check == 0:
					pass
				elif not check:
					
					frappe.db.sql("insert into tabSeries (name, current) values ('{}', 0)".format(name))

				frappe.db.sql("update `tabSeries` set current = {} where name = '{}'".format(cint(self.series_value) - 1, name))

def naming_series_name(name, fiscal, company_series=None, month=None):
	if company_series:
		name = name.replace('company_series', str(company_series))
	if month:
		name = name.replace('month', str(month))

	name = name.replace('YYYY', str(datetime.date.today().year))
	name = name.replace('YY', str(datetime.date.today().year)[2:])
	name = name.replace('MM', '{0:0=2d}'.format(datetime.date.today().month))
	name = name.replace('DD', '{0:0=2d}'.format(datetime.date.today().day))
	name = name.replace('fiscal', str(fiscal))
	name = name.replace('#', '')
	name = name.replace('.', '')
	return name

@frappe.whitelist()
def check_counter_series(name, company_series = None, date = None, month=None):
	if not date:
		date = datetime.date.today()

	month = str(datetime.datetime.strptime(str(date),'%Y-%m-%d').month)

	fiscal = get_fiscal(date)
	
	name = naming_series_name(name, fiscal, company_series, month)
	
	check = frappe.db.get_value('Series', name, 'current', order_by="name")
	
	if check == 0:
		return 1
	elif check == None:
		frappe.db.sql("insert into tabSeries (name, current) values ('{}', 0)".format(name))
		return 1
	else:
		return int(frappe.db.get_value('Series', name, 'current', order_by="name")) + 1

def get_fiscal(date):
	fy = get_fiscal_year(date)[0]
	fiscal = frappe.db.get_value("Fiscal Year", fy, 'fiscal')

	return fiscal if fiscal else fy.split("-")[0][2:] + fy.split("-")[1][2:]


def basic_validations(self):
	if self.transfer_type == 'Purchase':
		self.to_shareholder = ''
		if not self.from_shareholder:
			frappe.throw(_('The field From Shareholder cannot be blank'))
		if not self.from_folio_no:
			frappe.throw("Please Add Folio No.")
		if not self.asset_account:
			frappe.throw(_('The field Asset Account cannot be blank'))
	elif (self.transfer_type == 'Issue'):
		self.from_shareholder = ''
		if not self.to_shareholder:
			frappe.throw(_('The field To Shareholder cannot be blank'))
		if not self.to_folio_no:
			frappe.throw("Please Add Folio No.")
		if not self.asset_account:
			frappe.throw(_('The field Asset Account cannot be blank'))
	else:
		if not self.from_shareholder or not self.to_shareholder:
			frappe.throw(_('The fields From Shareholder and To Shareholder cannot be blank'))
		if not self.to_folio_no:
			frappe.throw("Please Add Folio No.")
	if not self.equity_or_liability_account:
			frappe.throw(_('The field Equity/Liability Account cannot be blank'))
	if self.from_shareholder == self.to_shareholder:
		frappe.throw(_('The seller and the buyer cannot be the same'))
	if self.no_of_shares != self.to_no - self.from_no + 1:
		frappe.throw(_('The number of shares and the share numbers are inconsistent'))
	if not self.amount:
		self.amount = self.rate * self.no_of_shares
	if self.amount != self.rate * self.no_of_shares:
		frappe.throw(_('There are inconsistencies between the rate, no of shares and the amount calculated'))
