import csv
from ..models.core import db


def clear_database():
    ...


def populate_database(base_path='/usr/src/api/app/data/'):
    ...

    # with open(base_path + 'orders.csv') as csvfile:
    #     reader = csv.DictReader(csvfile)
    #     for row in reader:
    #         order = Orders(
    #             #
    #             id = row['id'],
    #             created_at = row['created_at'],
    #             vendor_id = row['vendor_id'],
    #             customer_id = row['customer_id'],
    #         )
    #         db.session.add(order)


