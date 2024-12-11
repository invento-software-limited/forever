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
		before_save (frm) {
				let payment_due_date = frappe.datetime.add_days(frm.doc.due_date, 30);
				frm.set_value('due_date', payment_due_date);
				frm.refresh_field("due_date")
		}
})