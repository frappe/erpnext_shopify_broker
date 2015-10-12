# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import hashlib, base64, hmac
import requests
import json
import pickle as pk
from frappe.utils import getdate, now, time_diff_in_hours

class BrokerSettings(Document):
	pass

@frappe.whitelist(allow_guest=True)
def authenticate_user():
	form_dict = frappe.local.form_dict
	
	frappe.response["type"] = 'page'
	
	frappe.response["page_name"] = "setup_shopify"	

@frappe.whitelist(allow_guest=True)
def validate_erp_user(shop, site_name, email, password):	
	session = requests.Session()
	print "https://{}/api/method/login?usr={}&pwd={}".format(site_name, email, password)
	res = session.post(url="https://{}/api/method/login?usr={}&pwd={}".format(site_name, email, password))
	pk.dumps(session)
	if res.status_code == 200:
		if res.json()["full_name"]:
			url = "https://{}/api/resource/Shopify Settings/Shopify Settings".format(site_name)
			res = session.get(url)
			if res.status_code == 200:
				create_shopify_user_record(session, shop, site_name, email)
				return generate_redirect_uri(shop)
			else:
				return {"error": "You haven't installed ERPNent Shopify App."}
	else:
		return {"error": "Username or Password is wrong"}
	
def create_shopify_user_record(session, shop, site_name, email):
	frappe.set_user("Administrator")
	frappe.get_doc({
		"doctype": "Shopify User",
		"shop_name": shop,
		"site_name": site_name,
		"user_id": email,
		"session_details": pk.dumps(session)
	}).insert()

def generate_redirect_uri(shop): 
	broker_settings = get_brocker_details()
	api_key = broker_settings.api_key
	scopes = "read_products, write_products, read_customers, write_customers, read_orders, write_orders"
	redirect_uri = frappe.utils.get_url("/api/method/erpnext_shopify_broker.erpnext_shopify_broker.generate_token")

	auth_url = "https://{}/admin/oauth/authorize?client_id={}&scope={}&redirect_uri={}\
		".format(shop, api_key, scopes, redirect_uri)
				
	return {"auth_url": auth_url}

def get_brocker_details():
	return frappe.get_doc("Broker Settings", "Broker Settings")

@frappe.whitelist(allow_guest=True)
def generate_token():
	form_dict = frappe.local.form_dict	
	
	frappe.set_user("Administrator")
	broker_settings = get_brocker_details()
	token_dict = {
		"client_id": broker_settings.api_key,
		"client_secret": broker_settings.secret,
		"code": form_dict["code"]
	}
	url = "https://{}/admin/oauth/access_token".format(form_dict["shop"])
	res = requests.post(url= url, data=json.dumps(token_dict), headers={'Content-type': 'application/json'}) 
	update_shopify_settings(res.json()['access_token'], form_dict)
	
def update_shopify_settings(access_token, form_dict):
	shopify_user = frappe.get_doc("Shopify User", frappe.db.get_value("Shopify User", \
		{"shop_name": form_dict["shop"]}, "name"))
	session = pk.loads(shopify_user.session_details)
	
	url = "https://{}/api/resource/Shopify Settings/Shopify Settings".format(shopify_user.site_name)
	data = {
		"access_token": access_token,
		"shopify_url": form_dict["shop"],
		"app_type": "Public"
		
	}

	res = session.put(url, data='data='+json.dumps(data), headers={'content-type': 'application/x-www-form-urlencoded'})

	if res.status_code == 200:
		url = "https://{}/api/method/logout".format(shopify_user.site_name)
		res = session.get(url)
		
		frappe.response["type"] = 'redirect'
		frappe.response["location"] = "https://{}/admin/apps".format(form_dict["shop"])

def clear_session_details():
	frappe.set_user("Administrator")
	for doc in frappe.db.sql("select name from `tabShopify User` where session_details not in('')", as_dict=1):
		shopify_user = frappe.get_doc("Shopify User", doc["name"])
		if time_diff_in_hours(now(), getdate(shopify_user.creation)) > 1:
			shopify_user.session_details = ''
			shopify_user.save()
		