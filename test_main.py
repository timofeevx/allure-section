import allure

from allure_section import AllureSection


def func_(a, b):
    print()
    assert a + b == 4, f"a = {a}, b = {b}"


def test_func_():

    with AllureSection("Validation section") as section:

        with section.step("Validation 1"):
            section.execute(func_, 0, 4)

        with section.step("Validation 2"):
            section.execute(func_, 1, b=3)

        with section.step("Validation 3"):
            section.execute(func_, 2, b=2)

    with allure.step("Other step"):
        func_(1, 3)

    with AllureSection("Validation section 2") as section:

        with section.step("Validation 1"):
            section.execute(func_, 0, 4)

        with section.step("Validation 2"):
            section.execute(func_, 1, b=3)

        with section.step("Validation 3"):
            section.execute(func_, 2, b=2)
