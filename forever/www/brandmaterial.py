import frappe

def get_context(context):
    brand_materials = frappe.db.get_all("Brand Material Image","image")
    context.brand_materials = brand_materials
    
    logo_image = frappe.db.get_single_value("Website Settings", "app_logo")
    if logo_image:
        context.logo_image = logo_image