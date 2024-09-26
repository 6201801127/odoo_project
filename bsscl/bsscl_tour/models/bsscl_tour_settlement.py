from odoo import models, fields, _, api
from odoo.exceptions import ValidationError

class TourSettlement(models.Model):
    _name = 'tour.settlement'
    _description = 'Tour Settlement'
    _rec_name = 'tour_id'

    @api.model
    def _get_domain(self):
        settlement_pending_tour_ids = self.env['tour.settlement'].search(
            [('create_uid', '=', self._uid), ('state', 'in',['2','3','4','5'])])
        # print('=====================',settlement_pending_tour_ids)
        tour_ids = settlement_pending_tour_ids.mapped(lambda x: x.tour_id)
        # print('=====================',tour_ids)
        return [('create_uid', '=', self._uid), ('id', 'not in', tour_ids.ids), ('state','=','completed')]

    tour_id = fields.Many2one(comodel_name="bsscl.tour", string="Tour", domain=_get_domain)
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee Name / कर्मचारी का नाम",)
    originating_place_id = fields.Many2one(comodel_name="res.country.state", string="Originating Place / उद्गम स्थल")
    date_of_travel = fields.Date(string="Date Of Travel / यात्रा की तिथि")
    return_date = fields.Date(string="Return Date / वापसी दिनांक")
    travel_arrangement = fields.Selection(string="Travel Arrangement / यात्रा व्यवस्था",
        selection=[('Self', 'Self / खुद'), ('Company', 'Company / कंपनी')], required=True,
        default="Company")
    purpose_of_travel = fields.Text(string="Purpose Of Travel / यात्रा का उद्देश्य")
    travel_expense_details_ids = fields.One2many(comodel_name="bsscl.tour.travel.expense.details",inverse_name="tour_settlement_id", string="Travel Expense / यात्रा खर्च")
    medical_exp_ids = fields.One2many(comodel_name="bsscl.medical.expense", inverse_name="settlement_id", string="Medical Expense / चिकित्सा खर्च")
    telephone_bill_exp_ids = fields.One2many(comodel_name="bsscl.telephone.expense", inverse_name="settlement_id")
    tour_details_ids = fields.One2many(comodel_name="bsscl.tour.details", inverse_name="settlement_id", string="Tour Details / भ्रमण विवरण")
    state = fields.Selection([('1','Draft'),('2','Applied'),('3','Approved'),('4','Grant'),('5','Payment Done'),('6','Canceled')], string="State")
    travel_booking_ids = fields.One2many(comodel_name="travel.booking", inverse_name="settlement_id" , string="Travel Booking Details")
    currency_id = fields.Many2one('res.currency', string="Currency", required=True,
                                  default=lambda self: self.env.user.company_id.currency_id.id,
                                  track_visibility='onchange')
    amount_total = fields.Float(string="Total Travel cost", compute="_compute_amount_total")
    medical_amount_total = fields.Float(string="Total Medical cost", compute="_compute_medical_amount_total")
    telephone_amount_total = fields.Float(string="Total Telephone bill cost", compute="_compute_telephone_bill_amount_total")
    advance_amount_total = fields.Float(string="Advance Claim Amount", compute="_compute_advance_Amount")
    travel_expense_ammount = fields.Float(string="Travel Expense Amount", compute="_compute_travel_expense_ammount")
    claim_ammount = fields.Float(string="Tour Claim Amount", compute="_compute_claim_amount_total")
        

    @api.depends('tour_id.advance_amount')
    def _compute_advance_Amount(self):
        for rec in self:
            rec.advance_amount_total = rec.tour_id.advance_amount

    @api.depends('travel_expense_details_ids.amount')
    def _compute_travel_expense_ammount(self):
        for rec in self:
            if rec.travel_expense_details_ids:
                total_sum = 0
                for record in rec.travel_expense_details_ids:
                    if record.amount:
                        total_sum += record.amount
                        rec.travel_expense_ammount = total_sum
                    else:
                        rec.travel_expense_ammount = 0.0
            else:
                rec.travel_expense_ammount = 0.0

    @api.depends('travel_booking_ids.travel_cost')
    def _compute_amount_total(self):
        for rec in self:
            if rec.travel_booking_ids:
                total_sum = 0
                for record in rec.travel_booking_ids:
                    if record.travel_cost:
                        total_sum += record.travel_cost
                        rec.amount_total = total_sum
                    else:
                        rec.amount_total = 0.0
            else:
                rec.amount_total = 0.0

    @api.depends('medical_exp_ids.amount')
    def _compute_medical_amount_total(self):
        for rec in self:
            if rec.medical_exp_ids:
                total_sum = 0
                for record in rec.medical_exp_ids:
                    if record.amount:
                        total_sum += record.amount
                        rec.medical_amount_total = total_sum
                    else:
                        rec.medical_amount_total = 0.0
            else:
                rec.medical_amount_total = 0.0

    @api.depends('telephone_bill_exp_ids.amount')
    def _compute_telephone_bill_amount_total(self):
        for rec in self:
            if rec.telephone_bill_exp_ids:
                total_sum = 0
                for record in rec.telephone_bill_exp_ids:
                    if record.amount:
                        total_sum += record.amount
                        rec.telephone_amount_total = total_sum
                    else:
                        rec.telephone_amount_total = 0.0
            else:
                rec.telephone_amount_total = 0.0

    @api.depends('amount_total','medical_amount_total','telephone_amount_total','advance_amount_total')
    def _compute_claim_amount_total(self):
        for rec in self:
            rec.claim_ammount = (rec.amount_total + rec.medical_amount_total + rec.telephone_amount_total) - rec.advance_amount_total
        
    @api.onchange('tour_id')
    def _onchange_tour_id(self):
        for rec in self:
            if rec.tour_id:
                rec.employee_id = rec.tour_id.employee_id
                rec.originating_place_id = rec.tour_id.originating_place_id
                rec.date_of_travel = rec.tour_id.date_of_travel
                rec.return_date = rec.tour_id.return_date
                rec.travel_arrangement = rec.tour_id.travel_arrangement
                rec.purpose_of_travel = rec.tour_id.purpose_of_travel
                if rec.tour_id.travel_expense_details_ids.tour_id == rec.tour_id:
                    rec.travel_expense_details_ids = rec.tour_id.travel_expense_details_ids
                    rec.tour_details_ids = rec.tour_id.tour_details_ids
                    rec.medical_exp_ids = rec.tour_id.medical_exp_ids
                    rec.telephone_bill_exp_ids = rec.tour_id.telephone_bill_exp_ids
            else:
                return False
            
    @api.model
    def create(self,vals):
        res =super(TourSettlement, self).create(vals)
        res.state = '1'
        return res

    def apply_tour_settlement(self):
        for rec in self:
            rec.state = '2'

    def approved_tour_settlement(self):
        for rec in self:
            if not rec.travel_booking_ids:
                raise ValidationError("Booking details missing please provide travel booking details before settlement approved.")
            rec.tour_id.travel_booking_ids = rec.travel_booking_ids
            rec.tour_id.medical_exp_ids = rec.medical_exp_ids
            rec.tour_id.telephone_bill_exp_ids = rec.telephone_bill_exp_ids
            rec.tour_id.amount_total = rec.amount_total
            rec.tour_id.medical_amount_total = rec.medical_amount_total
            rec.tour_id.telephone_amount_total = rec.telephone_amount_total
            rec.tour_id.advance_amount_total = rec.advance_amount_total
            rec.tour_id.travel_expense_ammount = rec.travel_expense_ammount
            rec.tour_id.claim_ammount = rec.claim_ammount
            rec.state = '3'
    
    def grant_tour_settlement(self):
        for rec in self:
            rec.state = '4'

    def payment_done_tour_settlement(self):
        for rec in self:
            rec.state = '5'

    def settlement_cancel(self):
        for rec in self:
            rec.state = '6'