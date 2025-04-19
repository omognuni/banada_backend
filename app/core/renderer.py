import re

from rest_framework.renderers import JSONRenderer


def camelize(data):
    if isinstance(data, list):
        return [camelize(item) for item in data]
    elif isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            new_key = re.sub(r"_([a-z])", lambda x: x.group(1).upper(), key)
            new_dict[new_key] = camelize(value)
        return new_dict
    else:
        return data


class CamelCaseJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        data = camelize(data)
        return super().render(data, accepted_media_type, renderer_context)
