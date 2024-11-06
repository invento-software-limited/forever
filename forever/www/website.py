import frappe

def get_context(context):
    catalouge = frappe.db.get_single_value("Homepage Details", "catalouge")
    policy = frappe.db.get_single_value("Homepage Details", "company_policy")
    prodcut_list = frappe.db.get_single_value("Homepage Details", "product_list")
    context.catalouge = catalouge
    context.policy = policy
    context.prodcut_list = prodcut_list
    
    logo_image = frappe.db.get_single_value("Website Settings", "app_logo")
    if logo_image:
        context.logo_image = logo_image