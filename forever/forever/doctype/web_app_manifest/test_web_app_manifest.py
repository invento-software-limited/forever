
class TestWebAppManifest(unittest.TestCase):
    def test_configure_pwa(self):
        configure_pwa()
        ws = frappe.get_doc('Website Settings')
        self.assertIn('''rel="manifest"''', ws.head_html)
