// Copyright (c) 2022, Havenir Solutions and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Kingdom of Saudi Arabia VAT"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"reqd": 1
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"reqd": 1,
			"width": "60px"
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1,
			"width": "60px"
		}
	],
	"formatter": function(value, row, column, data, default_formatter) {
		if (data
			&& (data.title=='VAT on Sales' || data.title=='VAT on Purchases')
			&& data.title==value) {
			value = $(`<span>${value}</span>`);
			var $value = $(value).css("font-weight", "bold");
			value = $value.wrap("<p></p>").parent().html();
			return value
		}else if (data.title=='Grand Total'){
			if (data.title==value) {
				value = $(`<span>${value}</span>`);
				var $value = $(value).css("font-weight", "bold");
				value = $value.wrap("<p></p>").parent().html();
				return value
			}else{
				value = default_formatter(value, row, column, data);
				value = $(`<span>${value}</span>`);
				var $value = $(value).css("font-weight", "bold");
				value = $value.wrap("<p></p>").parent().html();
				return value
			}
		}else{
			value = default_formatter(value, row, column, data);
			return value;
		}
	}
};
