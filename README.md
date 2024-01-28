# AllureSection Context Manager

This module provides a context manager `allure_section`, for running multiple validation steps in a common section. The context manager offers a `step` method for creating and executing individual steps inside the section.

## Example

```python
with allure_section("Validate Electrical Power System activation") as section:
    with section.step("Validate Control Msg was sent"):
        validate_control_msg(msg_state='on')

    with section.step("Validate Pin State is On"):
        validate_pin_state_function(pin_state='on')

    with section.step("Validate Consumer reaction"):
        validate_consumer_reaction_function(consumer_state='power_on')
```

The above code demonstrates the creation of a section named "Validate Electrical Power System activation" with three individual steps inside it. The steps will be executed in the order they were created, and any exceptions will be collected and raised at the end of the section. This approach ensures that all steps in the section are validated before handling any failures.

**Note**: Use this context manager only when you need to validate multiple steps within the same section. Avoid using it for running multiple steps that change conditions to prevent unexpected behavior.

### Example Report

You can view an example report generated using `allure_section` by following [this link](https://raw.githack.com/timofeevx/allure_section/develop/examples/allure-report/index.html).

![allure-report.gif](examples/allure-report.gif)]

<br><br><br>

## Implementation Details

### Custom Exception Class

This module includes a `MultipleExceptions` and a `MultipleErrors` classes, custom exception types designed to aggregate section exceptions. They allows the user to identify and handle multiple exceptions/errors collectively.

### Section Context Class

The `SectionContext` class serves as the main context manager for the `allure_section`. It handles the entry and exit points of the section, logs relevant information, and manages exceptions. The `step` method is used to create individual steps within the section.

### Usage

```python
# Import the allure_section context manager
from allure_section_module import allure_section

# ...

# Use the allure_section context manager in your test code
with allure_section("Your Section Title") as section:
    with section.step("Step 1"):
        # Your validation code for Step 1

    with section.step("Step 2"):
        # Your validation code for Step 2

    # ...
```

Ensure that you have the necessary dependencies, including the `allure_commons` library, for using this module in your test environment.
