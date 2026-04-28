# Copyright (c) 2026, ok and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class MetalPrice(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		close_price: DF.Currency
		comodity: DF.Data | None
		created_at: DF.Datetime | None
		metal_ticker: DF.Link | None
		name: DF.Int | None
		price_date: DF.Date | None
		ticker_name: DF.Data | None
		unit_of_mesure: DF.Data | None
		volume: DF.Float
	# end: auto-generated types

	pass
