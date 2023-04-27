# Copyright 2021 - TODAY, Escodoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Fieldservice Project Domain Filter Project Tasks",
    "summary": """
        Add domain on task to filter only project tasks""",
    "version": "12.0.1.0.0",
    "license": "AGPL-3",
    "author": "Escodoo,Odoo Community Association (OCA)",
    "website": "https://github.com/Escodoo/account-addons",
    "maintainers": ["marcelsavegnago"],
    "images": ["static/description/banner.png"],
    "category": "Field Service",
    "depends": [
        "fieldservice_project",
    ],
    "data": [
        "views/fsm_order.xml",
    ],
}
