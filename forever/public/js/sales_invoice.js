frappe.ui.form.on("Sales Invoice", {
		refresh: function(frm){
				frm.set_query('updated_customer_group', () => {
						return {
								filters : [
									["name","!=","All Customer Groups"]
								]
						}
				})
		},
		customer (frm) {
				if (frm.doc.taxes) {
						frm.doc.taxes.forEach(element => {
								element.charge_type = "Actual"
						});
						refresh_field("taxes");
				}
		},
		
})