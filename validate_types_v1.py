class ValidateTypes:
    # def __init__(self):
    #     self.mapping = {
    #         "int": "check_int",
    #         "str": "check_string",
    #         "bool": "check_bool"
    #     }

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

    @staticmethod
    def check_list(value):
        if type(value) is list:
            return True
        return False

