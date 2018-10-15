# -*- coding: utf-8 -*-
{
    'name': 'classroom',
    'version': '1.0',
    'category': 'apps',
    'summary': 'Opportunities, Activities, ',
    'description': "Modulo dedicado a la Gestion de Aulas Virtuales",
    'website': '',
    'depends': [
        'document', 'hr', 'web', 'website', 'mail', 'calendar', 'contacts',
        'board',
    ],
    'data': [
        'security/op_security.xml',
        'op_student/op_student_view.xml',
        'op_faculty/op_faculty_view.xml',
        'op_assignment/op_assignment_view.xml',
        'op_exam/op_exam_view.xml',
        'op_exam_attendees/op_exam_attendees_view.xml',
        'menu/faculty_menu.xml',
        'op_timetable/op_timetable_view.xml',
        'op_student/student_dashboard_view.xml',
        'menu/student_menu.xml',
        'op_admission/op_admission_view.xml',
        'op_classroom/op_classroom_view.xml',
        'op_course/op_course_view.xml',
        'op_exam_type/op_exam_type_view.xml',
        'menu/openeducat_erp_menu.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
