def remap(indict, *args, **kwargs):
    """
    Re-map keys of indict using information from arguments.

    Non-keyword arguments are keys of input dictionary that are passed
    unchanged to the output. Keyword arguments must be in the form

    new="old"

    and act as a translation table for new key names.
    """
    outdict = {role: indict[role] for role in args}
    outdict.update(
        {new: indict[old] for new, old in kwargs.items()}
    )
    return outdict

