from odoo import models, api, fields, tools

class DepartmentWiseCapitalReport(models.Model):
    _name = "department_wise_capital_report"
    _description = "Departement wise Capital Report"
    _auto = False
    _order = "department_id asc"

    # name_of_expenses = fields.Char(string='Name of Expenses')
    account_id = fields.Many2one('account.account', 'Account Code')
    # account_code_id = fields.Many2one('account.account', 'Account Code')
    sequence_ref = fields.Char(string='ID')
    account_code = fields.Char(related='account_id.code', string='Account code')
    account_name = fields.Char(related='account_id.name', string='Account Name')
    merged_expenses_remark = fields.Char(string='Name of Expenses')
    # remark = fields.Char(string='Remark')
    # expense_type = fields.Char(string='Expense Type')
    budget_line =  fields.Many2one('kw_capital_budget_line', string="Budget Line")
    budget_department=fields.Many2one('kw_budget_dept_mapping', string="Budget Departement")
    fiscal_year_id = fields.Many2one('account.fiscalyear', string="Fiscal Year")
    department_id = fields.Many2one('hr.department', string="Department")
    division_id = fields.Many2one('hr.department', string="Division")
    section_id = fields.Many2one('hr.department', string="Section")
    april_budget = fields.Float('Apr Budget')
    may_budget = fields.Float('May Budget')
    june_budget = fields.Float('Jun Budget')
    july_budget = fields.Float('Jul Budget')
    august_budget = fields.Float('Aug Budget')
    september_budget = fields.Float('Sep Budget')
    october_budget = fields.Float('Oct Budget')
    november_budget = fields.Float('Nov Budget')
    december_budget = fields.Float('Dec Budget')
    january_budget = fields.Float('Jan Budget')
    february_budget = fields.Float('Feb Budget')
    march_budget = fields.Float('Mar Budget')
    next_fy_budget = fields.Float('Next Fy Budget')
    april_actual = fields.Float('Apr Actual', compute='_compute_actual_amount')
    may_actual = fields.Float('May Actual', compute='_compute_actual_amount')
    june_actual = fields.Float('Jun Actual', compute='_compute_actual_amount')
    july_actual = fields.Float('Jul Actual', compute='_compute_actual_amount')
    august_actual = fields.Float('Aug Actual', compute='_compute_actual_amount')
    september_actual = fields.Float('Sep Actual', compute='_compute_actual_amount')
    october_actual = fields.Float('Oct Actual', compute='_compute_actual_amount')
    november_actual = fields.Float('Nov Actual', compute='_compute_actual_amount')
    december_actual = fields.Float('Dec Actual', compute='_compute_actual_amount')
    january_actual = fields.Float('Jan Actual', compute='_compute_actual_amount')
    february_actual = fields.Float('Feb Actual', compute='_compute_actual_amount')
    march_actual = fields.Float('Mar Actual', compute='_compute_actual_amount')
    total_budget = fields.Float('Total Budget Amount' )
    actual_amount = fields.Float('Actual Amount', compute="_compute_practical_amount")
  

    @api.multi
    def _compute_actual_amount(self):
        for line in self:
            date_to = line.fiscal_year_id.date_stop
            date_from = line.fiscal_year_id.date_start
            aml_obj = self.env['account.move.line']
            domain = [('account_id', '=', line.account_id.id),
                    # ('capital_line', '=', line.budget_line.id),
                    ('capital_line', '=', line.budget_line and line.budget_line.id or False),
                      ('date', '>=', date_from),
                      ('date', '<=', date_to),
                        ('move_id.state', '=', 'posted'),
                         ('budget_type','=','capital'),
                          ('budget_update','=',True),
                      ]
            if not line.department_id and not line.section_id and not line.division_id:
                domain.extend([('department_id', '=', False),
                           ('section_id', '=', False),
                           ('division_id', '=', False)])
            else:
                if line.section_id:
                    domain.append(('section_id', '=', line.section_id.id))
                elif line.division_id:
                    domain.append(('division_id', '=', line.division_id.id))
                elif line.department_id:
                    domain.append(('department_id', '=', line.department_id.id))
                    domain.append(('section_id', '=', False))
                    domain.append(('division_id', '=', False))
            where_query = aml_obj._where_calc(domain)
            aml_obj._apply_ir_rules(where_query, 'read')
            from_clause, where_clause, where_clause_params = where_query.get_sql()

            month_conditions = [
                f"extract('month' from {aml_obj._table}.date) = {month}"
                for month in range(1, 13)
            ]
            where_clause += f" AND ({' OR '.join(month_conditions)})"
            
            if line.sudo().account_id.group_type.code == '3':
                select = "SELECT extract('month' from account_move_line.date) as month, sum(account_move_line.credit)-sum(account_move_line.debit) as balance " \
                         "from " + from_clause + "left join account_move am on am.id = account_move_line.move_id and am.state = 'posted'" + "where " + where_clause + " GROUP BY month"
            else:
                select = "SELECT extract('month' from account_move_line.date) as month, sum(account_move_line.debit)-sum(account_move_line.credit) as balance " \
                         "from " + from_clause +" left join account_move am on am.id = account_move_line.move_id and am.state = 'posted'"+" where " + where_clause + " GROUP BY month"

            self.env.cr.execute(select, where_clause_params)
            month_balances = dict(self.env.cr.fetchall())

            for month in range(1, 13):
                month_field = self._month_number_to_field_name(month)
                setattr(line, month_field, month_balances.get(month, 0.0))

    def _month_number_to_field_name(self, month):
        month_map = {4: 'april_actual',5: 'may_actual',6: 'june_actual',7: 'july_actual',8: 'august_actual',9: 'september_actual',10: 'october_actual',11: 'november_actual',12: 'december_actual',1: 'january_actual',2: 'february_actual',3: 'march_actual',}
        return month_map.get(month, 'january_actual')

    @api.multi
    def _compute_practical_amount(self):
        for line in self:
            # acc_ids = line.budgetary_position_id.account_ids.ids
            date_to = line.fiscal_year_id.date_stop
            date_from = line.fiscal_year_id.date_start
            aml_obj = self.env['account.move.line']
            domain = [('account_id', '=', line.account_id.id),
                ('capital_line', '=', line.budget_line and line.budget_line.id or False),
                        ('date', '>=', date_from),
                        ('date', '<=', date_to),
                        ('move_id.state', '=', 'posted'),
                        ('budget_type','=','capital'),
                         ('budget_update','=',True),
                      ]
            if not line.department_id and not line.section_id and not line.division_id:
                domain.extend([('department_id', '=', False),
                           ('section_id', '=', False),
                           ('division_id', '=', False)])
            else:
                if line.section_id:
                    domain.append(('section_id', '=', line.section_id.id))
                elif line.division_id:
                    domain.append(('division_id', '=', line.division_id.id))
                elif line.department_id:
                    domain.append(('department_id', '=', line.department_id.id))
                    domain.append(('section_id', '=', False))
                    domain.append(('division_id', '=', False))
            where_query = aml_obj._where_calc(domain)
            aml_obj._apply_ir_rules(where_query, 'read')
            from_clause, where_clause, where_clause_params = where_query.get_sql()
            
            if line.sudo().account_id.group_type.code == '3':
                select = "SELECT sum(account_move_line.credit)-sum(account_move_line.debit) from" + from_clause + "left join account_move am on am.id = account_move_line.move_id and am.state = 'posted'"+"where" + where_clause
            else:
                select = "SELECT sum(account_move_line.debit)-sum(account_move_line.credit) from" + from_clause + "left join account_move am on am.id = account_move_line.move_id and am.state = 'posted'"+" where " + where_clause
            self.env.cr.execute(select, where_clause_params)
            line.actual_amount = self.env.cr.fetchone()[0] or 0.0
          

    def action_open_budget_entries(self):
        action = self.env['ir.actions.act_window'].for_xml_id('account', 'action_account_moves_all_a')
        domain = [('account_id', '=', self.account_id.id),
                    ('capital_line', '=', self.budget_line and self.budget_line.id or False),
                            ('date', '>=', self.fiscal_year_id.date_start),
                            ('date', '<=', self.fiscal_year_id.date_stop),
                            ('move_id.state', '=', 'posted'),
                             ('budget_type','=','capital'),
                              ('budget_update','=',True),
                            ]
        if not self.department_id and not self.section_id and not self.division_id:
            domain.extend([('department_id', '=', False),
                           ('section_id', '=', False),
                           ('division_id', '=', False)])
        else:
            if self.section_id:
                domain.append(('section_id', '=', self.section_id.id))
            elif self.division_id:
                domain.append(('division_id', '=', self.division_id.id))
            elif self.department_id:
                domain.append(('department_id', '=', self.department_id.id))
                domain.append(('section_id', '=', False))
                domain.append(('division_id', '=', False))
        action['domain'] = domain
        return action

        
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        if self._context.get('report_action_approved_capital_budget'):
            data = self.env['kw_budget_dept_mapping'].sudo().search(['|',('level_2_approver','in',[self.env.user.employee_ids.id]),('level_1_approver','in',[self.env.user.employee_ids.id])])
            # print(data, '============>>>')
            if self.env.user.has_group('kw_budget.group_finance_kw_budget') or self.env.user.has_group('kw_budget.group_approver_kw_budget') or self.env.user.has_group('kw_budget.group_manager_kw_budget'):
                args += []
            elif self.env.user.has_group('kw_budget.group_manager_report'):
                args += []
            elif self.env.user.has_group('kw_budget.group_department_head_kw_budget'):
                args += [('budget_department', 'in', data.ids)]
        return super(DepartmentWiseCapitalReport, self)._search(args, offset=offset, limit=limit, order=order, count=count,
                                                            access_rights_uid=access_rights_uid)


    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(f""" CREATE or REPLACE VIEW %s as (
                with final as (With final_cte as (WITH a AS (
    SELECT 
        af.id AS fiscal_year_id,
        aa.id AS account_id
    FROM 
        account_account aa
    CROSS JOIN 
        account_fiscalyear af 
),
b as (
	 SELECT 
        aml.account_id,
		aml.capital_line,
        aml.fiscalyear_id,
		aml.department_id,
		aml.division_id,
		aml.section_id,
       aml.balance AS total_balance
    FROM 
        account_move_line aml
    JOIN 
        account_move am ON am.id = aml.move_id and aml.budget_type = 'capital'
    WHERE 
        am.state = 'posted' 
)
select 

		null::char as sequence_ref,
		null::char as merged_expenses_remark,
		b.capital_line as budget_line,
		a.account_id as account_id,
        (SELECT pb.id AS budget_department FROM kw_budget_dept_mapping pb LEFT JOIN account_move_line s 
		ON s.department_id = pb.department_id
		WHERE s.department_id = b.department_id  limit 1) as budget_department,  
		a.fiscal_year_id as fiscal_year_id,
	  	b.department_id,
		b.division_id,
		b.section_id,
		0 AS april_budget, 
        0 AS may_budget,
        0 AS june_budget,
        0 AS july_budget,
        0 AS august_budget,
        0 AS september_budget,
        0 AS october_budget,
        0 AS november_budget,
        0 AS december_budget,
        0 AS january_budget,
        0 AS february_budget,
        0 AS march_budget,
        0 AS next_fy_budget,
		0 as total_budget,
		b.total_balance 
		from a left join b on a.account_id = b.account_id and a.fiscal_year_id = b.fiscalyear_id
		where b.total_balance IS NOT NULL
	
 union all

			   SELECT 
                a.sequence_ref as sequence_ref,
                CONCAT(a.name_of_expenses, ' ; ', a.remark) as merged_expenses_remark,
				a.id as budget_line,
                a.account_code_id as account_id,
                b.budget_department,
				b.fiscal_year_id AS fiscal_year_id,
				(SELECT department_id FROM kw_budget_dept_mapping WHERE id = b.budget_department) AS department_id,
				(SELECT division_id FROM kw_budget_dept_mapping WHERE id = b.budget_department) AS division_id,
        		(SELECT section_id FROM kw_budget_dept_mapping WHERE id = b.budget_department) AS section_id,
				a.apr_budget AS april_budget, 
				a.may_budget AS may_budget,
				a.jun_budget AS june_budget,
				a.jul_budget AS july_budget,
				a.aug_budget AS august_budget,
				a.sep_budget AS september_budget,
				a.oct_budget AS october_budget,
				a.nov_budget AS november_budget,
				a.dec_budget AS december_budget,
				a.jan_budget AS january_budget,
				a.feb_budget AS february_budget,
				a.mar_budget AS march_budget,
                a.next_fy_year AS next_fy_budget,
				(COALESCE(a.apr_budget, 0) + COALESCE(a.may_budget, 0) + COALESCE(a.jun_budget, 0) + COALESCE(a.jul_budget, 0) + 
                COALESCE(a.aug_budget, 0) + COALESCE(a.sep_budget, 0) + COALESCE(a.oct_budget, 0) + COALESCE(a.nov_budget, 0) + 
                COALESCE(a.dec_budget, 0) + COALESCE(a.jan_budget, 0) + COALESCE(a.feb_budget, 0) + COALESCE(a.mar_budget, 0)+ COALESCE(a.next_fy_year, 0)) AS total_budget,
				0 as total_balance
			FROM 
				kw_capital_budget b
			LEFT JOIN 
				kw_capital_budget_line a ON a.capital_budget_id = b.id
			WHERE 
				a.account_code_id IS NOT NULL and b.state = 'validate'
			GROUP BY 
				b.fiscal_year_id, b.budget_department,a.name_of_expenses,a.id 			
	)
	SELECT 		
        COALESCE(NULLIF(TRIM(max(sequence_ref)), ''), 'NA') AS sequence_ref,
		max(merged_expenses_remark) merged_expenses_remark,
		budget_line,
		account_id,
		max(budget_department) budget_department ,
		fiscal_year_id, 
		department_id,
		division_id,
		section_id,
		SUM(april_budget) as april_budget, 
        SUM(may_budget) AS may_budget,
        SUM(june_budget) AS june_budget,
        SUM(july_budget) AS july_budget,
        SUM(august_budget) AS august_budget,
        SUM(september_budget) AS september_budget,
        SUM(october_budget) AS october_budget,
        SUM(november_budget) AS november_budget,
        SUM(december_budget) AS december_budget,
        SUM(january_budget) AS january_budget,
        SUM(february_budget) AS february_budget,
        SUM(march_budget) AS march_budget,
        SUM(next_fy_budget) AS next_fy_budget,
		sum(total_budget) as total_budget,
		sum(total_balance) as balance
	    FROM  final_cte
        group by 
        final_cte.fiscal_year_id,
        final_cte.account_id,
		final_cte.budget_line,
        final_cte.department_id,
        final_cte.division_id,
        final_cte.section_id)
		select ROW_NUMBER() OVER(order by account_id desc,fiscal_year_id desc) AS id,
		* from final
        
        )""" % (self._table))

           