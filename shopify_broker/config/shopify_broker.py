from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Settings"),
			"icon": "icon-star",
			"items": [
				{
					"type": "doctype",
					"name": "Broker Settings",
					"description": _("Setup API Key and Secret of Shopify Public App.")
				}
			]
		}
	]