# Copyright (c) 2026, ok and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class MetalTicker(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		comodity: DF.Link | None
		metal_name: DF.Data
		ticker_symbol: DF.Data | None
		unit_of_measure: DF.Link | None
	# end: auto-generated types

	pass
