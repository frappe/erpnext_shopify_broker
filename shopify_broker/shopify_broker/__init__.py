import frappe
from werkzeug.wrappers import Response
import hashlib, base64, hmac
import requests
import json

cred_dict = {}

@frappe.whitelist(allow_guest=True)
def authenticate_user():
	form_dict = frappe.local.form_dict
	
	frappe.response["type"] = 'page'
	
	frappe.response["page_name"] = "setup_shopify"	

@frappe.whitelist(allow_guest=True)
def validate_erp_user(shop, site_name, email, password):
	global cred_dict
	cred_dict = {"shop": shop, "site_name": site_name, "email": email, "password": password}
	
	res = requests.post(url="https://{}/api/method/login?usr={}&pwd={}".format(site_name, email, password))
	if res.json()["full_name"]:
		return generate_redirect_uri(shop)

def generate_redirect_uri(shop): 
	broker_settings = get_brocker_details()
	api_key = broker_settings.api_key
	scopes = "read_products, write_products, read_customers, write_customers, read_orders, write_orders"
	redirect_uri = "https://myacc.localtunnel.me/api/method/shopify_broker.shopify_broker.generate_token"

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
	print 
	update_shopify_settings(res.json()['access_token'])
	
def update_shopify_settings(access_token):
	s = requests.Session()
	res = s.post(url="https://{}/api/method/login?usr={}&pwd={}".format(cred_dict["site_name"], cred_dict["email"], cred_dict["password"]))
	
	url = "https://{}/api/resource/Shopify Settings/Shopify Settings".format(cred_dict["site_name"])
	data = {
		"access_token": access_token,
		"shopify_url": cred_dict["shop"]
	}
	res = s.put(url, data='data='+json.dumps(data), headers={'content-type': 'application/x-www-form-urlencoded'})	
	
	frappe.response["type"] = 'redirect'
	frappe.response["location"] = "https://{}/admin/apps".format(cred_dict["shop"])
	
	