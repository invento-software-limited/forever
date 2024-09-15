import frappe
import json
from frappe.utils import nowdate

@frappe.whitelist()
def check_customer_information(customer):
    if customer:
        if frappe.db.exists("Customer",customer):
            customer_doc = frappe.get_doc("Customer",customer)
            return {"has_customer" : "yes","customer_group" : customer_doc.customer_group,"mobile":customer_doc.mobile}
        else:
            frappe.throw("No customer found")
        
def get_context(context):
    data = []
    items = frappe.get_all("Item",fields=["item_code","item_name","standard_selling_rate","image"])
    for item in items:
        limit = frappe.db.get_value("Item Selling Limit",{"item_code":item.get("item_code")},"limit")
        data_dict = {
            "item_code" : item.get("item_code"),
            "item_name" : item.get("item_name"),
            "limit" : limit,
            "standard_selling_rate" : item.get("standard_selling_rate"),
            "image" : item.get("image")
        }
        data.append(data_dict)
    context.items = data

@frappe.whitelist()
def create_sales_invoice(customer,customer_group,items):
    try:
        customer_discount_percentage = frappe.db.get_value("Customer Group",customer_group,"discount")
        items = json.loads(items)
        si = frappe.new_doc("Sales Invoice")
        si.posting_date = nowdate()

        si.company = frappe.defaults.get_defaults().company
        si.customer = customer
        si.update_stock = 0
        
        if items:
            for it in items:
                item = frappe.get_doc("Item",it.get("item"))
                if customer_discount_percentage:
                    rate_with_discount = item.standard_selling_rate - ((customer_discount_percentage * item.standard_selling_rate ) / 100)
                else:
                    rate_with_discount = item.standard_selling_rate
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

        si.save()
        
        return si.name
    except:
        pass