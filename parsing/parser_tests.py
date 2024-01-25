import unittest

from parsing.parser import parse_debts_text


class ParserTestsCase(unittest.TestCase):
    def test_parse_incoming_debt(self):
        self.assertEqual(
            [
                {
                    'users': ['sergey'],
                    'is_incoming': True,
                    'amount': 5300
                }
            ],
            parse_debts_text(
                """
                @sergey мне 5000 + 300
                """
            )
        )

    def test_parse_incoming_debt_reversed(self):
        self.assertEqual(
            [
                {
                    'users': ['sergey'],
                    'is_incoming': True,
                    'amount': 300
                }
            ],
            parse_debts_text(
                """
                Мне @sergey 800/4 + 40 + 60
                """
            )
        )

    def test_parse_outgoing_debt(self):
        self.assertEqual(
            [
                {
                    'users': ['sergey'],
                    'is_incoming': False,
                    'amount': 444
                }
            ],
            parse_debts_text(
                """
                Я @sergey 333 + 111
                """
            )
        )

    def test_parse_debt_with_comments(self):
        self.assertEqual(
            [
                {
                    'users': ['sergey'],
                    'is_incoming': True,
                    'amount': 200
                }
            ],
            parse_debts_text(
                """
                Мне @sergey 600/3 за хостинг бота
                """
            )
        )

    def test_parse_no_debt(self):
        self.assertEqual(
            [],
            parse_debts_text(
                """
                @sergey через 2 часа идем
                """
            )
        )

    def test_parse_incoming_debt_with_multiple_users(self):
        self.assertEqual(
            [
                {
                    'users': ['sergey', 'artem', 'boris'],
                    'is_incoming': True,
                    'amount': 2000
                }
            ],
            parse_debts_text(
                """
                @sergey @artem @boris мне 8000/4 игры
                """
            )
        )

    def test_parse_outgoing_debt_multiple_users(self):
        self.assertEqual(
            [
                {
                    'users': ['sergey', 'artem', 'boris'],
                    'is_incoming': False,
                    'amount': 2500
                }
            ],
            parse_debts_text(
                """
                Я @sergey @artem @boris 10000/4 игры
                """
            )
        )

    def test_parse_multiple_debts(self):
        self.assertEqual(
            [
                {
                    'users': ['sergey', 'artem', 'boris'],
                    'is_incoming': False,
                    'amount': 150
                },
                {
                    'users': ['sergey', 'boris'],
                    'is_incoming': True,
                    'amount': 400
                }
            ],
            parse_debts_text(
                """
                Я @sergey @artem @boris 600/4 еда
                @sergey @boris мне 400
                """
            )
        )

    def test_parse_debt_with_brackets(self):
        self.assertEqual(
            [
                {
                    'users': ['sergey'],
                    'is_incoming': False,
                    'amount': 666
                }
            ],
            parse_debts_text(
                """
                Я @sergey (700 + 233 + 400) / 2
                """
            )
        )

    def test_no_debt_with_incorrect_expression(self):
        self.assertEqual(
            [],
            parse_debts_text(
                """
                Я @sergey (700 + 233 + 400 / 2
                """
            )
        )

    def test_no_debt_with_undefined_expression(self):
        self.assertEqual(
            [],
            parse_debts_text(
                """
                Я @sergey (700 + 233 + a) / 2
                """
            )
        )
