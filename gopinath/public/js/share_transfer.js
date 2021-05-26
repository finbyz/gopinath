frappe.ui.form.on('Share Transfer', {
    from_shareholder: function(frm){
        if(frm.doc.from_shareholder){
            frappe.db.get_value("Shareholder",frm.doc.from_shareholder,'folio_no',function(r){
                if(r.folio_no){
                    frm.set_value('from_folio_no',r.folio_no);
                }
            })
        }
    },
    to_shareholder: function(frm){
        if(frm.doc.to_shareholder){
            frappe.db.get_value("Shareholder",frm.doc.to_shareholder,'folio_no',function(r){
                if(r.folio_no){
                    frm.set_value('to_folio_no',r.folio_no);
                }
            })
        }
    }

})