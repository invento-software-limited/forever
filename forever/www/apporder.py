import frappe
import json
from frappe.utils import nowdate

@frappe.whitelist(allow_guest=True)
def check_customer_information(customer):
    if customer:
        if frappe.db.exists("Customer",customer):
            customer_doc = frappe.get_doc("Customer",customer)
            return {"has_customer" : "yes","customer_group" : customer_doc.customer_group,"mobile":customer_doc.mobile,"name" : customer_doc.customer_name,"customer_group" : customer_doc.customer_group}
        
def get_context(context):
    data = []
    items = frappe.get_all("Item",fields=["item_code","item_name","standard_selling_rate","image","item_group"])
    for item in items:
        limit = frappe.db.get_value(
            'Item Limit',
            {
                'item_code':item.get("item_code"),
                'from_date': ['<=', frappe.utils.today()],
                'to_date': ['>=', frappe.utils.today()],
                'docstatus' : 1
            }
            ,["limit"],debug=True)
        
        data_dict = {
            "item_code" : item.get("item_code"),
            "item_name" : item.get("item_name"),
            "limit" : limit,
            "standard_selling_rate" : item.get("standard_selling_rate"),
            "image" : item.get("image"),
            "item_group" : item.get("item_group"),
            "item_group_modify" : item.get("item_group").replace(" ","_")
        }
        data.append(data_dict)
    context.items = data
    
    item_group = frappe.get_all("Item Group","name",pluck="name")
    group_data = []
    for ig in item_group:
        group_data.append({
            "name" : ig,
            "modify_name" : ig.replace(" ","_")
        })
    context.item_groups = group_data
    
    logo_image = frappe.db.get_single_value("Website Settings", "app_logo")
    if logo_image:
        context.logo_image = logo_image
    

@frappe.whitelist(allow_guest=True)

def create_sales_invoice(customer,customer_group,mobile,items):
    if not frappe.db.exists("Customer Group",customer_group):
        customer_group_doc = frappe.new_doc("Customer Group")
        customer_group_doc.customer_group_name = customer_group
        customer_group_doc.save()
        
    if not frappe.db.exists("Customer",customer):
        customer_doc = frappe.new_doc("Customer")
        customer_doc.customer_name = customer
        customer_doc.customer_type = "Company"
        customer_doc.customer_group = customer_group
        customer_doc.mobile = mobile
        customer_doc.save()
    try:
        customer_discount_percentage = frappe.db.get_value("Customer Group",customer_group,"discount")
        items = json.loads(items)
        si = frappe.new_doc("Sales Invoice")
        si.posting_date = nowdate()

        si.company = frappe.defaults.get_defaults().company
        si.customer = customer
        si.updated_customer_group = customer_group
        si.update_stock = 1
        
        sub_total = 0
        
        if items:
            for it in items:
                item = frappe.get_doc("Item",it.get("item"))
                if customer_discount_percentage:
                    rate_with_discount = item.standard_selling_rate - ((customer_discount_percentage * item.standard_selling_rate ) / 100)
                else:
                    rate_with_discount = item.standard_selling_rate
                sub_total += rate_with_discount
                
                data_dict = {
                        "item_code": item.item_code or item.item_code or "_Test Item",
                        "item_name": item.item_name or "_Test Item",
                        "description": item.description or "_Test Item",
                        "qty": float(it.get("qty")),
                        "uom": item.stock_uom or "Nos",
                        "stock_uom": item.stock_uom or "Nos",
                        "rate": rate_with_discount,
                        "conversion_factor": item.get("conversion_factor", 1)
                    }
                si.append("items",data_dict)
                
        si.total = sub_total
        
        si.save()
        
        return si.name
    except:
        return "Error"
