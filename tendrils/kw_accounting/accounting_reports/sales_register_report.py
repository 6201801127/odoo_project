from odoo import models, fields, api,tools
from odoo.addons.kw_accounting.models.chart_of_accounts import state_list

class SalesRegisterReport(models.Model):
    _name = "sales.register.report"
    _description = "Sales Register Report"
    _auto = False

    slno = fields.Integer(string="Sl#")
    transaction_date = fields.Date(string="Transaction Date")
    invoice_date = fields.Date(string="Invoice Date")
    voucher_number = fields.Char(string="Voucher No")
    invoice_number = fields.Char(string="Invoice Number")
    partner_id = fields.Many2one('res.partner',string="Recipient")
    partner_name = fields.Char(related='partner_id.name',string="Recipient")
    partner_gstin = fields.Char(string="GSTIN")
    invoice_id = fields.Many2one('account.invoice',string="Invoice")
    particulars = fields.Char(string="Particulars",related="invoice_id.particulars")
    partner_state = fields.Many2one('res.country.state',string="State")
    partner_country = fields.Many2one('res.country',string="Country")
    item = fields.Many2one('product.product',string="Item/Service")
    narration = fields.Text(string="Narration")
    product_category = fields.Selection([('product','Goods'),('service','Service')],string="Goods/Service")
    hsn_code = fields.Char(string="HSN/SAC")
    taxable_amount = fields.Float(string="Taxable Value")
    igst_rate = fields.Float(string="%")
    igst_amount = fields.Float(string="IGST")
    cgst_rate = fields.Float(string="%")
    cgst_amount = fields.Float(string="CGST")
    sgst_rate = fields.Float(string="%")
    sgst_amount = fields.Float(string="SGST")
    invoice_amount = fields.Float(string="Invoice Amount")
    branch_id = fields.Many2one('accounting.branch.unit','Branch')
    type = fields.Selection([('out_invoice','Sales'),('out_refund','Credit Note')],string="Type")
    sbu_id = fields.Selection(state_list,string="State")
    current_financial_year = fields.Boolean("Current Financial Year",compute='_compute_current_financial_year',search="_register_search_current_financial_year")


    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        query = f""" CREATE or REPLACE VIEW {self._table} as (
            select 
            row_number() over(order by ai.id desc) as id,
            row_number() over() as slno,
            ai.date as transaction_date,
            ai.date_invoice as invoice_date,
            ai.id as invoice_id,
            ai.move_name as voucher_number,
            ai.reference_number as invoice_number,
            ai.partner_id as partner_id,
            rp.vat as partner_gstin,
            rp.state_id as partner_state,
            rp.country_id as partner_country,
            apl.product_id as item,
            ai.comment as narration,
            apl.product_category as product_category,
            apl.hsn_code as hsn_code,
            (apl.price_unit) as taxable_amount,
            apl.igst_per::double precision as igst_rate,
            (apl.igst_amount) as igst_amount,
            apl.cgst_per::double precision as cgst_rate,
            (apl.cgst_amount) as cgst_amount,
            apl.sgst_per::double precision as sgst_rate,
            (apl.sgst_amount) as sgst_amount,
            apl.amount as invoice_amount,
            sg.state_name as sbu_id,
            
            ai.unit_id as branch_id,
            ai.type as type
            

            from account_product_line apl
            left join account_invoice ai on ai.id = apl.invoice_id
            left join account_account aa on aa.id = ai.account_id
            left join res_partner rp on rp.id = apl.partner_id
			left join state_gstin sg on sg.id = ai.state_gstin_id

            where ai.type in ('out_invoice', 'out_refund') and ai.state != 'draft'
        )"""
        self.env.cr.execute(query)

    @api.multi
    def _compute_current_financial_year(self):
        for record in self:
            pass
        
    @api.multi
    def _register_search_current_financial_year(self, operator, value):
        start_date , end_date = self.env['hr.leave'].lv_get_current_financial_dates()
        domain = [('transaction_date', '>=', start_date),('transaction_date', '<=', end_date)]
        return domain