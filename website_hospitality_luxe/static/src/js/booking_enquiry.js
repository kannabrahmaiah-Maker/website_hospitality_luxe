/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.Widget.extend({
    selector: '.s_appointment_bar, .s_booking_bar, .hospital-contact-section',
    events: {
        'submit form': '_onSubmitAppointment',
    },

    start() {
        this._super(...arguments);
        const dateInput = this.el.querySelector('input[type="date"]');
        if (dateInput) {
            const today = new Date().toISOString().split('T')[0];
            dateInput.min = today;
            if (!dateInput.value) {
                dateInput.value = today;
            }
        }
    },

    async _onSubmitAppointment(ev) {
        ev.preventDefault();
        const form = ev.currentTarget;
        const submitBtn = form.querySelector('button[type="submit"]');
        const feedbackArea = form.querySelector('.appointment-feedback') || form;

        // Collect form data
        const formData = new FormData(form);

        const originalBtnHtml = submitBtn ? submitBtn.innerHTML : '';
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fa fa-spinner fa-spin me-2"></i>Submitting...';
        }

        try {
            const response = await fetch(form.action || '/website_hospital/appointment/submit', {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json',
                },
                body: new URLSearchParams(formData),
            });

            const result = await response.json();

            let alertEl = form.querySelector('.appointment-alert');
            if (!alertEl) {
                alertEl = document.createElement('div');
                alertEl.className = 'appointment-alert mt-3 p-3 rounded text-center';
                feedbackArea.appendChild(alertEl);
            }

            if (result.status === 'success') {
                alertEl.className = 'appointment-alert mt-3 p-3 rounded text-center alert alert-success';
                alertEl.style.backgroundColor = '#E6F7F5';
                alertEl.style.color = '#0B4F6C';
                alertEl.style.border = '1px solid #00A896';
                alertEl.innerHTML = `<i class="fa fa-check-circle me-2 fs-5" style="color: #00A896;"></i> <strong>Confirmed!</strong> ${result.message}`;
                form.reset();
            } else {
                alertEl.className = 'appointment-alert mt-3 p-3 rounded text-center alert alert-danger';
                alertEl.innerHTML = `<i class="fa fa-exclamation-triangle me-2"></i> ${result.message || 'Please check your information and try again.'}`;
            }
        } catch (error) {
            console.error('Submission error:', error);
            let alertEl = form.querySelector('.appointment-alert');
            if (!alertEl) {
                alertEl = document.createElement('div');
                alertEl.className = 'appointment-alert mt-3 p-3 rounded text-center alert alert-danger';
                feedbackArea.appendChild(alertEl);
            }
            alertEl.innerHTML = '<i class="fa fa-exclamation-triangle me-2"></i> An unexpected network error occurred. Please call our 24/7 hotline.';
        } finally {
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnHtml;
            }
        }
    },
});
