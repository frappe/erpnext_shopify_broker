# -*- coding: utf-8 -*-
from __future__ import unicode_literals

app_name = "erpnext_shopify_broker"
app_title = "ERPNext Shopify Broker"
app_publisher = "Frappe Technologies Pvt. Ltd."
app_description = "A broker to install Shopify public app."
app_icon = "icon-random"
app_color = "#9b59b6"
app_email = "info@frappe.io"
app_version = "1.0.0"
hide_in_installer = True

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/erpnext_shopify_broker/css/erpnext_shopify_broker.css"
# app_include_js = "/assets/erpnext_shopify_broker/js/erpnext_shopify_broker.js"

# include js, css files in header of web template
# web_include_css = "/assets/erpnext_shopify_broker/css/erpnext_shopify_broker.css"
# web_include_js = "/assets/erpnext_shopify_broker/js/erpnext_shopify_broker.js"

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

# before_install = "erpnext_shopify_broker.install.before_install"
# after_install = "erpnext_shopify_broker.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "erpnext_shopify_broker.notifications.get_notification_config"

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

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
	"hourly": [
		"erpnext_shopify_broker.erpnext_shopify_broker.doctype.broker_settings.broker_settings.clear_session_details"
	]
}

# Testing
# -------

# before_tests = "erpnext_shopify_broker.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "erpnext_shopify_broker.event.get_events"
# }

