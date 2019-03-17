import validate_types_v1 as validate_types

class Validate:

    def check(self, config, request):
        for key, value in request.items():
            if key not in config['keys'].keys():
                if config['allow_extended']:
                    continue
                else:
                    return {"error": "Field {} not allowed in reequest".format(key)}
            if config['keys'][key][type] not in validate_types.ValidateTypes.mapping.keys():
                return {"error": "Unknown type of field {} in config".format(key)}

            func = getattr(validate_types.ValidateTypes, validate_types.ValidateTypes.mapping[config['keys'][key][type]])

            if func(value) is False:
                return {"error": "Field {} should be {}".format(key, config['keys'][key][type])}

        for key in config['keys']:
            if (config['keys'][key]['is_optional'] is False) and (key not in request.keys()):
                return {"error": "Field {} should be present in request".format(key)}

        return {"status": "success"}

