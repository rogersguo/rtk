#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit.TestMicroprocessor.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
#
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, 
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, 
#    this list of conditions and the following disclaimer in the documentation 
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors 
#    may be used to endorse or promote products derived from this software 
#    without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A 
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER 
#    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
#    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, 
#    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR 
#    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF 
#    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING 
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS 
#    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
This is the test class for testing Microprocessor IC module algorithms and
models.
"""

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

from hardware.component.integrated_circuit.Microprocessor import *

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestMicroprocessorModel(unittest.TestCase):
    """
    Class for testing the Microprocessor IC data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Microprocessor IC class.
        """

        self.DUT = Microprocessor()
        
        self._base_values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                             'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                             0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN',
                             0, 'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                             'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014)
        self._stress_values = (1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0,
                               0.0, 1.0)
        self._rel_values = (0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                            0.0, 1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0,
                            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0,
                            0.0, 0)
        self._user_values = (0.0, 1.0, 2.0, 30.0, 440.0, 5, 6, 7.0, 8.0, 99.0, 10.0,
                             11, 12, 13.0, 14, 15.0, 16.0, 17.0, 18, 19.0, 0.0, 1.0, 
                             2, 3, 440.0, 50, 60, 7.0, 80.0, 90, 'Zero', 'One', 
                             'Two', 'Three', '4')
        self._comp_values = (0, 0, 0.0, 30.0, 0.0, 358.0)
        self._ic_values = (1.0, 0.05, 3.0, 4.0, 5.0, 1, "")
        
    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestMicroprocessor) __init__ should return an Microprocessor IC data model
        """

        self.assertTrue(isinstance(self.DUT, Microprocessor))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Inductor class was properly initialized.
        self.assertEqual(self.DUT.category, 1)
        self.assertEqual(self.DUT.quality, 0)
        self.assertEqual(self.DUT.base_hr, 0.0)
        self.assertEqual(self.DUT.piE, 0.0)
        self.assertEqual(self.DUT.piQ, 1.0)

        # Verify the Microprocessor IC class was properly initialized.
        self.assertEqual(self.DUT.subcategory, 4)
        self.assertEqual(self.DUT.technology, 0)
        self.assertEqual(self.DUT.package, 0)
        self.assertEqual(self.DUT.n_bits, 0)
        self.assertEqual(self.DUT.n_pins, 0)
        self.assertEqual(self.DUT.years_production, 0.0)
        self.assertEqual(self.DUT.case_temperature, 0.0)
        self.assertEqual(self.DUT.C1, 0.0)
        self.assertEqual(self.DUT.C2, 0.0)
        self.assertEqual(self.DUT.piL, 0.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestMicroprocessor) set_attributes should return a 0 error code on success
        """

        _my_values = (1, 3, 16, 8, 1.5, 75.0, 0.0025, 0.0097, 1.2)
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._ic_values + \
                  _my_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.technology, 1)
        self.assertEqual(self.DUT.package, 3)
        self.assertEqual(self.DUT.n_bits, 16)
        self.assertEqual(self.DUT.n_pins, 8)
        self.assertEqual(self.DUT.years_production, 1.5)
        self.assertEqual(self.DUT.case_temperature, 75.0)
        self.assertEqual(self.DUT.C1, 0.0025)
        self.assertEqual(self.DUT.C2, 0.0097)
        self.assertEqual(self.DUT.piL, 1.2)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestMicroprocessor) set_attributes should return a 40 error code when too few items are passed
        """

        _my_values = (1, 3, 16, 8, 1.5, 0.0025, 0.0097, 1.2)
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._ic_values + \
                  _my_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_type_error(self):
        """
        (TestMicroprocessor) set_attributes should return a 10 error code when the wrong type is passed
        """

        _my_values = (1, 3, 16, 8, 1.5, 75.0, None, 0.0097, 1.2)
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._ic_values + \
                  _my_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestMicroprocessor) get_attributes should return a tuple of attribute values
        """
        
        _my_values = (0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0)
        _values = (None, None, '', '', '', '', 0.0, 0.0, 0.0, '', 100.0, 0, 0, '', 
                   50.0, '', 1, 0, 10.0, '', '', 0, '', 0, 0, '', 1, '', 1.0, 0, '', 
                   0.0, '', 0, 30.0, 30.0, 0.0, 2014, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                   1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 
                   0.0, 0.0, 0.0, 0.0, 0.0, 1, 0.0, {}, 0.0, 0.0, 0.0, 1, 0.0, 0.0, 
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 
                   0.0, 0, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0, 0, 0, 0, 0, 0, 
                   0, 0, 0, 0], ['', '', '', '', ''], 0, 0, 0.0, 30.0, 0.0, 30.0, 
                   0.0, 0.0, 1.0, 0.0, 0.0, 0, "") + _my_values

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_attribute_sanity(self):
        """
        (TestMicroprocessor) get_attributes(set_attributes(values)) == values
        """

        _my_values = (0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0)
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._ic_values + \
                  _my_values
                  
        self.DUT.set_attributes(_values)
        _result = self.DUT.get_attributes()

        self.assertEqual(_result[:38], self._base_values)
        self.assertEqual(_result[38:50], self._stress_values)
        self.assertEqual(_result[50:86], self._rel_values)
        self.assertEqual(_result[86], list(self._user_values[:20]))
        self.assertEqual(_result[87], list(self._user_values[20:30]))
        self.assertEqual(_result[88], list(self._user_values[30:35]))
        self.assertEqual(_result[89:95], self._comp_values)
        self.assertEqual(_result[95:102], self._ic_values)
        
        self.assertEqual(_result[102:], _my_values)
        
    @attr(all=False, unit=False)
    def test_calculate_217_count(self):
        """
        (TestMicroprocessor) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1
        self.DUT.quality = 1
        self.DUT.technology = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')

    @attr(all=True, unit=True)
    def test_calculate_217_count_all(self):
        """
        (TestMicroprocessor) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.n_bits = 8
        self.test_calculate_217_count()
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.13)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 3.25E-8)

        self.DUT.n_bits = 16
        self.test_calculate_217_count()
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.23)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 5.75E-8)

        self.DUT.n_bits = 32
        self.test_calculate_217_count()
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.47)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.175E-7)

    @attr(all=True, unit=True)
    def test_calculate_217_stress(self):
        """
        (TestMicroprocessor) calculate_part should return False on success when calculating MIL-HDBK-217F parts stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1

        self.DUT.operating_power = 0.25
        self.DUT.thermal_resistance = 60.0

        self.DUT.technology = 1
        self.DUT.family = 2
        self.DUT.package = 3
        self.DUT.n_bits = 16
        self.DUT.n_pins = 18
        self.DUT.years_production = 1.5
        self.DUT.case_temperature = 35.0

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.junction_temperature, 50.0)
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         '(C1 * piT + C2 * piE) * piQ * piL')
        self.assertEqual(self.DUT.hazard_rate_model['C1'], 0.12)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['C2'], 0.0063511495)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piT'], 0.8416815)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 6.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piL'], 1.2458647)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.7112116E-8)