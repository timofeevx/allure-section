"""AllureSection context manager

This module provides a context manager for running multiple validation steps in a common section.
The context manager provides a `step` method for creating a new step inside the section.

Example:
    ```
    with allure_section("Validate Electrical Power System activation") as section:
        with section.step("Validate Control Msg was sent"):
            validate_control_msg(msg_state='on')

        with section.step("Validate Pin State is On"):
            validate_pin_state_function(pin_state='on')

        with section.step("Validate Consumer reaction"):
            validate_consumer_reaction_function(consumer_state='power_on')
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

import logging
from contextlib import contextmanager

import allure
from allure_commons._core import plugin_manager
from allure_commons.utils import uuid4


logger = logging.getLogger("Allure Section")


class MultipleExceptions(Exception):
    """Custom ExceptionClass for aggregate Section exceptions"""

    def __init__(self, exceptions):
        """Initialize MultipleExceptions instance"""
        self.exceptions = exceptions
        super().__init__()

    def __str__(self):
        """Generate output for MultipleExceptions message"""
        exceptions = ''.join([f"\n{i}. {e.__class__.__name__}: {e}" for i, e in enumerate(self.exceptions, start=1)])
        return f"Occurred.\n\nMultiple exceptions occurred:{exceptions}"


class SectionContext:
    """Section Context for AllureSection"""

    def __init__(self, title):
        """Create AllureSection instance

        Args:
            title: name of the section (It will be provided to the `allure.step`)
        """
        self.title = title
        self.uuid = uuid4()
        self.params = {}
        self._exceptions = []
        self._exc_type = AssertionError  # As a priority exception type to raise

    def __enter__(self):
        """Enter to the section context"""
        logger.info(f"Enter section <{self.title}>")
        plugin_manager.hook.start_step(uuid=self.uuid, title=self.title, params=self.params)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit from the section context"""
        logger.info(f"Exit from section <{self.title}>")
        if self._exceptions:
            if len(self._exceptions) == 1:
                exception = self._exceptions[0]
                exc_type = type(exception)
                exc_val = exception
                exc_tb = exception.__traceback__
            else:
                exc_type = self._exc_type if self._exc_type in [type(e) for e in self._exceptions] else Exception
                exc_val = MultipleExceptions(self._exceptions)

        plugin_manager.hook.stop_step(uuid=self.uuid, title=self.title, exc_type=exc_type, exc_val=exc_val,
                                      exc_tb=exc_tb)
        if exc_type:
            raise exc_type(exc_val)

    @contextmanager
    def step(self, step_name):
        """Create step context

        Args:
            step_name: name of the step (It will be provided to the `allure.step`)
        """
        logger.info(f"Executing step <{step_name}>")
        try:
            with allure.step(step_name):
                yield
        except Exception as e:
            logger.warning(f"Caught exception: {str(e)}")
            self._exceptions.append(e)
