"""This module contains test data.

All functions here exist to test different aspects of Docstring Validator.
"""


def test_ping():
    """Verify gateway address is reachable after change in configuration.

    Test steps:
    1. Configure gateway address
    2. Ping gateway address from DUT
    3. Revert to initial configuration

    Pass criteria:
    - DUT accepts gateway address configuration
    - Gateway responds to at least 95% packets
    - Response time is under 200 ms
    - DUT accepts initial configuration

    Fail criteria:
    - DUT rejects gateway address configuration
    - Ping respond rate is below 95% threshold
    - Ping response time is above 200 ms
    - DUT configuration cannot be reverted to initial settings
    """
    ...


def test_BUG1701():
    """Simple docstring."""
    ...


def test_BUG2137():
    """Verify device can boot up after seven power resets.

    During field tests it was discovered that device cannot boot up after
    6 power resets performed within 10 minutes.

    Test steps:
    1. Perform power reset on device 7 times within 5 minutes
    2. Verify all processes are up after 7th reboot

    Pass criteria:
    - All processes are up after each reboot
    - Processes are brought up within 20 seconds from reboot

    Fail criteria:
    - Device does not boot up after any power reset
    - Boot up time exceeds 20 seconds

    Reference: BUG2137, BUG2042005
    """
    a=1


def abc():
    print(abc.__name__)

    few_lines = """Lorem ipsum dolor

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam ultricies
    eleifend urna, sed auctor nibh fringilla a. Sed eget enim venenatis,
    egestas nunc eu, accumsan mauris. Integer vestibulum vestibulum lacinia.
    Cras sit amet nisl tincidunt, molestie dolor at, tincidunt neque.
    Vestibulum dui dui, ornare id aliquam vel, sollicitudin vitae elit. In
    eleifend cursus lacinia. Curabitur sagittis convallis odio, quis faucibus
    libero placerat ut.
    """
    print(few_lines)


def deff():
    """dfsdff"""
    ...


def dummy():
    ...


def test_BUG2042005():
    """Verify device can boot up after seven power resets.

    During field tests it was discovered that device cannot boot up after
    6 power resets performed within 10 minutes.

    Test steps:
    1. Perform power reset on device 7 times within 5 minutes
    2. Verify all processes are up after 7th reboot

    Pass criteria:
    - All processes are up after each reboot
    - Processes are brought up within 20 seconds from reboot

    Fail criteria:
    - Device does not boot up after any power reset
    - Boot up time exceeds 20 seconds

    Reference:
    - BUG2137
    - BUG2042005
    """
    ...


class A:
    def b(self):
        pass

    def d(self):
        pass
