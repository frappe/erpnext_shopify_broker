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
	print shop
	api_key = "96d040e1b908d6b39a337300e7fff77c"
	scopes = "read_products, write_products, read_customers, write_customers, read_orders, write_orders"
	redirect_uri = "https://myacc.localtunnel.me/api/method/shopify_broker.shopify_broker.generate_token"

	auth_url = "https://{}/admin/oauth/authorize?client_id={}&scope={}&redirect_uri={}\
		".format(shop, api_key, scopes, redirect_uri)
		
	print auth_url
		
	return {"auth_url": auth_url}

@frappe.whitelist(allow_guest=True)
def generate_token():
	form_dict = frappe.local.form_dict	
	
	frappe.set_user("Administrator")
	
	token_dict = {
		"client_id": "96d040e1b908d6b39a337300e7fff77c",
		"client_secret": "de1593719e236b571f0a8e251e366fd5",
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
	
	print res.text
	
	frappe.response["type"] = 'redirect'
	
	frappe.response["location"] = "https://{}/admin/apps".format(cred_dict["shop"])
	
	