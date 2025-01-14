
frappe.ui.form.on('Web App Manifest', {
    configure_pwa: function (frm) {
        frappe.call({
            method: 'forever.forever.doctype.web_app_manifest.web_app_manifest.configure_pwa',
            callback: function () {
                frappe.show_alert({message: __('Web app was configured'), indicator: 'green'})
            }
        });
    }
});
