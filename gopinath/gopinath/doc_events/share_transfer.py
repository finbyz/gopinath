from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.naming   import make_autoname
from frappe.exceptions import ValidationError
from frappe.utils import nowdate

def on_submit(self):
    if self.transfer_type == 'Issue':
        shareholder = self.get_company_shareholder()
        shareholder.append('share_balance', {
            'share_type': self.share_type,
            'from_no': self.from_no,
            'to_no': self.to_no,
            'rate': self.rate,
            'amount': self.amount,
            'no_of_shares': self.no_of_shares,
            'is_company': 1,
            'current_state': 'Issued',
            'certificate_no':self.share_certificate_no
        })
        shareholder.save()

        doc = self.get_shareholder_doc(self.to_shareholder)
        doc.append('share_balance', {
            'share_type': self.share_type,
            'from_no': self.from_no,
            'to_no': self.to_no,
            'rate': self.rate,
            'amount': self.amount,
            'no_of_shares': self.no_of_shares,
            'certificate_no':self.share_certificate_no
        })
        doc.save()

    elif self.transfer_type == 'Purchase':
        self.remove_shares(self.from_shareholder)
        self.remove_shares(self.get_company_shareholder().name)

    elif self.transfer_type == 'Transfer':
        self.remove_shares(self.from_shareholder)
        doc = self.get_shareholder_doc(self.to_shareholder)
        doc.append('share_balance', {
            'share_type': self.share_type,
            'from_no': self.from_no,
            'to_no': self.to_no,
            'rate': self.rate,
            'amount': self.amount,
            'no_of_shares': self.no_of_shares,
            'certificate_no':self.share_certificate_no

        })
        doc.save()

def on_cancel(self):
    if self.transfer_type == 'Issue':
        compnay_shareholder = self.get_company_shareholder()
        self.remove_shares(compnay_shareholder.name)
        self.remove_shares(self.to_shareholder)

    elif self.transfer_type == 'Purchase':
        compnay_shareholder = self.get_company_shareholder()
        from_shareholder = self.get_shareholder_doc(self.from_shareholder)

        from_shareholder.append('share_balance', {
            'share_type': self.share_type,
            'from_no': self.from_no,
            'to_no': self.to_no,
            'rate': self.rate,
            'amount': self.amount,
            'no_of_shares': self.no_of_shares,
            'certificate_no':self.share_certificate_no

        })

        from_shareholder.save()

        compnay_shareholder.append('share_balance', {
            'share_type': self.share_type,
            'from_no': self.from_no,
            'to_no': self.to_no,
            'rate': self.rate,
            'amount': self.amount,
            'no_of_shares': self.no_of_shares,
            'certificate_no':self.share_certificate_no

        })

        compnay_shareholder.save()

    elif self.transfer_type == 'Transfer':
        self.remove_shares(self.to_shareholder)
        from_shareholder = self.get_shareholder_doc(self.from_shareholder)
        from_shareholder.append('share_balance', {
            'share_type': self.share_type,
            'from_no': self.from_no,
            'to_no': self.to_no,
            'rate': self.rate,
            'amount': self.amount,
            'no_of_shares': self.no_of_shares,
            'certificate_no':self.share_certificate_no

        })
        from_shareholder.save()