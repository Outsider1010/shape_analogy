from src.utils.constants import LEFT_RIGHT, UP_DOWN

def find_unique_bool(bool_list: tuple[bool, ...]):
    count_true = count_false = elem_true = elem_false = 0
    for i in range(len(bool_list)):
        if bool_list[i]:
            count_true += 1
            elem_true = i
        else:
            count_false += 1
            elem_false = i
    if count_true == 1:
        return elem_true
    if count_false == 1:
        return elem_false
    return None


def aux(__corner: int):
    return (__corner & LEFT_RIGHT) - 1, ((__corner & UP_DOWN) // 4) - 1
