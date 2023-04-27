from datetime import datetime, timedelta

from odoo.tests.common import TransactionCase


class TestFsmAvailableWorker(TransactionCase):
    def setUp(self):
        super(TestFsmAvailableWorker, self).setUp()

        self.category_1 = self.env["fsm.category"].create(
            {
                "name": "Test Category",
            }
        )
        self.fsm_person_1 = self.env["fsm.person"].create(
            {
                "name": "Test Worker 1",
                "category_ids": [(6, 0, [self.category_1.id])],
            }
        )

        self.fsm_person_2 = self.env["fsm.person"].create(
            {
                "name": "Test Worker 2",
                "category_ids": [(6, 0, [self.category_1.id])],
            }
        )

        self.fsm_location_1 = self.env.ref("fieldservice.test_location")

        self.start_datetime = datetime.now()
        self.stop_datetime = self.start_datetime + timedelta(days=5)

        self.fsm_order_1 = self.env["fsm.order"].create(
            {
                "name": "Order 1",
                "person_id": self.fsm_person_1.id,
                "scheduled_date_start": self.start_datetime - timedelta(days=1),
                "scheduled_date_end": self.stop_datetime - timedelta(days=1),
                "location_id": self.fsm_location_1.id,
            }
        )

        self.fsm_order_2 = self.env["fsm.order"].create(
            {
                "name": "Order 2",
                "person_id": self.fsm_person_2.id,
                "scheduled_date_start": self.start_datetime + timedelta(days=10),
                "scheduled_date_end": self.stop_datetime + timedelta(days=10),
                "location_id": self.fsm_location_1.id,
            }
        )

    def test_get_available_workers(self):
        fsm_available_worker = self.env["fsm.available.worker"].create(
            {
                "category_ids": self.category_1.ids,
                "start_datetime": self.start_datetime,
                "stop_datetime": self.stop_datetime,
            }
        )

        # Test if only Worker 1 is considered available
        available_workers = fsm_available_worker._get_available_workers(
            category_ids=self.category_1,
            start_datetime=self.start_datetime,
            stop_datetime=self.stop_datetime,
        )
        self.assertEqual(len(available_workers), 1)
        self.assertEqual(available_workers, self.fsm_person_2)

        # Test if both Worker 1 and Worker 2 are considered unavailable
        self.env["fsm.order"].create(
            {
                "name": "Order 3",
                "person_id": self.fsm_person_2.id,
                "scheduled_date_start": self.start_datetime - timedelta(days=3),
                "scheduled_date_end": self.stop_datetime + timedelta(days=3),
                "location_id": self.fsm_location_1.id,
            }
        )
        available_workers = fsm_available_worker._get_available_workers(
            category_ids=self.category_1,
            start_datetime=self.start_datetime,
            stop_datetime=self.stop_datetime,
        )
        self.assertEqual(len(available_workers), 0)
