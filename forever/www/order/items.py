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
    context.no_cache = 1
    rank = frappe.local.request.args.get('rank')  # 'rank' is the parameter
    customer = frappe.local.request.args.get('customer')  # 'rank' is the parameter
    mobile = frappe.local.request.args.get('mobile')  # 'rank' is the parameter
    order_type = frappe.local.request.args.get('ordertype')  # 'rank' is the parameter
    customer_name = frappe.local.request.args.get('customername')  # 'rank' is the parameter

    context.customer = customer
    context.rank = rank
    context.mobile = mobile
    context.order_type = order_type
    context.customer_name = customer_name
    whatsapp_number = frappe.db.get_single_value("Homepage Details", "whats_app_number")
    if whatsapp_number:
        context.whatsapp_number = whatsapp_number

    discount = get_customer_group_discount_percentage(rank)
    data = []
    items = frappe.get_all("Item",fields=["item_code","item_name","standard_selling_rate","image","item_group","cc"])
    for item in items:
        limit = frappe.db.get_value(
            'Item Limit',
            {
                'item_code':item.get("item_code"),
                'from_date': ['<=', frappe.utils.today()],
                'to_date': ['>=', frappe.utils.today()],
                'docstatus' : 1
            }
            ,["limit"])
        
        data_dict = {
            "item_code" : item.get("item_code"),
            "item_name" : item.get("item_name"),
            "limit" : limit,
            "image" : item.get("image"),
            "item_group" : item.get("item_group"),
            "item_group_modify" : item.get("item_group").replace(" ","_"),
            "cc" : item.get("cc")
        }
        if discount:
            price = item.get("standard_selling_rate") - ((discount * item.get("standard_selling_rate")) / 100)
            data_dict["standard_selling_rate"] = round(price,1)
            data_dict["standard_selling_rate_show"] = format_taka(round(price,1))
        else:
            data_dict["standard_selling_rate"] = item.get("standard_selling_rate")
            data_dict["standard_selling_rate_show"] = format_taka(item.get("standard_selling_rate"))

        data.append(data_dict)
    context.itemss = data
    
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
        
    customer_groups = frappe.get_all("Customer Group","name",pluck="name")
    context.customer_groups = customer_groups

@frappe.whitelist(allow_guest=True)
def create_sales_invoice(customer,customer_group,mobile,items,order_type,customer_name,tax_amount):
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
        customer_doc.customer_name = customer_name
        customer_doc.save()
    try:
        customer_discount_percentage = frappe.db.get_value("Customer Group",customer_group,"discount")
        items = json.loads(items)
        si = frappe.new_doc("Sales Invoice")
        si.posting_date = nowdate()
        

        si.company = frappe.defaults.get_defaults().company
        si.customer = customer
        si.updated_customer_group = customer_group
        si.order_type = order_type
        si.update_stock = 1
        
        if tax_amount:
            default_tax_template = frappe.db.get_value("Sales Taxes and Charges Template",{"is_default" : 1 },"name")
            si.taxes_and_charges = default_tax_template
            si.append("taxes",{
                "charge_type": "Actual",
                "account_head": "VAT - FL",
                "description": "VAT 5%",
                "cost_center": "Main - FL",
                "rate": 5,
                "tax_amount": float(tax_amount)
            })
        
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
        return { "order_id" : si.name, "customer_name" : customer_name }
    except:
        return "Error"

@frappe.whitelist(allow_guest=True)
def make_cart_page(customer_group,items):
    items = json.loads(items)
    discount = get_customer_group_discount_percentage(customer_group)
    result = []
    if items:
        for it in items:
            item = frappe.get_doc("Item",it.get("item"))
            if discount:
                rate_with_discount = item.standard_selling_rate - ((discount * item.standard_selling_rate ) / 100)
                amount = float(it.get("qty")) * rate_with_discount
                cc = float(it.get("qty")) * item.cc
            else:
                rate_with_discount = item.standard_selling_rate
                amount = float(it.get("qty")) * rate_with_discount
                cc = float(it.get("qty")) * item.cc
            
            data_dict = {
                    "item_code": item.item_code or item.item_code or "",
                    "item_name": item.item_name or "",
                    "rate" : format_taka(rate_with_discount),
                    "qty": float(it.get("qty")),
                    "amount": round(amount),
                    "cc": round(cc,1) or "",
                    "image" : item.image,
                    "item_cc" : item.cc or ""
                }
            result.append(data_dict)
    
    return result

@frappe.whitelist(allow_guest=True)
def get_customer_group_discount_percentage(customer_rank):
    discount = frappe.db.get_value("Customer Group",{"name":customer_rank},"discount")
    return discount

def format_taka(amount):
    formatted_amount = "{:,.1f}".format(amount)  # Format with commas and 2 decimal places
    return f"৳{formatted_amount}"