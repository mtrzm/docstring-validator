from docstring_validator import chunks

VALID_DOCSTRING = """Verify device can boot up after seven power resets.

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


RAW_CHUNKS = {
    chunks.ChunkTypes.DESCRIPTION: VALID_DOCSTRING.split("\n")[0:1],
    chunks.ChunkTypes.DESCRIPTION: VALID_DOCSTRING.split("\n")[2:4],
    chunks.ChunkTypes.TEST_STEPS: VALID_DOCSTRING.split("\n")[5:8],
    chunks.ChunkTypes.PASS_CRITERIA: VALID_DOCSTRING.split("\n")[9:12],
    chunks.ChunkTypes.FAIL_CRITERIA: VALID_DOCSTRING.split("\n")[13:16],
    chunks.ChunkTypes.REFERENCE: VALID_DOCSTRING.split("\n")[17:20],
}
