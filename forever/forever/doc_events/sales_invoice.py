import frappe

def extended_before_validate(doc,method=None):
    if doc.sales_type == "Product":
        if doc.customer_group != doc.updated_customer_group:
            customer = frappe.get_doc("Customer",doc.customer)
            customer.customer_group = doc.updated_customer_group
            customer.save()
            
        customer_group_percentage = frappe.db.get_value("Customer Group",doc.updated_customer_group,"discount")
        sub_total = 0
        if not customer_group_percentage:
            customer_group_percentage = 0
            
        for item in doc.items:
            #  or item.item_group != "All Item Groups"
            item_group = frappe.db.get_value("Item",item.item_code,"item_group")
            if item_group != "Products":
                frappe.throw("Item Group must be Products")
            item_rate = frappe.db.get_value("Item",item.get("item_code"),"standard_selling_rate") if frappe.db.get_value("Item",item.get("item_code"),"standard_selling_rate") else 0
            rate =  item_rate - ((customer_group_percentage * item_rate ) / 100)
            # item.amount = rate * item.qty
            item.rate = rate
            # sub_total += rate * item.qty
        
        # doc.total = sub_total
        # doc.grand_total = sub_total
        # doc.rounded_total = sub_total

def extended_validate(doc,method=None):
    if doc.sales_type == "Product":
        total = 0
        if doc.items:
            for item in doc.items:
                total += item.price_list_rate * item.qty
            vat_percentage = ((5 * total ) / 100)
            if doc.taxes:
                for tax in doc.taxes:
                    if tax.charge_type == "Actual":
                        tax.tax_amount = vat_percentage