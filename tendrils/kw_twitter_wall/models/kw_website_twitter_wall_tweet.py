# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class KwWebsiteTwitterTweet(models.Model):

    _name = 'kw_website_twitter_wall_tweet'
    _description = 'Website Twitter Wall'

    website_id = fields.Many2one('website', string='Website')
    screen_name = fields.Char(string='Screen Name')
    tweet = fields.Text(string='Tweets')

    # Twitter IDs are 64-bit unsigned ints, so we need to store them in
    # unlimited precision NUMERIC columns, which can be done with a
    # float field. Used digits=(0,0) to indicate unlimited.
    # Using VARCHAR would work too but would have sorting problems.
    tweet_id = fields.Float(string='Tweet ID', digits=(0, 0))  # Twitter