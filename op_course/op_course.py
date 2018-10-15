# -*- coding: utf-8 -*-
###############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
#
#    Modifications by Laboratorio Vivencial para la Formación de Investigadoras
#    e Investigadores en Aplicaciones Libres 2017. VeneSis-CPP (Luis Aviles,
#    César Cordero, Ángel Ramírez Isea, Enmanuel Cubillán, Asociación
#    Cooperativa Simón Rodríguez para el Conocimiento Libre, R.S.).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from openerp import models, fields


class OpCourse(models.Model):
    _name = 'op.course'

    name = fields.Char('Name', size=32, required=True)
    code = fields.Char('Code', size=8, required=True)
    evaluation_type = fields.Selection(
        [('normal', 'Normal'), ('GPA', 'GPA'), ('CWA', 'CWA'), ('CCE', 'CCE')],
        'Evaluation Type', required=True)
    #payment_term = fields.Many2one('account.payment.term', 'Payment Term')
    subject_ids = fields.Many2many('op.subject', string='Subject(s)')
    duration = fields.Integer(
        u'Duración del curso',
        help='Ingrese la duracion del curso en horas académicas'
    )
    imagen_curs = fields.Binary(string='Logo del modulo')
#    batch_ids = fields.Many2many('op.batch', string='Batch')
    faculty_id = fields.Many2one('op.faculty', 'Faculty')
