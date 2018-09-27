# Copyright (c) 2018 Ultimaker B.V.
# Cura is released under the terms of the LGPLv3 or higher.

import configparser #To parse the resulting config files.
import pytest #To register tests with.

import VersionUpgrade34to40 #The module we're testing.

##  Creates an instance of the upgrader to test with.
@pytest.fixture
def upgrader():
    return VersionUpgrade34to40.VersionUpgrade34to40()

test_upgrade_version_nr_data = [
    ("Empty config file",
    """[general]
    version = 5
    [metadata]
    setting_version = 4
"""
    )
]

##  Tests whether the version numbers are updated.
@pytest.mark.parametrize("test_name, file_data", test_upgrade_version_nr_data)
def test_upgradeVersionNr(test_name, file_data, upgrader):
    #Perform the upgrade.
    _, upgraded_instances = upgrader.upgradePreferences(file_data, "<string>")
    upgraded_instance = upgraded_instances[0]
    parser = configparser.ConfigParser(interpolation = None)
    parser.read_string(upgraded_instance)

    #Check the new version.
    assert parser["general"]["version"] == "6"
    assert parser["metadata"]["setting_version"] == "5"