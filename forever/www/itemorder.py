import frappe
import json
from frappe.utils import nowdate

@frappe.whitelist(allow_guest=True)
def check_customer_information(customer):
    if customer:
        if frappe.db.exists("Customer",customer):
            customer_doc = frappe.get_doc("Customer",customer)
            return {"has_customer" : "yes","customer_group" : customer_doc.customer_group,"mobile":customer_doc.mobile,"name" : customer_doc.customer_name,"customer_group" : customer_doc.customer_group}

@frappe.whitelist(allow_guest=True)
def get_customer_group_discount_percentage(customer_rank):
    discount = frappe.db.get_value("Customer Group",{"name":customer_rank},"discount")
    return discount

def get_context(context):
    item_group = frappe.get_all("Item Group","name",pluck="name")
    group_data = []
    for ig in item_group:
        group_data.append({
            "name" : ig,
            "modify_name" : ig.replace(" ","_")
        })
    context.item_groups = group_data
    
    logo_image = frappe.db.get_single_value("Website Settings", "app_logo")
    
    print("------------------------",logo_image)
    
    if logo_image:
        context.logo_image = logo_image
        
    customer_groups = frappe.get_all("Customer Group","name",pluck="name")
    context.customer_groups = customer_groups