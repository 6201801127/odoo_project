import copy
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.osv import expression
from odoo.tools import pycompat
from odoo.tools.misc import formatLang
from odoo.tools import misc

class AccountReconciliationInherit(models.AbstractModel):
    _inherit = 'account.reconciliation.widget'

    @api.model
    def _domain_move_lines_for_manual_reconciliation(self, account_id, partner_id=False, excluded_ids=None, search_str=False):
        """ Create domain criteria that are relevant to manual reconciliation. """
        domain = [
            '&',
                '&',
                    ('reconciled', '=', False),
                    ('account_id', '=', account_id),
                '|',
                    ('move_id.state', '=', 'posted'),
                    '&',
                        ('move_id.state', '=', 'draft'),
                        ('move_id.journal_id.post_at_bank_rec', '=', True),
            ]
        domain = expression.AND([domain, [('balance', '!=', 0.0)]])
        if partner_id:
            domain = expression.AND([domain, [('partner_id', '=', partner_id)]])
        if excluded_ids:
            domain = expression.AND([[('id', 'not in', excluded_ids)], domain])
        if search_str:
            str_domain = self._domain_move_lines(search_str=search_str)
            str_domain = expression.OR([
                str_domain,
                [('partner_id.name', 'ilike', search_str)]
            ])
            domain = expression.AND([domain, str_domain])
        # filter on account.move.line having the same company as the given account
        account = self.env['account.account'].browse(account_id)
        domain = expression.AND([domain, [('company_id', '=', account.company_id.id),('account_id.internal_type','=','payable')]])
        return domain

    @api.model
    def _prepare_move_lines(self, move_lines, target_currency=False, target_date=False, recs_count=0):
        """ Returns move lines formatted for the manual/bank reconciliation widget

            :param move_line_ids:
            :param target_currency: currency (browse) you want the move line debit/credit converted into
            :param target_date: date to use for the monetary conversion
        """
        context = dict(self._context or {})
        ret = []

        for line in move_lines:
            company_currency = line.company_id.currency_id
            line_currency = (line.currency_id and line.amount_currency) and line.currency_id or company_currency
            date_maturity = misc.format_date(self.env, line.date_maturity, lang_code=self.env.user.lang)
            if line.account_id.internal_type == 'payable':
                ret_line = {
                    'id': line.id,
                    'name': line.name and line.name != '/' and line.move_id.name + ': ' + line.name or line.move_id.name,
                    'ref': line.move_id.ref or '',
                    # For reconciliation between statement transactions and already registered payments (eg. checks)
                    # NB : we don't use the 'reconciled' field because the line we're selecting is not the one that gets reconciled
                    'account_id': [line.account_id.id, line.account_id.display_name],
                    'already_paid': line.account_id.internal_type == 'liquidity',
                    'account_code': line.account_id.code,
                    'account_name': line.account_id.name,
                    'account_type': line.account_id.internal_type,
                    'date_maturity': date_maturity,
                    'date': line.date,
                    'journal_id': [line.journal_id.id, line.journal_id.display_name],
                    'partner_id': line.partner_id.id,
                    'partner_name': line.partner_id.name,
                    'currency_id': line_currency.id,
                }

                debit = line.debit
                credit = line.credit
                amount = line.amount_residual
                amount_currency = line.amount_residual_currency

                # For already reconciled lines, don't use amount_residual(_currency)
                if line.account_id.internal_type == 'liquidity':
                    amount = debit - credit
                    amount_currency = line.amount_currency

                target_currency = target_currency or company_currency

                # Use case:
                # Let's assume that company currency is in USD and that we have the 3 following move lines
                #      Debit  Credit  Amount currency  Currency
                # 1)    25      0            0            NULL
                # 2)    17      0           25             EUR
                # 3)    33      0           25             YEN
                #
                # If we ask to see the information in the reconciliation widget in company currency, we want to see
                # The following information
                # 1) 25 USD (no currency information)
                # 2) 17 USD [25 EUR] (show 25 euro in currency information, in the little bill)
                # 3) 33 USD [25 YEN] (show 25 yen in currency information)
                #
                # If we ask to see the information in another currency than the company let's say EUR
                # 1) 35 EUR [25 USD]
                # 2) 25 EUR (no currency information)
                # 3) 50 EUR [25 YEN]
                # In that case, we have to convert the debit-credit to the currency we want and we show next to it
                # the value of the amount_currency or the debit-credit if no amount currency
                if target_currency == company_currency:
                    if line_currency == target_currency:
                        amount = amount
                        amount_currency = ""
                        total_amount = debit - credit
                        total_amount_currency = ""
                    else:
                        amount = amount
                        amount_currency = amount_currency
                        total_amount = debit - credit
                        total_amount_currency = line.amount_currency

                if target_currency != company_currency:
                    if line_currency == target_currency:
                        amount = amount_currency
                        amount_currency = ""
                        total_amount = line.amount_currency
                        total_amount_currency = ""
                    else:
                        amount_currency = line.currency_id and amount_currency or amount
                        company = line.account_id.company_id
                        date = target_date or line.date
                        amount = company_currency._convert(amount, target_currency, company, date)
                        total_amount = company_currency._convert((line.debit - line.credit), target_currency, company, date)
                        total_amount_currency = line.currency_id and line.amount_currency or (line.debit - line.credit)

                ret_line['recs_count'] = recs_count
                ret_line['debit'] = amount > 0 and amount or 0
                ret_line['credit'] = amount < 0 and -amount or 0
                ret_line['amount_currency'] = amount_currency
                ret_line['amount_str'] = formatLang(self.env, abs(amount), currency_obj=target_currency)
                ret_line['total_amount_str'] = formatLang(self.env, abs(total_amount), currency_obj=target_currency)
                ret_line['amount_currency_str'] = amount_currency and formatLang(self.env, abs(amount_currency), currency_obj=line_currency) or ""
                ret_line['total_amount_currency_str'] = total_amount_currency and formatLang(self.env, abs(total_amount_currency), currency_obj=line_currency) or ""
                ret.append(ret_line)
        return ret