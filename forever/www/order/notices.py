import frappe

def get_context(context):
    context.no_cache = 1
    notices = frappe.db.get_all("Notice",["image","date","title"])
    context.notices = notices
    
    logo_image = frappe.db.get_single_value("Website Settings", "app_logo")
    if logo_image:
        context.logo_image = logo_image