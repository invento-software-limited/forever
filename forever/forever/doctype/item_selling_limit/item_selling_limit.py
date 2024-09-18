# Copyright (c) 2024, Invento Software limited and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class ItemSellingLimit(Document):
    def validate(self):
        from_date = self.from_date
        to_date = self.to_date

        if not from_date or not to_date:
            return

        overlapping_records = frappe.get_all(
            'Item Selling Limit',
            filters={
                'name': ['!=', self.name],
                'from_date': ['<=', to_date],
                'to_date': ['>=', from_date],
                'docstatus' : 1
            }
        )

        if overlapping_records:
            frappe.throw(_('There is an existing selling limit record with overlapping date ranges.'))
        
        # set from_date and to_date
        if self.items:
            for item in self.items:
                item.from_date = self.from_date
                item.to_date = self.to_date