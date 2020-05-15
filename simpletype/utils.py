def str_limit(s):
    s = str(s)
    if len(s) > 20:
        return s[:20] + '...'
    return s


def type_name_ref(val):
    return val.__class__.__name__
