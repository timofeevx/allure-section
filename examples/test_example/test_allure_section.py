from allure_section import allure_section


def test_positive_section():
    with allure_section("Positive test section") as section:
        with section.step("First step validation"):
            pass
        with section.step("Second step validation"):
            pass
        with section.step("Third step validation"):
            pass
        with section.step("Fourth step validation"):
            pass
        with section.step("Fifth step validation"):
            pass


def test_one_negative_exception():
    with allure_section("Positive test section") as section:
        with section.step("First step validation"):
            pass
        with section.step("Second step validation"):
            raise Exception("Failed exception here")
        with section.step("Third step validation"):
            pass
        with section.step("Fourth step validation"):
            pass
        with section.step("Fifth step validation"):
            pass


def test_one_negative_error():
    with allure_section("Positive test section") as section:
        with section.step("First step validation"):
            pass
        with section.step("Second step validation"):
            pass
        with section.step("Third step validation"):
            pass
        with section.step("Fourth step validation"):
            raise AssertionError("AssertionError here")
        with section.step("Fifth step validation"):
            pass


def test_few_negative_exceptions():
    with allure_section("Positive test section") as section:
        with section.step("First step validation"):
            pass
        with section.step("Second step validation"):
            pass
        with section.step("Third step validation"):
            raise Exception("Failed exception here")
        with section.step("Fourth step validation"):
            raise ZeroDivisionError("ZeroDivisionError here")
        with section.step("Fifth step validation"):
            pass


def test_few_negative_exceptions_and_errors():
    with allure_section("Positive test section") as section:
        with section.step("First step validation"):
            raise AssertionError("AssertionError here")
        with section.step("Second step validation"):
            pass
        with section.step("Third step validation"):
            raise Exception("Failed exception here")
        with section.step("Fourth step validation"):
            raise ZeroDivisionError("ZeroDivisionError here")
        with section.step("Fifth step validation"):
            pass


def test_few_sections():
    with allure_section("Positive section") as section:
        with section.step("First step validation"):
            pass
        with section.step("Second step validation"):
            pass
        with section.step("Third step validation"):
            pass

    with allure_section("Negative test section") as section:
        with section.step("First step validation"):
            raise Exception("Failed exception here")
        with section.step("Second step validation"):
            pass
        with section.step("Third step validation"):
            pass
        with section.step("Fourth step validation"):
            raise ZeroDivisionError("ZeroDivisionError here")
        with section.step("Fifth step validation"):
            pass

    with allure_section("Positive test section") as section:
        with section.step("First step validation"):
            pass
        with section.step("Second step validation"):
            pass
