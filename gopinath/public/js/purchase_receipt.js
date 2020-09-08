frappe.ui.form.on("Purchase Receipt", {
    validate: function (frm) {
        frm.doc.items.forEach(function (d) {
            frappe.db.get_value("Item", d.item_code, 'maintain_as_is_stock', function (r) {
                if (!d.supplier_qty) {
                    frappe.model.set_value(d.doctype, d.name, 'supplier_qty', d.qty)
                }
                if(d.packing_size && d.no_of_packages) {
                    frappe.model.set_value(d.doctype, d.name, 'qty', flt(d.packing_size * d.no_of_packages));
                    frappe.model.set_value(d.doctype, d.name, 'received_qty', flt(d.packing_size * d.no_of_packages));
                    if (r.maintain_as_is_stock) {
                        if (!d.concentration) {
                            frappe.throw("Please add concentration for Item " + d.item_code)
                        }
                        frappe.model.set_value(d.doctype, d.name, 'quantity', d.qty * d.concentration / 100);
                    }
                    else {
                        frappe.model.set_value(d.doctype, d.name, 'quantity', flt(d.qty));
                    }
                }
                if (d.supplier_packing_size && d.supplier_no_of_packages) {
                    frappe.model.set_value(d.doctype, d.name, 'supplier_qty', flt(d.supplier_packing_size * d.supplier_no_of_packages));
                    if (r.maintain_as_is_stock) {
                        if (!d.supplier_concentration) {
                            frappe.throw("Please add supplier concentration for Item " + d.item_code)
                        }
                        frappe.model.set_value(d.doctype, d.name, 'supplier_quantity', d.supplier_qty * d.supplier_concentration / 100);
                    }
                    else {
                        frappe.model.set_value(d.doctype, d.name, 'supplier_quantity', flt(d.supplier_qty));
                    }
                }
                if (d.accepted_packing_size && d.accepted_no_of_packages) {
                    frappe.model.set_value(d.doctype, d.name, 'accepted_qty', flt(d.accepted_packing_size * d.accepted_no_of_packages));
                    if (r.maintain_as_is_stock) {
                        frappe.model.set_value(d.doctype, d.name, 'quantity', d.accepted_qty * d.accepted_concentration / 100);
                    }
                    else {
                        frappe.model.set_value(d.doctype, d.name, 'quantity', flt(d.accepted_qty));
                    }
                }
                if (!d.accepted_quantity) {
                    frappe.model.set_value(d.doctype, d.name, 'short_quantity', flt(d.quantity -  d.supplier_quantity))
                }
                else {
                    frappe.model.set_value(d.doctype, d.name, 'short_quantity', flt(d.accepted_quantity - d.supplier_quantity))
                }
                frappe.model.set_value(d.doctype, d.name, 'amount_difference', flt(d.short_quantity) * flt(d.price))
            });
        });
    },
    cal_rate_qty: function (frm, cdt, cdn) {
        let d = locals[cdt][cdn];
        frappe.db.get_value("Item", d.item_code, 'maintain_as_is_stock', function (r) {
            if (!d.supplier_qty) {
                frappe.model.set_value(d.doctype, d.name, 'supplier_qty', d.qty)
            }
            if (d.packing_size && d.no_of_packages) {
                frappe.model.set_value(d.doctype, d.name, 'qty', flt(d.packing_size * d.no_of_packages));
                frappe.model.set_value(d.doctype, d.name, 'received_qty', flt(d.packing_size * d.no_of_packages));
                if (r.maintain_as_is_stock) {
                    if (!d.concentration) {
                        frappe.throw("Please add concentration for Item " + d.item_code)
                    }
                    frappe.model.set_value(d.doctype, d.name, 'quantity', d.qty * d.concentration / 100);
                }
                else {
                    frappe.model.set_value(d.doctype, d.name, 'quantity', flt(d.qty));
                }
            }
            if (d.supplier_packing_size && d.supplier_no_of_packages) {
                frappe.model.set_value(d.doctype, d.name, 'supplier_qty', flt(d.supplier_packing_size * d.supplier_no_of_packages));
                if (r.maintain_as_is_stock) {
                    if (!d.supplier_concentration) {
                        frappe.throw("Please add supplier concentration for Item " + d.item_code)
                    }
                    frappe.model.set_value(d.doctype, d.name, 'supplier_quantity', d.supplier_qty * d.supplier_concentration / 100);
                }
                else {
                    frappe.model.set_value(d.doctype, d.name, 'supplier_quantity', flt(d.supplier_qty));
                }
            }
            if (d.accepted_packing_size && d.accepted_no_of_packages) {
                frappe.model.set_value(d.doctype, d.name, 'accepted_qty', flt(d.accepted_packing_size * d.accepted_no_of_packages));
                if (r.maintain_as_is_stock) {
                    frappe.model.set_value(d.doctype, d.name, 'quantity', d.accepted_qty * d.accepted_concentration / 100);
                }
                else {
                    frappe.model.set_value(d.doctype, d.name, 'quantity', flt(d.accepted_qty));
                }
            }
            if (!d.accepted_quantity) {
                frappe.model.set_value(d.doctype, d.name, 'short_quantity', flt(d.quantity - d.supplier_quantity))
            }
            else {
                frappe.model.set_value(d.doctype, d.name, 'short_quantity', flt(d.accepted_quantity - d.supplier_quantity))
            }
            frappe.model.set_value(d.doctype, d.name, 'amount_difference', flt(d.short_quantity) * flt(d.price))
        });
    }, 
});


frappe.ui.form.on("Purchase Receipt Item", {
    quantity: function (frm, cdt, cdn) {
        frm.events.cal_rate_qty(frm, cdt, cdn)
    },
    price: function (frm, cdt, cdn) {
        frm.events.cal_rate_qty(frm, cdt, cdn)
    },
    concentration: function (frm, cdt, cdn) {
        frm.events.cal_rate_qty(frm, cdt, cdn)
    },
    packing_size: function (frm, cdt, cdn) {
        frm.events.cal_rate_qty(frm, cdt, cdn)
    },
    no_of_packages: function (frm, cdt, cdn) {
        frm.events.cal_rate_qty(frm, cdt, cdn)
    },
    supplier_packing_size: function (frm, cdt, cdn) {
        frm.events.cal_rate_qty(frm, cdt, cdn)
    },
    supplier_no_of_packages: function (frm, cdt, cdn) {
        frm.events.cal_rate_qty(frm, cdt, cdn)
    },
    supplier_quantity: function (frm, cdt, cdn) {
        frm.events.cal_rate_qty(frm, cdt, cdn)
    },
    supplier_concentration: function (frm, cdt, cdn) {
        frm.events.cal_rate_qty(frm, cdt, cdn)
    },
    accepted_packing_size: function (frm, cdt, cdn) {
        frm.events.cal_rate_qty(frm, cdt, cdn)
    },
    accepted_no_of_packages: function (frm, cdt, cdn) {
        frm.events.cal_rate_qty(frm, cdt, cdn)
    },
    accepted_quantity: function (frm, cdt, cdn) {
        frm.events.cal_rate_qty(frm, cdt, cdn)
    },
    accepted_concentration: function (frm, cdt, cdn) {
        frm.events.cal_rate_qty(frm, cdt, cdn)
    },
});