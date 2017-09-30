#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# JotForm API - Python Client
#
# copyright : 2013 Interlogy, LLC.
# link : http://www.jotform.com
# version : 1.0
# package : JotFormAPI

from urllib.parse import urljoin, urlparse
import requests
import json
import logging
import pathlib


logger = logging.getLogger('spam_application')
logger.setLevel(logging.DEBUG)


class JotformAPIClient(object):
    base_url = 'https://api.jotform.com/'
    api_version = 'v1'

    def __init__(self, api_key='', debug=False):
        self.api_key = api_key
        self.debug_mode = debug

    def log(self, message):
        if self.debug_mode:
            logger.debug(message)

    def fetch_url(self, url, params=None, method=None):
        versioned = urljoin(self.base_url, self.api_version)
        endpoint = str(pathlib.Path(url).with_suffix('.json'))
        url = urljoin(versioned, endpoint)

        self.log('fetching url ' + url)

        if params:
            self.log(params)

        headers = {
            'apiKey': self.api_key
        }

        resp = requests.request(method=method, url=url,
            headers=headers, params=params)

        json_response = resp.json()
        return json_response.get('content')

    @staticmethod
    def create_conditions(offset, limit, filters, order_by):

        kwargs = {
            'offset': offset,
            'limit': limit,
            'orderby': order_by
        }

        params = {k: v for k, v in kwargs.items() if k}

        if filters:
            params.update({'filter': json.dumps(filters)})

        return params

    @staticmethod
    def create_history_query(action, date, sort_by, start_date, end_date):
        kwargs = {
            'action': action,
            'date': date,
            'sort_by': sort_by,
            'startDate': start_date,
            'endDate': end_date
        }

        params = {k: v for k, v in kwargs.items() if k}

        return params

    def get_user(self):
        """Get user account details for a JotForm user.

        Returns:
            User account type, avatar URL, name, email, website URL and account limits.
        """

        return self.fetch_url('/user', method='GET')

    def get_usage(self):
        """Get number of form submissions received this month.

        Returns:
            Number of submissions, number of SSL form submissions, payment form submissions and upload space used by user.
        """

        return self.fetch_url('/user/usage', method='GET')

    def get_forms(self, offset=None, limit=None, filters=None, order_by=None):
        """Get a list of forms for this account

        Args:
            offset (string): Start of each result set for form list. (optional)
            limit (string): Number of results in each result set for form list. (optional)
            filters (array): Filters the query results to fetch a specific form range.(optional)
            order_by (string): Order results by a form field name. (optional)

        Returns:
            Basic details such as title of the form, when it was created, number of new and total submissions.
        """

        params = self.create_conditions(offset, limit, filters, order_by)

        return self.fetch_url('/user/forms', params, 'GET')

    def get_submissions(self, offset=None, limit=None, filters=None, order_by=None):
        """Get a list of submissions for this account.

        Args:
            offset (string): Start of each result set for form list. (optional)
            limit (string): Number of results in each result set for form list. (optional)
            filters (array): Filters the query results to fetch a specific form range.(optional)
            order_by (string): Order results by a form field name. (optional)

        Returns:
            Basic details such as title of the form, when it was created, number of new and total submissions.
        """

        params = self.create_conditions(offset, limit, filters, order_by)

        return self.fetch_url('/user/submissions', params, 'GET')

    def get_subusers(self):
        """Get a list of sub users for this account.

        Returns:
            List of forms and form folders with access privileges.
        """

        return self.fetch_url('/user/subusers', method='GET')

    def get_folders(self):
        """Get a list of form folders for this account.

        Returns:
            Name of the folder and owner of the folder for shared folders.
        """

        return self.fetch_url('/user/folders', method='GET')

    def get_reports(self):
        """List of URLS for reports in this account.

        Returns:
            Reports for all of the forms. ie. Excel, CSV, printable charts, embeddable HTML tables.
        """

        return self.fetch_url('/user/reports', method='GET')

    def get_settings(self):
        """Get user's settings for this account.

        Returns:
            User's time zone and language.
        """

        return self.fetch_url('/user/settings', method='GET')

    def update_settings(self, settings):
        """Update user's settings.

        Args:
            settings (array): New user setting values with setting keys

        Returns:
            Changes on user settings.
        """

        return self.fetch_url('/user/settings', settings, 'POST')

    def get_history(self, action=None, date=None, sort_by=None,
                    start_date=None, end_date=None):
        """Get user activity log.

        Args:
            action (enum): Filter results by activity performed. Default is 'all'.
            date (enum): Limit results by a date range. If you'd like to limit results by specific dates you can use startDate and endDate fields instead.
            sort_by (enum): Lists results by ascending and descending order.
            start_date (string): Limit results to only after a specific date. Format: MM/DD/YYYY.
            end_date (string): Limit results to only before a specific date. Format: MM/DD/YYYY.

        Returns:
            Activity log about things like forms created/modified/deleted, account logins and other operations.
        """

        params = self.create_history_query(action, date, sort_by, start_date, end_date)

        return self.fetch_url('/user/history', params, 'GET')

    def get_form(self, id):
        """Get basic information about a form.

        Args:
            id (string): Form ID is the numbers you see on a form URL. You can get form IDs when you call /user/forms.

        Returns:
            Form ID, status, update and creation dates, submission count etc.
        """

        return self.fetch_url('/form/' + id, method='GET')

    def get_form_questions(self, id):
        """Get a list of all questions on a form.

        Args:
            id (string): Form ID is the numbers you see on a form URL. You can get form IDs when you call /user/forms.

        Returns:
            Question properties of a form.
        """

        return self.fetch_url('/form/' + id + '/questions', method='GET')

    def get_form_question(self, id, qid):
        """Get details about a question

        Args:
            formID (string): Form ID is the numbers you see on a form URL. You can get form IDs when you call /user/forms.
            qid (string): Identifier for each question on a form. You can get a list of question IDs from /form/{id}/questions.

        Returns:
            Question properties like required and validation.
        """
        return self.fetch_url('/form/' + id + '/question/' + qid, method='GET')

    def get_form_submissions(self, id, offset=None, limit=None,
                             filters=None, order_by=None):
        """List of a form submissions.

        Args:
            id (string): Form ID is the numbers you see on a form URL. You can get form IDs when you call /user/forms.
            offset (string): Start of each result set for form list. (optional)
            limit (string): Number of results in each result set for form list. (optional)
            filters (array): Filters the query results to fetch a specific form range.(optional)
            order_by (string): Order results by a form field name. (optional)

        Returns:
            Submissions of a specific form.
        """

        params = self.create_conditions(offset, limit, filters, order_by)

        return self.fetch_url('/form/' + id + '/submissions', params, 'GET')

    def create_form_submission(self, id, submission):
        """Submit data to this form using the API.

        Args: id (string): Form ID is the numbers you see on a form URL. You
        can get form IDs when you call /user/forms. submission (array):
        Submission data with question IDs.

        Returns:
            Posted submission ID and URL.
        """

        sub = {}

        for key in submission:
            if "_" in key:
                sub['submission[' + key[0:key.find("_")] + '][' + key[key.find("_")+1:len(key)] + ']'] = submission[key]
            else:
                sub['submission[' + key + ']'] = submission[key]

        return self.fetch_url('/form/' + id + '/submissions', sub, 'POST')

    def create_form_submissions(self, id, submissions):
        """Submit data to this form using the API.

        Args:
            id (string): Form ID is the numbers you see on a form URL. You can get form IDs when you call /user/forms.
            submissions (json): Submission data with question IDs.

        Returns:
            Posted submission ID and URL.
        """

        return self.fetch_url('/form/' + id + '/submissions',
            submissions, 'PUT')

    def get_form_files(self, formID):
        """List of files uploaded on a form.

        Args:
            formID (string): Form ID is the numbers you see on a form URL. You can get form IDs when you call /user/forms.

        Returns:
            Uploaded file information and URLs on a specific form.
        """

        return self.fetch_url('/form/' + formID + '/files', method='GET')

    def get_form_webhooks(self, id):
        """Get list of webhooks for a form

        Args:
            id (string): Form ID is the numbers you see on a form URL. You can get form IDs when you call /user/forms.

        Returns:
            List of webhooks for a specific form.
        """

        return self.fetch_url('/form/' + id + '/webhooks', method='GET')

    def create_form_webhook(self, id, webhook_url):
        """Add a new webhook

        Args:
            id (string): Form ID is the numbers you see on a form URL. You can get form IDs when you call /user/forms.
            webhook_url (string): Webhook URL is where form data will be posted when form is submitted.

        Returns:
            List of webhooks for a specific form.
        """

        params = {'webhookURL': webhook_url}

        return self.fetch_url('/form/' + id + '/webhooks', params, 'POST')

    def delete_form_webhook(self, id, webhook_id):
        """Delete a specific webhook of a form.

        Args:
            id (string): Form ID is the numbers you see on a form URL. You can get form IDs when you call /user/forms.
            webhook_id (string): You can get webhook IDs when you call /form/{formID}/webhooks.

        Returns:
            Remaining webhook URLs of form.
        """

        return self.fetch_url('/form/' + id + '/webhooks/' + webhook_id, None, 'DELETE')

    def get_submission(self, sid):
        """Get submission data

        Args:
            sid (string): You can get submission IDs when you call /form/{id}/submissions.

        Returns:
            Information and answers of a specific submission.
        """

        return self.fetch_url('/submission/' + sid, method='GET')

    def get_report(self, report_id):
        """Get report details

        Args:
            report_id (string): You can get a list of reports from /user/reports.

        Returns:
            Properties of a speceific report like fields and status.
        """

        return self.fetch_url('/report/' + report_id, method='GET')

    def get_folder(self, folder_id):
        """Get folder details

        Args:
            folder_id (string): Get a list of folders from /user/folders

        Returns:
            A list of forms in a folder, and other details about the form such as folder color.
        """

        return self.fetch_url('/folder/' + folder_id, method='GET')

    def get_form_properties(self, form_id):
        """Get a list of all properties on a form.

        Args:
            form_id (string): Form ID is the numbers you see on a form URL. You can get form IDs when you call /user/forms.

        Returns:
            Form properties like width, expiration date, style etc.
        """

        return self.fetch_url('/form/' + form_id + '/properties', method='GET')

    def get_form_property(self, form_id, property_key):
        """Get a specific property of the form.

        Args:
            form_id (string): Form ID is the numbers you see on a form URL. You can get form IDs when you call /user/forms.
            property_key (string): You can get property keys when you call /form/{id}/properties.

        Returns:
            Given property key value.
        """

        return self.fetch_url(
            '/form/' + form_id + '/properties/' + property_key, method='GET'
        )

    def get_form_reports(self, form_id):
        """Get all the reports of a form, such as excel, csv, grid, html, etc.

        Args:
            form_id (string): Form ID is the numbers you see on a form URL. You can get form IDs when you call /user/forms.

        Returns:
            List of all reports in a form, and other details about the reports such as title.
        """

        return self.fetch_url('/form/' + form_id + '/reports', method='GET')

    def create_report(self, form_id, report):
        """Create new report of a form

        Args:
            form_id (string): Form ID is the numbers you see on a form URL. You can get form IDs when you call /user/forms.
            report (array): Report details. List type, title etc.

        Returns:
            Report details and URL
        """
        return self.fetch_url('/form/' + form_id + '/reports', report, 'POST')

    def delete_submission(self, sid):
        """Delete a single submission.

        Args:
            sid (string): You can get submission IDs when you call /form/{id}/submissions.

        Returns:
            Status of request.
        """

        return self.fetch_url('/submission/' + sid, None, 'DELETE')

    def edit_submission(self, sid, submission):
        """Edit a single submission.

        Args:
            sid (string): You can get submission IDs when you call /form/{id}/submissions.
            submission (array): New submission data with question IDs.

        Returns:
            Status of request.
        """

        sub = {}

        for key in submission:
            if '_' in key and key != "created_at":
                sub['submission[' + key[0:key.find('_')] + '][' + key[key.find('_')+1:len(key)] + ']'] = submission[key]
            else:
                sub['submission[' + key + ']'] = submission[key]

        return self.fetch_url('/submission/' + sid, sub, 'POST')

    def clone_form(self, form_id):
        """Clone a single form.

        Args:
            form_id (string): Form ID is the numbers you see on a form URL. You can get form IDs when you call /user/forms.

        Returns:
            Status of request.
        """
        params = {"method": "post"}

        return self.fetch_url('/form/' + form_id + '/clone', params, 'POST')

    def delete_form_question(self, form_id, qid):
        """Delete a single form question.

        Args:
            form_id (string): Form ID is the numbers you see on a form URL. You can get form IDs when you call /user/forms.
            qid (string): Identifier for each question on a form. You can get a list of question IDs from /form/{id}/questions.

        Returns:
            Status of request.
        """

        return self.fetch_url(
            '/form/' + form_id + '/question/' + qid, None, 'DELETE'
        )

    def create_form_question(self, form_id, question):
        """Add new question to specified form.

        Args:
            form_id (string): Form ID is the numbers you see on a form URL. You can get form IDs when you call /user/forms.
            question (array): New question properties like type and text.

        Returns:
            Properties of new question.
        """
        params = {}

        for key in question:
            params['question[' + key + ']'] = question[key]

        return self.fetch_url('/form/' + form_id + '/questions', params, 'POST')

    def create_form_questions(self, form_id, questions):
        """Add new questions to specified form.

        Args:
            form_id (string): Form ID is the numbers you see on a form URL. You can get form IDs when you call /user/forms.
            questions (json): New question properties like type and text.

        Returns:
            Properties of new question.
        """

        return self.fetch_url('/form/' + form_id + '/questions', questions, 'PUT')

    def edit_form_question(self, form_id, qid, question_properties):
        """Add or edit a single question properties.

        Args:
            form_id (string): Form ID is the numbers you see on a form URL. You can get form IDs when you call /user/forms.
            qid (string): Identifier for each question on a form. You can get a list of question IDs from /form/{id}/questions.
            question_properties (array): New question properties like type and text.

        Returns:
            Edited property and type of question.
        """
        question = {}

        for key in question_properties:
            question['question[' + key + ']'] = question_properties[key]

        return self.fetch_url('/form/' + form_id + '/question/' + qid, question, 'POST')

    def set_form_properties(self, form_id, form_properties):
        """Add or edit properties of a specific form

        Args:
            form_id (string): Form ID is the numbers you see on a form URL. You can get form IDs when you call /user/forms.
            form_properties (array): New properties like label width.

        Returns:
            Edited properties.
        """
        properties = {}

        for key in form_properties:
            properties['properties[' + key + ']'] = form_properties[key]

        return self.fetch_url('/form/' + form_id + '/properties', properties, 'POST')

    def set_multiple_form_properties(self, form_id, form_properties):
        """Add or edit properties of a specific form

        Args:
            form_id (string): Form ID is the numbers you see on a form URL. You can get form IDs when you call /user/forms.
            form_properties (json): New properties like label width.

        Returns:
            Edited properties.
        """

        return self.fetch_url('/form/' + form_id + '/properties', form_properties, 'PUT')

    def create_form(self, form):
        """ Create a new form

        Args:
            form (array): Questions, properties and emails of new form.

        Returns:
            New form.
        """

        params = {}

        for key in form:
            value = form[key]
            for k in value:
                if (key == 'properties'):
                    for k in value:
                        params[key + '[' + k + ']'] = value[k]
                else:
                    v = value[k]
                    for a in v:
                        params[key + '[' + k + '][' + a + ']'] =v[a]

        return self.fetch_url('/user/forms', params, 'POST')

    def create_forms(self, form):
        """ Create new forms

        Args:
            form (json): Questions, properties and emails of forms.

        Returns:
            New forms.
        """

        return self.fetch_url('/user/forms', form, 'PUT')

    def delete_form(self, form_id):
        """Delete a specific form

        Args:
            form_id (string): Form ID is the numbers you see on a form URL. You can get form IDs when you call /user/forms.

        Returns:
            Properties of deleted form.
        """

        return self.fetch_url('/form/' + form_id, None, 'DELETE')

    def register_user(self, userDetails):
        """Register with username, password and email

        Args:
            userDetails (array): Username, password and email to register a new user

        Returns:
            New user's details
        """

        return self.fetch_url('/user/register', userDetails, 'POST')

    def login_user(self, credentials):
        """Login user with given credentials

        Args:
            credentials (array): Username, password, application name and access type of user

        Returns:
            Logged in user's settings and app key
        """

        return self.fetch_url('/user/login', credentials, 'POST')

    def logout_user(self):
        """Logout user

        Returns:
            Status of request
        """

        return self.fetch_url('/user/logout', method='GET')

    def get_plan(self, plan_name):
        """Get details of a plan

        Args:
            plan_name (string): Name of the requested plan. FREE, PREMIUM etc.

        Returns:
            Details of a plan
        """

        return self.fetch_url('/system/plan/' + plan_name, method='GET')

    def delete_report(self, reportID):
        """Delete a specific report

        Args:
            reportID (string): You can get a list of reports from /user/reports.

        Returns:
            Status of request.
        """

        return self.fetch_url('/report/' + reportID, None, 'DELETE')
