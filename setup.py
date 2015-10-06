# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

version = '1.0.0'

setup(
    name='erpnext_shopify_broker',
    version=version,
    description='A broker to install Shopify public app.',
    author='Frappe Technologies Pvt. Ltd.',
    author_email='info@frappe.io',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=("frappe",),
)
