def _template_to_title(template) -> str:
    column_names = [s.split(":")[0] for s in template.strip("{}").split("}{")]
    column_dict = {t: t for t in column_names}
    return template.format(**column_dict)
