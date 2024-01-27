from allure_section._allure_section import SectionContext


def allure_section(title):
    """Call contextmanager for AllureSecction

    Args:
        title: Title of the section

    Returns:
        SectionContext
    """
    return SectionContext(title)
