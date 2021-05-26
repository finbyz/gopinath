frappe.ui.form.on("Stock Entry", {
refresh: function(frm){
    if (frm.doc.docstatus != 1)
        {
            frm.add_custom_button("Rename", function() {
                frappe.call({
                    method: "gopinath.api.rename_se",
                    args:{
                        "existing_name": cur_frm.doc.name,
                        "series_value": cur_frm.doc.series_value,
                        "naming_series":cur_frm.doc.naming_series,
                    },
                    callback: function(r){
                        if(r.message){
                            frappe.set_route('Form', 'Stock Entry', r.message)
                        }
                    }
                })
            })
        }
    }
})