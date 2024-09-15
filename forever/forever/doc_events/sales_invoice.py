import frappe

def extended_on_submit(doc,method=None):
    if doc.customer_group != doc.updated_customer_group:
        customer = frappe.get_doc("Customer",doc.customer)
        customer.customer_group = doc.updated_customer_group
        customer.save()
        customer_group_percentage = frappe.db.get_value("Customer Group",doc.updated_customer_group,"discount")
        if customer_group_percentage:
            for item in doc.items:
                item_rate = frappe.db.get_value("Item",item.get("item_code"),"standard_selling_rate") if frappe.db.get_value("Item",item.get("item_code"),"standard_selling_rate") else 0
                rate =  item_rate - ((customer_group_percentage * item_rate ) / 100)
                item.amount = rate * item.qty
                item.rate = rate