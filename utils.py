def get_variants(s: str) -> list[str]:
    return s.split(' *')


def cut(s: str) -> str:
    return s.split(' *')[0]


def reverse_dict(dct: dict) -> dict:
    new_dict = {}
    for k, v in dct.items():
        new_dict[v] = k
    return new_dict
