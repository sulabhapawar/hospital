from openerp.osv import fields, osv

class hospital_hospital(osv.osv):
    _name='hospital.hospital'
    _description = "hospital"
    
    def button_function(self,cr,uid,id,context=None):
        print "====================id",id
        return True
    
    def onchange_fees(self, cr, uid, ids, fees, total_days, context=None):
        msg = False
        if total_days == 0: 
            charge_per_day = 0
            msg = {
                   'title':"Divsion by zero error",
                   'message':"Division by zero is not allowed",
                   }
        else:
            charge_per_day = fees/total_days

        return {
                'value':{
                         'charge_per_day':charge_per_day,
                         },
                'warning':msg,
                
                'domain':{
                          'partner_id':[('id','=',1)]
                          }
                }
    
    def name_get(self,cr,uid,ids,context=None):
        res = super(hospital_hospital,self).name_get(cr,uid,ids,context=None)
        print "====================================//////////////name_get",res
        new_list = []
        for i in res:
            new_list.append((i[0],i[1]+" Sulabha"))
        return new_list
    
    _columns={
              'name':fields.char('Hospital Name'),
              'hospital_addr':fields.text('Hospital Address'),
              'doctor_id':fields.one2many('doctor.doctor','hospital_id','Doctors'),
              'paitent_id':fields.one2many('paitent.paitent','paitent_hospital_id','Paitents'),
              'partner_id':fields.many2one('res.partner','Partner'),
              'fees':fields.float("Fees"),
              'total_days':fields.float("Total Days"),
              'charge_per_day':fields.float("Charge per day")
              }

class doctor_doctor(osv.osv):
    _name='doctor.doctor'
    _description = "doctor"
    
    def open_choice_hospital(self,cr,uid,ids,context):
       
       return{
            'name': 'Choose Hospital',
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'ask.hospital',
            'view_id': False,
            'target':"new",
            'type': 'ir.actions.act_window',              
              }
               
    def open_hospital(self,cr,uid,ids,context=None):
       hospital_id = self.read(cr,uid,ids,['hospital_id'],context)
#        [{'id':<>,hospital_id:(id,name)}]
       
       print "=======================================================================",hospital_id
       hospital_id = hospital_id[0].get('hospital_id',False)[0]
       print "================================================",hospital_id
       return{
            'name': 'Hospital',
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'hospital.hospital',
            'view_id': False,
            'target':"new",
            'type': 'ir.actions.act_window',              
              }
       
   
    _columns={
              'name':fields.char(string='Doctor name'),
              'qualification':fields.char(string='Qualification'),
              'specialist':fields.char(string='specialist of'),     
              'paitents_id':fields.many2many('paitent.paitent','paitent_paitent_doctor_doctor_relation','doctor_id','paitent_id','paitents'),
              'hospital_id':fields.many2one('hospital.hospital',string='hospital'),
              'attachemnet_id':fields.binary("Certificate")              
              }
    
class paitent_paitent(osv.osv):
    _name='paitent.paitent'
    _description='paitent'
    _columns={
              'name':fields.char(string='Paitent name',required=True),
              'age':fields.integer('Age'),
              'suffering_from':fields.char(string='description about disease'),      
              'address':fields.text('Paitent address'),
              'doctors_id':fields.many2many('doctor.doctor','paitent_paitent_doctor_doctor_relation','paitent_id','doctor_id','doctors'),
              'paitent_hospital_id':fields.many2one('hospital.hospital',string='hospital'),
              'hospital_addr':fields.related('paitent_hospital_id','hospital_addr',string='Address',type='text'),
              'hospital_partner_id':fields.related('paitent_hospital_id','partner_id',type="many2one",relation="res.partner",string = "Hospital Partner")
              }
    