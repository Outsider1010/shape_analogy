def arithmetic(a:float, b:float, c:float) -> float:
    return c + b - a

def geometric(a:float, b:float, c:float) -> float:
    return c * b / a

def bounded(a:float, b:float, c:float) -> float:
    assert 0 < a < 1, f"forbidden value ({a}) for bounded analogy : {round(a, 2)}:{round(b, 2)}::{round(c, 2)}:?"
    assert 0 < b < 1, f"forbidden value ({b}) for bounded analogy : {round(a, 2)}:{round(b, 2)}::{round(c, 2)}:?"
    assert 0 < c < 1, f"forbidden value ({c}) for bounded analogy : {round(a, 2)}:{round(b, 2)}::{round(c, 2)}:?"
    
    return 1 / (1 + (1-c) * (1-b) * a / ((1-a) * b * c))

def ext_bounded(a:float, b:float, c:float, Ia: tuple[float, float], Ib: tuple[float, float],
                Ic: tuple[float, float], Id: tuple[float, float]) -> float:
    b_inf_a, b_sup_a = Ia
    b_inf_b, b_sup_b = Ib
    b_inf_c, b_sup_c = Ic
    b_inf_d, b_sup_d = Id
    assert b_inf_a < a < b_sup_a, f"forbidden value ({a}) for ext bounded analogy : {round(a, 2)}:{round(b, 2)}::{round(c, 2)}:?"
    assert b_inf_b < b < b_sup_b, f"forbidden value ({b}) for bounded analogy : {round(a, 2)}:{round(b, 2)}::{round(c, 2)}:?"
    assert b_inf_c < c < b_sup_c, f"forbidden value ({c}) for bounded analogy : {round(a, 2)}:{round(b, 2)}::{round(c, 2)}:?"

    return b_inf_d + ((b_sup_d - b_inf_d) / (1 +
            ((b_sup_c - c) * (b_sup_b - b) * (a - b_inf_a)) / ((c - b_inf_c) * (b - b_inf_b) * (b_sup_a - a))))
    
    
    
    