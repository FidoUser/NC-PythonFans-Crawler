import validate_types


class Validate:


    def check_keys(self, keys, config):
        for key, value in keys.items():
            if key not in config['keys'].keys():
                if config['allow_extended']:
                    continue
                else:
                    return {"error": "Field {} not allowed in request".format(key)}
            if config['keys'][key][type] not in validate_types.ValidateTypes.mapping.keys():
                return {"error": "Unknown type of field {} in config".format(key)}

            func = getattr(validate_types.ValidateTypes,
                           validate_types.ValidateTypes.mapping[config['keys'][key][type]])

            if func(value) is False:
                return {"error": "Field {} should be {}".format(key, config['keys'][key][type])}


    # @staticmethod
    def check(self, config, request):
        # for key, value in request.items():
        #     if key not in config['keys'].keys():
        #         if config['allow_extended']:
        #             continue
        #         else:
        #             return {"error": "Field {} not allowed in request".format(key)}
        #     if config['keys'][key][type] not in validate_types.ValidateTypes.mapping.keys():
        #         return {"error": "Unknown type of field {} in config".format(key)}
        #
        #     func = getattr(validate_types.ValidateTypes,
        #                    validate_types.ValidateTypes.mapping[config['keys'][key][type]])
        #
        #     if func(value) is False:
        #         return {"error": "Field {} should be {}".format(key, config['keys'][key][type])}

        res = self.check_keys(request, config)
        if res != None:
            return res
        for key in config['keys']:
            if (config['keys'][key]['is_optional'] is False) and (key not in request.keys()):
                return {"error": "Field {} should be present in request".format(key)}

        return {"status": "success"}

