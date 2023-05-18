import datetime

from peewee import *

db = SqliteDatabase('debts.db')


class BaseModel(Model):
    class Meta:
        database = db


class Debt(BaseModel):
    from_user = CharField()
    to_user = CharField()
    amount = IntegerField()
    created_date = TimestampField()
    is_payed = BooleanField()


Debt.create_table()


def __is_user_debt(user: str):
    return (Debt.from_user == user) | (Debt.to_user == user)


def create_debt(from_user: str, to_user: str, amount: int):
    assert from_user != to_user
    return Debt.create(from_user=from_user, to_user=to_user, amount=amount,
                       created_date=datetime.datetime.now(), is_payed=False)


def mark_debts_as_payed(first_user: str, second_user: str):
    Debt.update(is_payed=True).where((Debt.from_user == first_user) & (Debt.to_user == second_user)
                                     | (Debt.from_user == second_user) & (Debt.to_user == first_user)).execute()


def mark_all_debts_as_payed(user: str):
    Debt.update(is_payed=True).where(__is_user_debt(user)).execute()


def calculate_total_debts(user: str):
    debts = Debt.select().where(__is_user_debt(user) & (~Debt.is_payed))
    total = {}
    for debt in debts:
        is_incoming = debt.to_user == user
        debt_user = debt.from_user if is_incoming else debt.to_user
        if debt_user not in total:
            total[debt_user] = 0
        total[debt_user] += -debt.amount if is_incoming else debt.amount
    total = {user: debt for user, debt in total.items() if debt != 0}
    return total


def get_all_debts(user: str):
    return Debt.select().where(__is_user_debt(user))
