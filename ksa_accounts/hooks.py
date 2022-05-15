from . import __version__ as app_version

app_name = "ksa_accounts"
app_title = "KSA Accounts"
app_publisher = "Havenir Solutions"
app_description = "Localisation App for KSA Accounts"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "hello@havenir.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/ksa_accounts/css/ksa_accounts.css"
# app_include_js = "/assets/ksa_accounts/js/ksa_accounts.js"

# include js, css files in header of web template
# web_include_css = "/assets/ksa_accounts/css/ksa_accounts.css"
# web_include_js = "/assets/ksa_accounts/js/ksa_accounts.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "ksa_accounts/public/scss/website"

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

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "ksa_accounts.install.before_install"
# after_install = "ksa_accounts.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "ksa_accounts.uninstall.before_uninstall"
# after_uninstall = "ksa_accounts.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "ksa_accounts.notifications.get_notification_config"

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
	"Sales Invoice": {
		"validate": "ksa_accounts.events.accounts.sales_invoice.create_advance_retention_entry",
		"on_submit": "ksa_accounts.events.accounts.sales_invoice.create_advance_retention_entry"
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"ksa_accounts.tasks.all"
# 	],
# 	"daily": [
# 		"ksa_accounts.tasks.daily"
# 	],
# 	"hourly": [
# 		"ksa_accounts.tasks.hourly"
# 	],
# 	"weekly": [
# 		"ksa_accounts.tasks.weekly"
# 	]
# 	"monthly": [
# 		"ksa_accounts.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "ksa_accounts.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "ksa_accounts.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "ksa_accounts.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"ksa_accounts.auth.validate"
# ]

fixtures = [
	{
		"dt":
		"Custom Field",
		"filters": [[
			"name", "in",
			[
				'Account-ksa_account_position',
				'Account-ksa_account_title',
				'Account-ksa_account_type',
				'Sales Invoice-apply_advance_deduction',
				'Sales Invoice-apply_retention_deduction',
				'Sales Invoice-advance_deduction_percentage',
				'Sales Invoice-retention_deduction_percentage'
			]
		]]
	}
]
