"""Test availability of required packages."""

import unittest
from pathlib import Path

import pkg_resources

#_REQUIREMENTS_PATH = Path(__file__).parent.with_name("requirements.txt")
_REQUIREMENTS_PATH = Path(__file__).with_name("requirements.txt")


class TestRequirements(unittest.TestCase):
    """Test availability of required packages."""

    def test_requirements(self):
        errorlevel = 0
        """Test that each required package is available."""
        # Ref: https://stackoverflow.com/a/45474387/
        requirements = pkg_resources.parse_requirements(_REQUIREMENTS_PATH.open())
        for requirement in requirements:
            requirement = str(requirement)
            print (f"checking {requirement} ... ", end="")
            try:
                with self.subTest(requirement=requirement):
                    pkg_resources.require(requirement)
            except Exception as e:
                print ("FAILED!" + str(e) )
                errorlevel = 1
            else:
                print ("OK!") 
        return errorlevel            


if __name__ == "__main__": 
    tr = TestRequirements()
    errorlevel = tr.test_requirements()
    exit(errorlevel)
