#!/usr/bin/env python -O
"""
This is the test class for testing Mica capacitor module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.unit.TestMica.py is part of The RTK Project
#
# All rights reserved.

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk", )

import unittest
from nose.plugins.attrib import attr

from hardware.component.capacitor.fixed.Mica import Button, Mica

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestMicaButtonModel(unittest.TestCase):
    """
    Class for testing the Mica Button capacitor data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Capacitor class.
        """

        self.DUT = Button()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestMicaButton) __init__ should return a Mica Button capacitor model
        """

        self.assertTrue(isinstance(self.DUT, Button))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Capacitor class was properly initialized.
        self.assertEqual(self.DUT.quality, 0)

        # Verify the Mica Button capacitor class was properly initialized.
        self.assertEqual(self.DUT._piE, [1.0, 2.0, 10.0, 5.0, 16.0, 5.0, 7.0,
                                         22.0, 28.0, 23.0, 0.5, 13.0, 34.0,
                                         610.0])
        self.assertEqual(self.DUT._piQ, [5.0, 15.0])
        self.assertEqual(self.DUT._lambdab_count, [0.018, 0.037, 0.19, 0.094,
                                                   0.31, 0.10, 0.14, 0.47,
                                                   0.60, 0.48, 0.0091, 0.25,
                                                   0.68, 11.0])
        self.assertEqual(self.DUT.subcategory, 47)
        self.assertEqual(self.DUT.specification, 0)
        self.assertEqual(self.DUT.spec_sheet, 0)
        self.assertEqual(self.DUT.reference_temperature, 358.0)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestMicaButton) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.quality = 1
        self.DUT.environment_active = 5
        self.DUT.specification = 2
        self.DUT.hazard_rate_type = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.31)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 5.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.55E-6)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_low_temp(self):
        """
        (TestMicaButton) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for the 85C specification
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.reference_temperature = 358.0
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE * piCV')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.014951137)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 5.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piCV'], 0.389560899)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 5.82437856E-8)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_high_temp(self):
        """
        (TestMicaButton) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for the 125C specification
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.reference_temperature = 423.0
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE * piCV')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.011380255)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 5.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piCV'], 0.389560899)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 4.43330228E-8)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_overflow(self):
        """
        (TestMicaButton) calculate_part should return True when an OverflowError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6
        self.DUT.reference_temperature = 0.00000001

        self.assertTrue(self.DUT.calculate_part())

    @attr(all=True, unit=True)
    def test_calculate_217_stress_zero_division(self):
        """
        (TestMicaButton) calculate_part should return True when a ZeroDivisionError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6
        self.DUT.reference_temperature = 0.0

        self.assertTrue(self.DUT.calculate_part())


class TestMicaMicaModel(unittest.TestCase):
    """
    Class for testing the Mica capacitor data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Mica Capacitor class.
        """

        self.DUT = Mica()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestMicaMica) __init__ should return a Mica capacitor model
        """

        self.assertTrue(isinstance(self.DUT, Mica))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Capacitor class was properly initialized.
        self.assertEqual(self.DUT.quality, 0)

        # Verify the Mica capacitor class was properly initialized.
        self.assertEqual(self.DUT._piE, [1.0, 2.0, 10.0, 6.0, 16.0, 5.0, 7.0,
                                         22.0, 28.0, 23.0, 0.5, 13.0, 34.0,
                                         610.0])
        self.assertEqual(self.DUT._piQ, [0.01, 0.03, 0.1, 0.3, 1.0, 1.5, 3.0,
                                         6.0, 15.0])
        self.assertEqual(self.DUT._lambdab_count, [0.0005, 0.0015, 0.0091,
                                                   0.0044, 0.014, 0.0068,
                                                   0.0095, 0.054, 0.069, 0.031,
                                                   0.00025, 0.012, 0.046,
                                                   0.45])
        self.assertEqual(self.DUT.subcategory, 46)
        self.assertEqual(self.DUT.specification, 0)
        self.assertEqual(self.DUT.spec_sheet, 0)
        self.assertEqual(self.DUT.reference_temperature, 343.0)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestMicaMica) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.quality = 1
        self.DUT.environment_active = 5
        self.DUT.specification = 2
        self.DUT.hazard_rate_type = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.014)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.01)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.4E-10)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_low_temp(self):
        """
        (TestMicaMica) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for the 70C specification
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.reference_temperature = 343.0
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE * piCV')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.002193033)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.01)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piCV'], 0.517134415)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 6.80455807E-10)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_mid1_temp(self):
        """
        (TestMicaMica) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for the 85C specification
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.reference_temperature = 358.0
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE * piCV')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.001212973)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.01)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piCV'], 0.517134415)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 3.76361032E-10)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_mid2_temp(self):
        """
        (TestMicaMica) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for the 125C specification
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.reference_temperature = 398.0
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE * piCV')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.000311013)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.01)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piCV'], 0.517134415)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 9.65013129E-11)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_high_temp(self):
        """
        (TestMicaMica) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for the 150C specification
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.reference_temperature = 423.0
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE * piCV')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.0001514)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.01)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piCV'], 0.517134415)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 4.69763836E-11)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_overflow(self):
        """
        (TestMicaMica) calculate_part should return True when an OverflowError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6
        self.DUT.reference_temperature = 0.00000001

        self.assertTrue(self.DUT.calculate_part())

    @attr(all=True, unit=True)
    def test_calculate_217_stress_zero_division(self):
        """
        (TestMicaMica) calculate_part should return True when a ZeroDivisionError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6
        self.DUT.reference_temperature = 0.0

        self.assertTrue(self.DUT.calculate_part())
