import allure


class AllureSection:

    class Step:

        def __init__(self, manager, step_name: str):
            self.manager = manager
            self.step_name = step_name

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            return

    def __init__(self, section_name):
        self.section_name = section_name

        self._step = None
        self._step_kwargs = {}

        self._steps = []
        self._exceptions = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__execute_steps()

        if self._exceptions:
            for exception in self._exceptions:
                raise exception

    def step(self, step_name):
        self._step = self.Step(self, step_name)
        return self._step

    def execute(self, func, *args, **kwargs):
        step_data = {
            "step_name": self._step.step_name,
            "func": func,
            "args": args,
            "kwargs": kwargs
        }

        self._steps.append(step_data)

    def __execute_steps(self):
        with allure.step(self.section_name):

            for step in self._steps:
                name, func, args, kwargs = step.values()

                try:
                    with allure.step(name):
                        func(*args, **kwargs)
                except Exception as e:
                    self._exceptions.append(e)

            if self._exceptions:
                raise AssertionError(f"Some faults inside `{self.section_name}`")
