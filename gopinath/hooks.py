# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "gopinath"
app_title = "Gopinath"
app_publisher = "FInByz Tech Pvt Ltd"
app_description = "Custom App"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "info@finbyz.com"
app_license = "GPL 3.0"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/gopinath/css/gopinath.css"
# app_include_js = "/assets/gopinath/js/gopinath.js"

# include js, css files in header of web template
# web_include_css = "/assets/gopinath/css/gopinath.css"
# web_include_js = "/assets/gopinath/js/gopinath.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------
doctype_js = {
    "Purchase Receipt": "public/js/purchase_receipt.js",
}

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "gopinath.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "gopinath.install.before_install"
# after_install = "gopinath.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "gopinath.notifications.get_notification_config"

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
doc_events = {
    "Purchase Receipt": {
        "before_naming": "gopinath.api.before_naming",
    },
    "Stock Entry":{
        "before_naming": "gopinath.api.before_naming",
    }
}
# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"gopinath.tasks.all"
# 	],
# 	"daily": [
# 		"gopinath.tasks.daily"
# 	],
# 	"hourly": [
# 		"gopinath.tasks.hourly"
# 	],
# 	"weekly": [
# 		"gopinath.tasks.weekly"
# 	]
# 	"monthly": [
# 		"gopinath.tasks.monthly"
# 	]
# }
scheduler_events = {
 	"daily": [
		"gopinath.batch_controller.get_batch_data"
	]
}
# Testing
# -------

# before_tests = "gopinath.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "gopinath.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "gopinath.task.get_dashboard_data"
# }

