from allure_section import allure_section


def test_all_steps_passed():
    with allure_section("Validate Electrical Power System activation") as section:
        with section.step("Validate Control Msg was sent"):
            pass
        with section.step("Validate Pin State is On"):
            pass
        with section.step("Validate Consumer reaction"):
            pass


def test_one_broken_step():
    with allure_section("Validate Electrical Power System activation") as section:
        with section.step("Validate Control Msg was sent"):
            pass
        with section.step("Validate Pin State is On"):
            raise Exception("Can't validate Pin State")
        with section.step("Validate Consumer reaction"):
            pass


def test_one_failed_step():
    with allure_section("Validate Electrical Power System activation") as section:
        with section.step("Validate Control Msg was sent"):
            raise AssertionError("Error during CAN Validating")
        with section.step("Validate Pin State is On"):
            pass
        with section.step("Validate Consumer reaction"):
            pass


def test_few_broken_steps():
    with allure_section("Validate Electrical Power System activation") as section:
        with section.step("Validate Control Msg was sent"):
            pass
        with section.step("Validate Pin State is On"):
            raise Exception("Can't validate Pin State")
        with section.step("Validate Consumer reaction"):
            raise Exception("Can't validate Consumer reaction")


def test_with_at_least_one_failure_step():
    with allure_section("Validate Electrical Power System activation") as section:
        with section.step("Validate Control Msg was sent"):
            raise AssertionError("Error during CAN Validating")
        with section.step("Validate Pin State is On"):
            raise Exception("Can't validate Pin State")
        with section.step("Validate Consumer reaction"):
            pass
