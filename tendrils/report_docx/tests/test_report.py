# Copyright 2017 Creu Blanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common
import logging
_logger = logging.getLogger(__name__)

try:
    from xlrd import open_workbook
except ImportError:
    _logger.debug('Can not import xlrd`.')


class TestReport(common.TransactionCase):
    def setUp(self):
        super(TestReport, self).setUp()
        report_object = self.env['ir.actions.report']
        self.docx_report = (
            self.env['report.report_docx.abstract']
            .with_context(active_model='res.partner')
        )
        self.report_name = 'report_docx.partner_docx'
        self.report = report_object._get_report_from_name(self.report_name)
        self.docs = self.env['res.company'].search([], limit=1).partner_id

    def test_report(self):
        report = self.report
        self.assertEqual(report.report_type, 'docx')
        rep = report.render(self.docs.ids, {})
        wb = open_workbook(file_contents=rep[0])
        sheet = wb.sheet_by_index(0)
        self.assertEqual(sheet.cell(0, 0).value, self.docs.name)

    def test_id_retrieval(self):

        # Typical call from WebUI with wizard
        objs = self.docx_report._get_objs_for_report(
            False, {"context": {"active_ids": self.docs.ids}})
        self.assertEquals(objs, self.docs)

        # Typical call from within code not to report_action
        objs = self.docx_report.with_context(
            active_ids=self.docs.ids)._get_objs_for_report(False, False)
        self.assertEquals(objs, self.docs)

        # Typical call from WebUI
        objs = self.docx_report._get_objs_for_report(
            self.docs.ids,
            {"data": [self.report_name, self.report.report_type]}
        )
        self.assertEquals(objs, self.docs)

        # Typical call from render
        objs = self.docx_report._get_objs_for_report(self.docs.ids, {})
        self.assertEquals(objs, self.docs)
