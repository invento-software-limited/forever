app_name = "forever"
app_title = "Forever"
app_publisher = "Invento Software limited"
app_description = "Forever"
app_email = "support@invento.com.bd"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/forever/css/forever.css"
# app_include_js = "/assets/forever/js/forever.js"

# include js, css files in header of web template
# web_include_css = "/assets/forever/css/forever.css"
# web_include_js = "/assets/forever/js/forever.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "forever/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "forever/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "forever.utils.jinja_methods",
# 	"filters": "forever.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "forever.install.before_install"
# after_install = "forever.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "forever.uninstall.before_uninstall"
# after_uninstall = "forever.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "forever.utils.before_app_install"
# after_app_install = "forever.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "forever.utils.before_app_uninstall"
# after_app_uninstall = "forever.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "forever.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Item": {
		  "validate": "forever.forever.doc_events.item.extend_validate"
    },
    "Item Price": {
		  "validate": "forever.forever.doc_events.item_price.extend_validate"
    },
    "Sales Invoice" : {
      "validate": "forever.forever.doc_events.sales_invoice.extended_validate"
    }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"forever.tasks.all"
# 	],
# 	"daily": [
# 		"forever.tasks.daily"
# 	],
# 	"hourly": [
# 		"forever.tasks.hourly"
# 	],
# 	"weekly": [
# 		"forever.tasks.weekly"
# 	],
# 	"monthly": [
# 		"forever.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "forever.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "forever.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "forever.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["forever.utils.before_request"]
# after_request = ["forever.utils.after_request"]

# Job Events
# ----------
# before_job = ["forever.utils.before_job"]
# after_job = ["forever.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"forever.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

