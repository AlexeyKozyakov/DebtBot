from typing import Optional, TypedDict

DIRECTION_INCOMING = 1
DIRECTION_OUTGOING = 2

EXPRESSION_SIMBOLS = {'+', '-', '*', '/', '(', ')', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}


class DebtLine(TypedDict):
    users: list[str]
    is_incoming: bool
    amount: int


def parse_debts_text(text: str) -> list[DebtLine]:
    """
    debt_line_1,
    ...
    debt_line_n
    """
    debts = []
    for line in text.splitlines():
        line_trimmed = line.strip()
        if not line_trimmed:
            continue
        debt = __parse_debts_line(line_trimmed)
        if debt:
            debts.append(debt)
    return debts


def __parse_debts_line(line: str) -> Optional[DebtLine]:
    """
    (Я/Мне)|(@ник_1 ... @ник_n) мне|(@ник_1 ... @ник_n) 1234+123/3 <коммент_1> ... <коммент_n>
    """
    words = line.split()
    users = __parse_users(words) or __parse_users(words[1::])
    if not users:
        return None
    direction = __parse_direction(words[0]) or __parse_direction(words[len(users)])
    if not direction:
        return None
    amount = __parse_amount(words[len(users) + 1::])
    if not amount:
        return None
    return {
        'users': users,
        'is_incoming': direction == DIRECTION_INCOMING,
        'amount': amount
    }


def __parse_direction(word: str) -> Optional[int]:
    word_lowercase = word.lower()
    if word_lowercase == 'мне':
        return DIRECTION_INCOMING
    if word_lowercase == 'я':
        return DIRECTION_OUTGOING
    return None


def __parse_users(words: list[str]) -> Optional[list[str]]:
    users = []
    for word in words:
        if not word.startswith('@'):
            return users
        users.append(word[1::])


def __parse_amount(words: list[str]) -> Optional[int]:
    expression = __extract_expression(words)
    if not expression:
        return None
    try:
        return int(eval(expression))
    except SyntaxError:
        return None


def __extract_expression(words: list[str]) -> Optional[str]:
    expression = ''
    for word in words:
        for symbol in word:
            if symbol in EXPRESSION_SIMBOLS:
                expression += symbol
            else:
                return expression
    return expression
