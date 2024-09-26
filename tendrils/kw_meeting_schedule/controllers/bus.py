# -*- coding: utf-8 -*

from odoo.addons.bus.controllers.main import BusController
from odoo.http import request


class KwMeetingScheduleBusController(BusController):
    # --------------------------
    # Extends BUS Controller Poll
    # --------------------------
    def _poll(self, dbname, channels, last, options):
        if request.session.uid:
            channels = list(channels)
            channels.append((request.db, 'kw_meeting_events', request.env.user.partner_id.id))
        return super(KwMeetingScheduleBusController, self)._poll(dbname, channels, last, options)
