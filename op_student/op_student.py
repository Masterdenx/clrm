# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp import tools



class OpStudent(models.Model):
    _name = 'op.student'
    _inherits = {'res.partner': 'partner_id'}
    _rec_name = 'id_number'

    middle_name = fields.Char('Middle Name', size=128, required=True)
    last_name = fields.Char('Last Name', size=128, required=True)
    birth_date = fields.Date('Birth Date', required=True)
    blood_group = fields.Selection(
        [('A+', 'A+ve'), ('B+', 'B+ve'), ('O+', 'O+ve'), ('AB+', 'AB+ve'),
         ('A-', 'A-ve'), ('B-', 'B-ve'), ('O-', 'O-ve'), ('AB-', 'AB-ve')],
        'Blood Group')
    gender = fields.Selection(
        [('m', 'Male'), ('f', 'Female'),
         ('o', 'Other')], 'Gender', required=True)
    nationality = fields.Many2one('res.country', 'Nationality')
    library_card = fields.Char('Library Card', size=64)
    emergency_contact = fields.Many2one(
        'res.partner', 'Emergency Contact')
    pan_card = fields.Char('PAN Card', size=64)
    bank_acc_num = fields.Char('Bank Acc Number', size=64)
    visa_info = fields.Char('Visa Info', size=64)
    id_number = fields.Char('ID Card Number', size=25, required=True)
    cod_carnet = fields.Char('ID Del Carnet', size=15)
    photo = fields.Binary('Photo')
    photo_medium = fields.Binary(
        string="Medium photo", store=False, compute="_get_image"
    )
    #batch_ids = fields.Many2many('op.batch', string='Batch')
    partner_id = fields.Many2one(
        'res.partner', 'Partner', required=True, ondelete="cascade")
    # health_lines = fields.One2many('op.health', 'student_id', 'Health Detail')
    allocation_ids = fields.Many2many('op.assignment', string='Assignment')
    alumni_boolean = fields.Boolean('Alumni Student')
   # passing_year = fields.Many2one('op.batch', 'Passing Year')
    current_position = fields.Char('Current Position', size=256)
    current_job = fields.Char('Current Job', size=256)
    email = fields.Char('Email', size=128)
    phone = fields.Char('Phone Number', size=256)
    user_id = fields.Many2one('res.users', 'User')
    #placement_line = fields.One2many(
        #'op.placement.offer', 'student_id', 'Placement Details')
    #activity_log = fields.One2many(
        #'op.activity', 'student_id', 'Activity Log')
#    parent_ids = fields.Many2many('op.parent', string='Parent')
    gr_no = fields.Char("GR Number", size=20)
    invoice_exists = fields.Boolean('Invoice')
    mods_attended_ids = fields.Many2many('op.course', string='Modulos Vistos')
    mods_passed = fields.Integer(
        string='Modulos aprobados', compute="_get_aprobados"
    )
    total_hours = fields.Integer(
        string='Horas aprobadas', compute="_get_horas"
    )
    course_state = fields.Selection(
        [
            ('aprobo', 'Aprobado'),
            ('curso', 'En proceso'),
            ('retira', 'Retirado')
        ], string="Estatus"
    )
    cert_qr = fields.Binary(
        string=u'Código QR', compute="_compute_qr_depends", store=False
    )

    @api.multi
    def create_invoice(self):
        """ Create invoice for fee payment process of student """

        invoice_pool = self.env['account.invoice']

        default_fields = invoice_pool.fields_get(self)
        invoice_default = invoice_pool.default_get(default_fields)

        for student in self:
            type = 'out_invoice'
            partner_id = student.partner_id.id
            onchange_partner = invoice_pool.onchange_partner_id(
                type, partner_id)
            invoice_default.update(onchange_partner['value'])

            invoice_data = {
                'partner_id': student.partner_id.id,
                'date_invoice': fields.Date.today(),

            }

        invoice_default.update(invoice_data)
        invoice_id = invoice_pool.create(invoice_default).id
        self.write({'invoice_ids': [(4, invoice_id)], 'invoice_exists': True})
        form_view = self.env.ref('account.invoice_form')
        tree_view = self.env.ref('account.invoice_tree')
        value = {
            'domain': str([('id', '=', invoice_id)]),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.invoice',
            'view_id': False,
            'views': [(form_view and form_view.id or False, 'form'),
                      (tree_view and tree_view.id or False, 'tree')],
            'type': 'ir.actions.act_window',
            'res_id': invoice_id,
            'target': 'current',
            'nodestroy': True
        }
        return value

    @api.multi
    def action_view_invoice(self):
        '''
        This function returns an action that
        display existing invoices of given student ids and show a invoice"
        '''
        result = self.env.ref('account.action_invoice_tree1')
        id = result and result.id or False
        result = self.env['ir.actions.act_window'].browse(id).read()[0]
        # compute the number of invoices to display
        inv_ids = []
        for so in self:
            inv_ids += [invoice.id for invoice in so.invoice_ids]
        # choose the view_mode accordingly
        if len(inv_ids) > 1:
            result['domain'] = \
                "[('id','in',[" + ','.join(map(str, inv_ids)) + "])]"
        else:
            res = self.env.ref('account.invoice_form')
            result['views'] = [(res and res.id or False, 'form')]
            result['res_id'] = inv_ids and inv_ids[0] or False
        return result

    @api.depends('course_state')
    def _compute_qr_depends(self):
        for student in self:
            if(student.course_state == 'aprobo'):
                direccion = \
                    'http://certs.labviv.venesis.org.ve/?system=labviv&carnet='\
                    + str(student.cod_carnet) + '&ci=' + str(student.id_number)
                qr = QRCode(version=1, error_correction=ERROR_CORRECT_L)
                qr.add_data(direccion)
                qr.make(fit=True)
                im = qr.make_image()
                buffer_io = cStringIO.StringIO()
                im.save(buffer_io)
                student.qr_certificate = buffer_io.getvalue().encode('base64')
                student.qr_certificate = tools.image_resize_image(
                    student.qr_certificate, (200, 200)
                )

    @api.one
    @api.depends("photo")
    def _get_image(self):
        """ calculate the images sizes and set the images to the corresponding
            fields
        """
        image = self.photo
        data = tools.image_resize_image(
            image, size=(250, 300), encoding='base64', filetype=None,
            avoid_if_small=False
        )
        self.photo_medium = data
        return True

    """@api.multi
    def _get_aprobados(self):
        print 'aprobados'
        self.aprobados = len(self.mods_attended_ids)
        return len(self.mods_attended_ids)

    @api.multi
    def _get_horas(self):
        a = 0
        for i in self.mods_attended_ids:
            print str(i.duration)
            a = a + i.duration
        self.total_horas = a
"""