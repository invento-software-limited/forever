
from __future__ import unicode_literals
import frappe

from frappe.model.document import Document
from frappe.website.utils import clear_cache


class WebAppManifest(Document):
    def on_update(self):
        """clear cache"""
        frappe.clear_cache(user='Guest')
        clear_cache()


@frappe.whitelist()
def configure_pwa():
    manifest = '''<link href="/manifest.json" rel="manifest">'''
    ws = frappe.get_doc('Website Settings')
    if not ws.head_html:
        ws.head_html = manifest
    if 'rel="manifest"' not in ws.head_html:
        ws.head_html += manifest
    ws.save()
