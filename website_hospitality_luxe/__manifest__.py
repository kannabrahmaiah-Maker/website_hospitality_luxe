# -*- coding: utf-8 -*-
{
    'name': 'Website Hospital Care - Premium Hospital & Healthcare Theme',
    'version': '19.0.1.0.0',
    'category': 'Theme/Healthcare',
    'summary': 'Realistic, Modern & Attractive Hospital & Healthcare Website Theme for Odoo 19 with 15 Medical Drag-and-Drop Snippets',
    'description': """
Website Hospital Care
=====================
A commercial-grade, realistic, high-converting hospital and healthcare website theme for Odoo 19.
Designed specifically for multi-specialty hospitals, medical centers, clinics, super-specialty institutes, 
and diagnostic healthcare systems.

Key Features & Highlights:
--------------------------
* 100% Compatible with Odoo 19 Community & Enterprise
* Pure dependency on 'website' module - no core modifications required
* 15 Bespoke Website Builder Drag-and-Drop Snippets under a dedicated "Hospital Care" tab:
  1. Hospital Hero Banner (High-impact clinical campus hero with instant appointment CTA)
  2. Quick Doctor Appointment Bar (Interactive appointment booking bar with date & slot pickers)
  3. Emergency & Trauma 24/7 Callout (High-visibility emergency dispatch & ambulance hotline)
  4. Medical Departments Grid (Cardiology, Neuro, Ortho, Pediatrics, Oncology, Trauma)
  5. Senior Doctors & Specialists (Doctor directory with qualifications, OPD schedule & consultation CTA)
  6. Hospital Milestones & Stats (Counters for beds, surgeries, doctors, and recovery rate)
  7. Hospital Facilities & Tech (Robotic surgery, modular OTs, 3T MRI, 24/7 labs)
  8. Preventive Health Checkup Packages (Master health, cardiac, executive screening tiers)
  9. Patient Recovery Reviews (Clinical patient testimonials with verified treatment badges)
  10. Hospital Accreditations (JCI, NABH, NABL, and ISO global standards)
  11. Medical Facilities Virtual Tour (Tabbed showcase of campus, recovery rooms, and OTs)
  12. Cashless Insurance Partners (Empanelled insurance providers and TPA desk info)
  13. Patient & Visitor FAQ (Comprehensive accordion answering admission, visiting hours, and tests)
  14. Hospital Location & Campus Access (Interactive campus directions, emergency gate coordinates)
  15. Closing Appointment CTA (High-conversion medical booking banner)
* 8 Ready-to-Publish Responsive Healthcare Pages:
  - Homepage (Curated narrative layout with clinical trust flow)
  - Doctors Directory (/doctors - Searchable specialists with OPD timings and direct booking)
  - Centres of Clinical Excellence (/departments - Full multidisciplinary department profiles)
  - Hospital Facilities (/facilities - Modular OTs, Da Vinci robotics, private recovery rooms)
  - About Us (/about-us - Medical heritage, clinical ethics, board of doctors, and accreditations)
  - Patient & Visitor Guide (/patient-guide - Inpatient admission protocol, TPA cashless claims, visiting hours)
  - Hospital Gallery (/gallery - High-definition visual photo showcase)
  - Contact & Emergency (/contactus - Emergency hotline, ambulance dispatch, and appointment desk)
* Real-time Patient Appointment Engine:
  - Dynamic client-side date validation (past dates disabled)
  - Server-side clinical validation with instant JSON or formatted response
  - Seamless automatic routing to CRM pipeline ('crm.lead') when CRM is installed
* Clinical Color Palette:
  - Trust Navy (#0B4F6C / #073B52)
  - Healthcare Cyan (#00A896 / #028090)
  - Clean Soft Ice (#F4F9F9)
  - 24/7 Emergency Alert Red (#E63946)
* Tested and optimized across Mobile (375px), Tablet (768px), and Desktop (1440px)
* Accessibility compliant with high contrast ratios and prefers-reduced-motion support
    """,
    'author': 'Kanna',
    'maintainer': 'Kanna',
    'website': 'https://apps.odoo.com/apps/modules/19.0/website_hospitality_luxe',
    'license': 'OPL-1',
    'price': 49.00,
    'currency': 'EUR',
    'depends': ['website'],
    'data': [
        'views/snippets/s_hospital_hero.xml',
        'views/snippets/s_appointment_bar.xml',
        'views/snippets/s_emergency_callout.xml',
        'views/snippets/s_departments_grid.xml',
        'views/snippets/s_featured_doctors.xml',
        'views/snippets/s_hospital_stats.xml',
        'views/snippets/s_services_facilities.xml',
        'views/snippets/s_health_packages.xml',
        'views/snippets/s_patient_testimonials.xml',
        'views/snippets/s_accreditation_badges.xml',
        'views/snippets/s_virtual_tour.xml',
        'views/snippets/s_insurance_partners.xml',
        'views/snippets/s_patient_faq.xml',
        'views/snippets/s_hospital_location.xml',
        'views/snippets/s_appointment_cta.xml',
        'views/snippets.xml',
        'views/pages.xml',
        'views/header.xml',
        'views/footer.xml',
        'views/contactus.xml',
        'data/website_pages.xml',
        'data/website_menu.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'website_hospitality_luxe/static/src/scss/theme.scss',
            'website_hospitality_luxe/static/src/js/booking_enquiry.js',
        ],
    },
    'images': [
        'static/description/banner.png',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
