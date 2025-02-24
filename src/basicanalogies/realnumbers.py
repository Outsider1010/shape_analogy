def arithmetic(a: float, b: float, c: float) -> float:
    """
    Realize the arithmetic analogical proportion on R (the set of real numbers) to solve the equation `a`:`b`::`c`:?
    :param a: a real number `a`
    :param b: a real number `b`
    :param c: a real number `c`
    :return: a real number `d` solution of the equation
    """
    return c + b - a


def geometric(a: float, b: float, c: float) -> float:
    """
    Realize the geometric analogical proportion on R* (the set of real numbers excluding 0)
    to solve the equation `a`:`b`::`c`:?
    :param a: a real nonzero number `a`
    :param b: a real nonzero number `b`
    :param c: a real nonzero number `c`
    :return: a real nonzero number `d` solution of the equation
    """
    return c * b / a


def bounded(a: float, b: float, c: float) -> float:
    """
    Realize a particular analogical proportion on (0, 1) to solve the equation `a`:`b`::`c`:?
    :param a: a real number between 0 and 1 `a`
    :param b: a real number between 0 and 1 `b`
    :param c: a real number between 0 and 1 `c`
    :return: a real numer `d` solution of the equation
    """
    assert 0 < a < 1, f"forbidden value ({a}) for bounded analogy : {round(a, 2)}:{round(b, 2)}::{round(c, 2)}:?"
    assert 0 < b < 1, f"forbidden value ({b}) for bounded analogy : {round(a, 2)}:{round(b, 2)}::{round(c, 2)}:?"
    assert 0 < c < 1, f"forbidden value ({c}) for bounded analogy : {round(a, 2)}:{round(b, 2)}::{round(c, 2)}:?"

    return 1 / (1 + (1 - c) * (1 - b) * a / ((1 - a) * b * c))


def ext_bounded(a: float, b: float, c: float, Ia: tuple[float, float], Ib: tuple[float, float],
                Ic: tuple[float, float], Id: tuple[float, float]) -> float:
    """
    Realize a particular analogical proportion on dynamic intervals to solve the equation `a`:`b`::`c`:?
    :param a: a real number `a` within the interval `Ia` (exclusive)
    :param b: a real number `b` within the interval `Ib` (exclusive)
    :param c: a real number `c` within the interval `Ic` (exclusive)
    :param Ia: the interval (a couple of real numbers) of values for `a`
    :param Ib: the interval of values for `b`
    :param Ic: the interval of values for `c`
    :param Id: the interval of values for the solution `d`
    :return: d, a real number within the interval `d` solution of the equation
    """
    b_inf_a, b_sup_a = Ia
    b_inf_b, b_sup_b = Ib
    b_inf_c, b_sup_c = Ic
    b_inf_d, b_sup_d = Id
    assert b_inf_a < a < b_sup_a, f"forbidden value ({a}) for ext bounded analogy : {round(a, 2)}:{round(b, 2)}::{round(c, 2)}:?"
    assert b_inf_b < b < b_sup_b, f"forbidden value ({b}) for bounded analogy : {round(a, 2)}:{round(b, 2)}::{round(c, 2)}:?"
    assert b_inf_c < c < b_sup_c, f"forbidden value ({c}) for bounded analogy : {round(a, 2)}:{round(b, 2)}::{round(c, 2)}:?"

    return b_inf_d + ((b_sup_d - b_inf_d) / (1 +
                                             ((b_sup_c - c) * (b_sup_b - b) * (a - b_inf_a)) / (
                                                         (c - b_inf_c) * (b - b_inf_b) * (b_sup_a - a))))


def asc_couple(a: tuple[float, float], b: tuple[float, float], c: tuple[float, float]) -> tuple[float, float]:
    a1, a2 = a
    b1, b2 = b
    c1, c2 = c
    assert 0 <= a1 <= a2 <= 1 and a1 != 1
    assert 0 <= b1 <= b2 <= 1 and b1 != 1
    assert 0 <= c1 <= c2 <= 1 and c1 != 1
    return bounded(a1, b1, c1), bounded((a2 - a1) / (1 - a1), (b2 - b1) / (1 - b1), (c2 - c1) / (1 - c1))

