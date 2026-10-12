# -*- coding: utf-8 -*-
import json
import logging
import re
from datetime import datetime, date
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'


class HospitalCareController(http.Controller):

    @http.route([
        '/website_hospital/appointment/submit',
        '/website_hospitality_luxe/enquiry/submit'
    ], type='http', auth='public', methods=['POST'], website=True, csrf=False)
    def submit_appointment(self, **post):
        """Processes patient appointment requests with clinical validation."""
        patient_name = (post.get('patient_name') or post.get('name') or '').strip()
        patient_email = (post.get('patient_email') or post.get('email') or '').strip()
        patient_phone = (post.get('patient_phone') or post.get('phone') or '').strip()
        department = (post.get('department') or 'General Medicine').strip()
        doctor_name = (post.get('doctor_name') or post.get('room_type') or 'Consultant Specialist').strip()
        appointment_date_str = (post.get('appointment_date') or post.get('checkin_date') or '').strip()
        time_slot = (post.get('time_slot') or post.get('guests') or 'Morning (09:00 - 12:00)').strip()
        symptoms = (post.get('symptoms') or post.get('message') or '').strip()

        errors = []
        if not patient_name:
            errors.append('Patient name is required.')
        if not patient_phone:
            errors.append('Contact phone number is required for appointment confirmation.')
        if not patient_email or not re.match(EMAIL_REGEX, patient_email):
            errors.append('A valid email address is required.')
        if not appointment_date_str:
            errors.append('Appointment date is required.')

        appt_date = None
        if appointment_date_str:
            try:
                appt_date = datetime.strptime(appointment_date_str, '%Y-%m-%d').date()
                if appt_date < date.today():
                    errors.append('Appointment date cannot be in the past. Please select today or a future date.')
            except ValueError:
                errors.append('Invalid date format. Please use YYYY-MM-DD.')

        is_json = request.httprequest.headers.get('X-Requested-With') == 'XMLHttpRequest' or 'application/json' in request.httprequest.headers.get('Accept', '')

        if errors:
            error_msg = ' '.join(errors)
            if is_json:
                return request.make_response(
                    json.dumps({'status': 'error', 'message': error_msg}),
                    headers={'Content-Type': 'application/json'}
                )
            return request.render('website_hospitality_luxe.booking_enquiry_result', {
                'status': 'error',
                'message': error_msg
            })

        # Process lead creation in CRM if installed
        lead_created = False
        crm_lead_model = request.env.get('crm.lead')
        if crm_lead_model is not None and request.env['ir.module.module'].sudo().search([('name', '=', 'crm'), ('state', '=', 'installed')]):
            try:
                lead_vals = {
                    'name': f"Doctor Appointment: {patient_name} - {department}",
                    'contact_name': patient_name,
                    'email_from': patient_email,
                    'phone': patient_phone,
                    'description': (
                        f"Patient Appointment Request\n"
                        f"----------------------------\n"
                        f"Patient Name: {patient_name}\n"
                        f"Phone: {patient_phone}\n"
                        f"Email: {patient_email}\n"
                        f"Department: {department}\n"
                        f"Doctor Requested: {doctor_name}\n"
                        f"Appointment Date: {appt_date}\n"
                        f"Preferred Time Slot: {time_slot}\n"
                        f"Symptoms / Reason for Visit: {symptoms}\n"
                    ),
                    'priority': '2',
                }
                lead = crm_lead_model.sudo().create(lead_vals)
                lead_created = bool(lead)
                _logger.info("Successfully created crm.lead ID %s for appointment %s", lead.id, patient_name)
            except Exception as e:
                _logger.warning("CRM lead creation failed gracefully: %s", e)

        success_msg = (
            f"Thank you, {patient_name}! Your appointment request for {department} with "
            f"{doctor_name} on {appt_date} ({time_slot}) has been received. "
            f"Our patient care coordinator will call {patient_phone} to confirm your appointment time."
        )

        if is_json:
            return request.make_response(
                json.dumps({
                    'status': 'success',
                    'message': success_msg,
                    'lead_created': lead_created
                }),
                headers={'Content-Type': 'application/json'}
            )

        return request.render('website_hospitality_luxe.booking_enquiry_result', {
            'status': 'success',
            'message': success_msg,
            'lead_created': lead_created
        })

    @http.route([
        '/hospital/contact/submit',
        '/website_hospital/contact/submit'
    ], type='http', auth='public', methods=['POST'], website=True, csrf=False)
    def submit_contact(self, **post):
        """Processes contact enquiries and patient questions."""
        patient_name = (post.get('patient_name') or post.get('name') or '').strip()
        patient_email = (post.get('patient_email') or post.get('email') or '').strip()
        patient_phone = (post.get('patient_phone') or post.get('phone') or '').strip()
        department = (post.get('department') or 'General Medicine').strip()
        inquiry_type = (post.get('inquiry_type') or 'General Inquiry').strip()
        appointment_date_str = (post.get('appointment_date') or '').strip()
        message = (post.get('message') or post.get('question') or '').strip()

        errors = []
        if not patient_name:
            errors.append('Patient name is required.')
        if not patient_phone:
            errors.append('Contact phone number is required.')
        if not patient_email or not re.match(EMAIL_REGEX, patient_email):
            errors.append('A valid email address is required.')
        if not message:
            errors.append('Please describe your inquiry or symptoms.')

        appt_date = None
        if appointment_date_str:
            try:
                appt_date = datetime.strptime(appointment_date_str, '%Y-%m-%d').date()
                if appt_date < date.today():
                    errors.append('Preferred date cannot be in the past.')
            except ValueError:
                errors.append('Invalid date format.')

        is_json = request.httprequest.headers.get('X-Requested-With') == 'XMLHttpRequest' or 'application/json' in request.httprequest.headers.get('Accept', '')

        if errors:
            error_msg = ' '.join(errors)
            if is_json:
                return request.make_response(
                    json.dumps({'status': 'error', 'message': error_msg}),
                    headers={'Content-Type': 'application/json'}
                )
            return request.render('website_hospitality_luxe.booking_enquiry_result', {
                'status': 'error',
                'message': error_msg
            })

        # Process lead creation in CRM if installed
        lead_created = False
        crm_lead_model = request.env.get('crm.lead')
        if crm_lead_model is not None and request.env['ir.module.module'].sudo().search([('name', '=', 'crm'), ('state', '=', 'installed')]):
            try:
                lead_vals = {
                    'name': f"Hospital Inquiry: {patient_name} - {inquiry_type} ({department})",
                    'contact_name': patient_name,
                    'email_from': patient_email,
                    'phone': patient_phone,
                    'description': (
                        f"Patient / Visitor Contact Inquiry\n"
                        f"---------------------------------\n"
                        f"Name: {patient_name}\n"
                        f"Phone: {patient_phone}\n"
                        f"Email: {patient_email}\n"
                        f"Department: {department}\n"
                        f"Inquiry Type: {inquiry_type}\n"
                        f"Preferred Date: {appt_date or 'N/A'}\n"
                        f"Message / Details:\n{message}\n"
                    ),
                    'priority': '2',
                }
                lead = crm_lead_model.sudo().create(lead_vals)
                lead_created = bool(lead)
                _logger.info("Successfully created crm.lead ID %s for inquiry from %s", lead.id, patient_name)
            except Exception as e:
                _logger.warning("CRM lead creation failed gracefully: %s", e)

        success_msg = (
            f"Thank you, {patient_name}! Your inquiry regarding {inquiry_type} ({department}) "
            f"has been received. Our clinical coordinator will contact you at {patient_phone} shortly."
        )

        if is_json:
            return request.make_response(
                json.dumps({
                    'status': 'success',
                    'message': success_msg,
                    'lead_created': lead_created
                }),
                headers={'Content-Type': 'application/json'}
            )

        return request.render('website_hospitality_luxe.booking_enquiry_result', {
            'status': 'success',
            'message': success_msg,
            'lead_created': lead_created
        })

