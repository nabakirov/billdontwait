def getargs(request, *keys, default_val=None):

    json = request.get_json(force=True, silent=True)
    out = []
    for key in keys:
        out.append(
            request.args.get(key) or request.form.get(key) or (
                json.get(key, default_val) if isinstance(json, dict) else default_val)
        )
    return tuple(out)
