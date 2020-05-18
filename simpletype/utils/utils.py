def str_limit(s):
    s = str(s)
    if len(s) > 20:
        return s[:20] + '...'
    return s

def type_name_ref(val):
    return val.__class__.__name__


def predicate_filtered_list(arr, predicate):
    return [i for i in arr if predicate(i)]


def type_filtered_list(arr, t):
    return predicate_filtered_list(
        arr,
        lambda x: type(x) is t,
    )



