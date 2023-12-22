"""AllureSection context manager

This module provides a context manager for running multiple validation steps in a common section.
The context manager provides a `step` method for creating a new step inside the section.

Example:
    ```
    with AllureSection("Validate Electrical Power System activation") as section:
        with section.step("Validate Control Msg was sent"):
            section.execute(validate_control_msg, msg_state='on')

        with section.step("Validate Pin State is On"):
            section.execute(validate_pin_state_function, pin_state='on')

        with section.step("Validate Consumer reaction"):
            section.execute(validate_consumer_reaction_function, consumer_state='power_on')
    ```

    The above code will create a section with the name "Validate Electrical Power System activation" and three steps
    inside it. The steps will be named "Validate Control Msg was sent", "Validate Pin State is On" and "Validate
    Consumer reaction". The steps will be executed in the order they were created, and the exceptions will be
    collected and raised at the end of the section. It will help to validate all steps in the section and not fall
    victim to the first step that fails.

    Pay attention!:
        Use this context manager only if you need to validate multiple steps in the same section.
        Do not use it for run multiple steps that change condition to avoid unexpected behaviour.
"""

import allure


class AllureSection:
    """Context manager for running multiple validation steps in a common section"""

    class AllureSectionStep:
        """Wrapper for describes step as a context"""

        def __init__(self, manager, step_name: str):
            """Create AllureSectionStep instance

            Args:
                manager: parent of the step
                step_name: name fot the step (It will be provided to the `allure.step`)
            """
            self.manager = manager
            self.step_name = step_name

        def __enter__(self):
            """Enter to the step context"""
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            """Exit from the step context"""

        def execute(self, func, *args, **kwargs):
            """Provide function link into collection for future execution in the loop"""
            self.manager.execute(func, *args, **kwargs)

    class AllureSectionException(Exception):
        """Exception for AllureSection"""""

        def __init__(self, message):
            """Create AllureSectionException instance

            Args:
                message: error message
            """
            super().__init__(message)

    def __init__(self, section_name):
        """Create AllureSection instance

        Args:
            section_name: name of the section (It will be provided to the `allure.step`)
        """
        self.section_name = section_name

        self._step = None
        self._step_kwargs = {}

        self._steps = []
        self._exceptions = []

    def __enter__(self):
        """Enter to the section context"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit from the section context"""
        self.__execute_steps()

    def step(self, step_name) -> AllureSectionStep:
        """Create a new step inside the section

        Args:
            step_name: name of the step (It will be provided to the `allure.step`)
        """
        self._step = self.AllureSectionStep(self, step_name)
        return self._step

    def execute(self, func, *args, **kwargs):
        """Provide function link into collection for future execution in the loop

        Args:
            func: link to the function
        """
        step_data = {
            "step_name": self._step.step_name,
            "func": func,
            "args": args,
            "kwargs": kwargs
        }

        self._steps.append(step_data)

    def __execute_steps(self):
        """Execute steps"""
        with allure.step(self.section_name):

            for step in self._steps:
                name, func, args, kwargs = step.values()

                try:
                    with allure.step(name):
                        func(*args, **kwargs)
                except Exception as e:
                    self._exceptions.append(e)

            if self._exceptions:
                formatted_exceptions = '\b'.join([f"{i}. {e}" for i, e in enumerate(self._exceptions, start=1)])
                raise self.AllureSectionException(f"Occurred:\n {formatted_exceptions}")
