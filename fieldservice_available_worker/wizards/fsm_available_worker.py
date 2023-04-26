# Copyright 2023 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class FsmAvailableWorker(models.TransientModel):
    _name = "fsm.available.worker"

    skill_ids = fields.Many2many("hr.skill", string="Required Skills")
    category_ids = fields.Many2many("fsm.category", string="Categories")
    calendar_id = fields.Many2one("resource.calendar", string="Working Schedules")
    territory_id = fields.Many2one("fsm.territory", string="Territory")
    start_datetime = fields.Datetime("Start Date")
    stop_datetime = fields.Datetime("Stop Date")

    def _get_available_workers(
        self,
        territory_id=None,
        calendar_id=None,
        skill_ids=None,
        category_ids=None,
        start_datetime=None,
        stop_datetime=None,
    ):
        domain = []
        if territory_id:
            domain.append(("territory_ids", "in", territory_id.id))
        if calendar_id:
            domain.append(("calendar_id", "=", calendar_id.id))
        available_workers = self.env["fsm.person"].search(domain)

        if skill_ids:
            for skill in skill_ids:
                available_workers = available_workers.filtered(
                    lambda r: any(s.skill_id == skill for s in r.skill_ids)
                )

        if category_ids:
            for category in category_ids:
                available_workers = available_workers.filtered(
                    lambda r: category in r.category_ids
                )

        fsm_order_domain = [
            "|",
            "&",
            ("scheduled_date_start", ">=", start_datetime),
            ("scheduled_date_start", "<=", stop_datetime),
            "|",
            "&",
            ("scheduled_date_end", ">=", start_datetime),
            ("scheduled_date_end", "<=", stop_datetime),
            "&",
            ("scheduled_date_start", "<=", start_datetime),
            ("scheduled_date_end", ">=", stop_datetime),
        ]

        fsm_orders = self.env["fsm.order"].search(fsm_order_domain)
        if fsm_orders:
            person_ids = fsm_orders.mapped("person_id")
            available_workers = available_workers.filtered(
                lambda r: r.id not in person_ids.ids
            )

        return available_workers

    @api.multi
    def doit(self):
        self.ensure_one()
        available_workers = self._get_available_workers(
            territory_id=self.territory_id,
            calendar_id=self.calendar_id,
            skill_ids=self.skill_ids,
            category_ids=self.category_ids,
            start_datetime=self.start_datetime,
            stop_datetime=self.stop_datetime,
        )

        action = {
            "type": "ir.actions.act_window",
            "name": _("Available Workers"),
            "res_model": "fsm.person",
            "domain": [("id", "in", available_workers.ids)],
            "view_mode": "tree,form",
            "context": self.env.context,
        }
        return action
