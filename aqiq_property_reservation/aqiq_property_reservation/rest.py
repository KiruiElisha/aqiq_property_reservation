import frappe
from frappe import _



def sales_order_on_submit(self, method):
	for i in self.items:
		item = frappe.get_doc('Item', i.item_code)
		item.custom_unit_status = 'Leased'
		item.save(ignore_permissions=True)
		item.reload()


def sales_order_on_cancel(self, method):
	for i in self.items:
		item = frappe.get_doc('Item', i.item_code)
		item.custom_unit_status = 'Available'
		item.save(ignore_permissions=True)
		item.reload()


def sales_invoice_on_submit(self, method):
	for i in self.items:
		item = frappe.get_doc('Item', i.item_code)
		if self.is_return == 0:
			item.custom_unit_status = 'Booked'
		else:
			item.unit_status = 'Available'
		item.save(ignore_permissions=True)
		item.reload()

def sales_invoice_on_cancel(self, method):
	for i in self.items:
		item = frappe.get_doc('Item', i.item_code)
		item.custom_unit_status = 'Available'
		item.save(ignore_permissions=True)
		item.reload()

def delivery_note_on_submit(self, method):
	for i in self.items:
		item = frappe.get_doc('Item', i.item_code)
		item.custom_unit_status = 'Sold'
		item.save(ignore_permissions=True)
		item.reload()
		


def stock_entry_validate(self, method):
	if self.stock_entry_type == 'Plotting':
		if len(self.items)>1:
			land = self.items[0]
			land_qty = land.transfer_qty
			land_rate = land.basic_rate
			total_plot_qty = 0
			for i in self.items[1:]:
				total_plot_qty += i.transfer_qty
			plot_rate = (land_qty/total_plot_qty)*land_rate

			for i in self.items[1:]:
				i.basic_rate = plot_rate
				i.amount = i.transfer_qty*plot_rate

