import re


def validate_cpf(cpf: str | None) -> bool:
    if cpf is None:
        return False

    cpf = "".join(filter(str.isdigit, cpf))

    if len(cpf) != 11:
        return False

    sum_total = 0
    for i in range(9):
        sum_total += int(cpf[i]) * (10 - i)
    digit_1 = (sum_total * 10) % 11
    digit_1 %= 10

    sum_total = 0
    for i in range(10):
        sum_total += int(cpf[i]) * (11 - i)
    digit_2 = (sum_total * 10) % 11
    digit_2 %= 10

    if int(cpf[9]) != digit_1 or int(cpf[10]) != digit_2:
        return False

    return True


def validate_email(email: str | None) -> bool:
    if email is None:
        return False

    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if not re.match(pattern, email):
        return False

    return True
