class Validate:
    mapping = {
        "int": "check_int",
        "str": "check_string",
        "bool": "check_bool"
    }

    @staticmethod
    def check_int(value):
        if type(value) is int:
            return True
        return False

    @staticmethod
    def check_string(value):
        if type(value) is str:
            return True
        return False

    @staticmethod
    def check_bool(value):
        if type(value) is bool:
            return True
        return False

    def check(self, config, request):
        for key, value in request.items():
            if key not in config['keys'].keys():
                if config['allow_extended']:
                    continue
                else:
                    return {"error": "Field {} not allowed in reequest".format(key)}
            if config['keys'][key][type] not in self.mapping.keys():
                return {"error": "Unknown type of field {} in config".format(key)}

            func = getattr(self, self.mapping[config['keys'][key][type]])

            if func(value) is False:
                return {"error": "Field {} should be {}".format(key, config['keys'][key][type])}

        for key in config['keys']:
            if (config['keys'][key]['is_optional'] == False) and (key not in request.keys() ):
                return {"error": "Field {} should be present in request".format(key)}

        return {"status": "success"}

def check_result():
    pass
    # correct_config_allow_extended = {
    #     "keys": {
    #         "var1": {type: "int", "is_optional": True},
    #         "var2": {type: "str", "is_optional": False},
    #         "var3": {type: "bool", "is_optional": True},
    #         "var4": {type: "bool", "is_optional": False},
    #         "var5": {type: "int", "is_optional": True},
    #         "var6": {type: "str", "is_optional": False},
    #         "var7": {type: "bool", "is_optional": True}
    #     },
    #     "allow_extended": True
    # }
    #
    # correct_config_disable_extended = {
    #     "keys": {
    #         "var1": {type: "int", "is_optional": True},
    #         "var2": {type: "str", "is_optional": False},
    #         "var3": {type: "bool", "is_optional": True},
    #         "var4": {type: "bool", "is_optional": False},
    #         "var5": {type: "int", "is_optional": True},
    #         "var6": {type: "str", "is_optional": False},
    #         "var7": {type: "bool", "is_optional": True}
    #     },
    #     "allow_extended": False
    # }
    # correct_request = {
    #     "var1": 10,
    #     "var2": "str",
    #     "var3": True,
    #     "var4": True,
    #     "var5": 5,
    #     "var6": "True"
    # }
    #
    # request_more_extended = {
    #     "var1": 10,
    #     "var2": "str",
    #     "var3": True,
    #     "var4": True,
    #     "var5": 5,
    #     "var6": "True",
    #     "var11": "True"
    # }
    #
    # request_not_present_all_mandatoty_vars = {
    #     "var1": 10,
    #     "var2": "str",
    #     "var3": True,
    #     # "var4": True,
    #     "var5": 5,
    #     "var6": "True",
    #     "var11": "True"
    # }
    #
    #
    # validator = Validate()
    # print(validator.check(correct_config_allow_extended, correct_request))
    # print(validator.check(correct_config_allow_extended, request_more_extended))
    # print(validator.check(correct_config_disable_extended, request_more_extended))
    # print(validator.check(correct_config_allow_extended, request_not_present_all_mandatoty_vars))
