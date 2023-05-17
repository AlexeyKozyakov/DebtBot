import unittest

from peewee import SqliteDatabase

import core.debts
from core.debts import Debt

MODELS = [Debt]

test_db = SqliteDatabase(':memory:')


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)
        self.init_test_data()

    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()

    @staticmethod
    def init_test_data():
        core.debts.create_debt("sergey", "alexey", 120)
        core.debts.create_debt("sergey", "alexey", 35)
        core.debts.create_debt("sergey", "alexey", 228)
        core.debts.create_debt("alexey", "sergey", 75)
        core.debts.create_debt("alexey", "sergey", 21)
        core.debts.create_debt("alexey", "artem", 100)
        core.debts.create_debt("artem", "alexey", 25),
        core.debts.create_debt("alexey", "artem", 75)
        core.debts.create_debt("sergey", "artem", 25)

    def test_total_debts(self):
        self.assertEqual(
            {
                'sergey': -287,
                'artem': 150
            },
            core.debts.calculate_total_debts("alexey")
        )

    def test_no_zero_debts(self):
        core.debts.create_debt('alexey', 'sergey', 287)
        self.assertEqual(
            {
                'artem': 150
            },
            core.debts.calculate_total_debts("alexey")
        )

    def test_mark_debts_as_payed(self):
        core.debts.mark_debts_as_payed("alexey", "artem")
        self.assertEqual(
            {
                'sergey': -287,
            },
            core.debts.calculate_total_debts("alexey")
        )

    def test_mark_all_debts_as_payed(self):
        core.debts.mark_all_debts_as_payed("alexey")
        self.assertEqual(
            {},
            core.debts.calculate_total_debts("alexey")
        )

    def test_get_debts(self):
        self.assertEqual(
            [
                {'amount': 120, 'from': 'sergey', 'payed': False, 'to': 'alexey'},
                {'amount': 35, 'from': 'sergey', 'payed': False, 'to': 'alexey'},
                {'amount': 228, 'from': 'sergey', 'payed': False, 'to': 'alexey'},
                {'amount': 75, 'from': 'alexey', 'payed': False, 'to': 'sergey'},
                {'amount': 21, 'from': 'alexey', 'payed': False, 'to': 'sergey'},
                {'amount': 100, 'from': 'alexey', 'payed': False, 'to': 'artem'},
                {'amount': 25, 'from': 'artem', 'payed': False, 'to': 'alexey'},
                {'amount': 75, 'from': 'alexey', 'payed': False, 'to': 'artem'}
            ],
            [
                {
                    'from': debt.from_user,
                    'to': debt.to_user,
                    'amount': debt.amount,
                    'payed': debt.is_payed
                }
                for debt in core.debts.get_all_debts("alexey")
            ]
        )
