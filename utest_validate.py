import validate as validator
import validate_types
import unittest


class ValidateTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.validator = validator.Validate()

        cls.correct_config_allow_extended = {
            "keys": {
                "var1": {type: "int", "is_optional": True},
                "var2": {type: "str", "is_optional": False},
                "var3": {type: "bool", "is_optional": True},
                "var4": {type: "bool", "is_optional": False},
                "var5": {type: "int", "is_optional": True},
                "var6": {type: "str", "is_optional": False},
                "var7": {type: "bool", "is_optional": True}
            },
            "allow_extended": True
        }

        cls.correct_config_disable_extended = {
            "keys": {
                "var1": {type: "int", "is_optional": True},
                "var2": {type: "str", "is_optional": False},
                "var3": {type: "bool", "is_optional": True},
                "var4": {type: "bool", "is_optional": False},
                "var5": {type: "int", "is_optional": True},
                "var6": {type: "str", "is_optional": False},
                "var7": {type: "bool", "is_optional": True}
            },
            "allow_extended": False
        }
        cls.correct_request = {
            "var1": 10,
            "var2": "str",
            "var3": True,
            "var4": True,
            "var5": 5,
            "var6": "True"
        }

        cls.request_more_extended = {
            "var1": 10,
            "var2": "str",
            "var3": True,
            "var4": True,
            "var5": 5,
            "var6": "True",
            "var11": "True"
        }

        cls.request_not_present_all_mandatoty_vars = {
            "var1": 10,
            "var2": "str",
            "var3": True,
            # "var4": True,
            "var5": 5,
            "var6": "True",
            "var11": "True"
        }

    def test_validator_correct_config_allow_extended_correct_config(self):
        self.assertEqual(self.validator.check(self.correct_config_allow_extended, self.correct_request),
                         {'status': 'success'})

    def test_validator_correct_config_allow_extended____request_more_extended(self):
        self.assertEqual(self.validator.check(self.correct_config_allow_extended, self.request_more_extended),
                         {'status': 'success'})

    def test_validator_correct_config_disable_extended____request_more_extended(self):
        self.assertEqual(self.validator.check(self.correct_config_disable_extended, self.request_more_extended),
                         {'error': 'Field var11 not allowed in request'})

    def test_validator_correct_config_allow_extended____request_not_present_all_mandatoty_vars(self):
        self.assertEqual(self.validator.check(self.correct_config_allow_extended,
                                              self.request_not_present_all_mandatoty_vars),
                         {'error': 'Field var4 should be present in request'})
        self.subTest(self.assertEqual(self.validator.check(self.correct_config_allow_extended,
                                              self.request_not_present_all_mandatoty_vars),
                         {'error': 'Field var4 should be present in request'}))

    def test_validator_correct_url(self):
        checks_ok = ['http://i.ua','http://google.com.ua/']
        checks_error = ['h1ttp://i.ua','http:google.com.ua/']
        for url in checks_ok:
            self.subTest(self.assertTrue(validate_types.ValidateTypes.check_url(url)))
        for url in checks_error:
            self.subTest(self.assertIsNot(validate_types.ValidateTypes.check_url(url),True))



if __name__ == '__main__':
    unittest.main()
