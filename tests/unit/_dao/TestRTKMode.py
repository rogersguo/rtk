#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKMode.py is part of The RTK Project

#
# All rights reserved.

"""
This is the test class for testing the RTKMode module algorithms and
models.
"""

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk")

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKMode import RTKMode

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKMode(unittest.TestCase):
    """
    Class for testing the RTKMode class.
    """

    _attributes = (1, 1, 1, 0, 'Test Failure Mode', '', '', '', '', '', 0.0,
                   '', '', 'Default Mission', '', 0.0, 0.0, 0.0, '', 0.0, '',
                   '', '', '', '', '', 0, 0)

    def setUp(self):
        """
        Sets up the test fixture for the RTKMode class.
        """

        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKMode).first()
        self.DUT.description = self._attributes[4]

        session.commit()

    @attr(all=True, unit=True)
    def test00_rtkmode_create(self):
        """
        ($f) DUT should create an RTKMode model.
        """

        self.assertTrue(isinstance(self.DUT, RTKMode))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_mode')
        self.assertEqual(self.DUT.function_id, 1)
        self.assertEqual(self.DUT.hardware_id, 1)
        self.assertEqual(self.DUT.mode_id, 1)
        self.assertEqual(self.DUT.critical_item, 0)
        self.assertEqual(self.DUT.description, 'Test Failure Mode')
        self.assertEqual(self.DUT.design_provisions, '')
        self.assertEqual(self.DUT.detection_method, '')
        self.assertEqual(self.DUT.effect_end, '')
        self.assertEqual(self.DUT.effect_local, '')
        self.assertEqual(self.DUT.effect_next, '')
        self.assertEqual(self.DUT.effect_probability, 0.0)
        self.assertEqual(self.DUT.hazard_rate_source, '')
        self.assertEqual(self.DUT.isolation_method, '')
        self.assertEqual(self.DUT.mission, 'Default Mission')
        self.assertEqual(self.DUT.mission_phase, '')
        self.assertEqual(self.DUT.mode_criticality, 0.0)
        self.assertEqual(self.DUT.mode_hazard_rate, 0.0)
        self.assertEqual(self.DUT.mode_op_time, 0.0)
        self.assertEqual(self.DUT.mode_probability, '')
        self.assertEqual(self.DUT.mode_ratio, 0.0)
        self.assertEqual(self.DUT.operator_actions, '')
        self.assertEqual(self.DUT.other_indications, '')
        self.assertEqual(self.DUT.remarks, '')
        self.assertEqual(self.DUT.rpn_severity, '')
        self.assertEqual(self.DUT.rpn_severity_new, '')
        self.assertEqual(self.DUT.severity_class, '')
        self.assertEqual(self.DUT.single_point, 0)
        self.assertEqual(self.DUT.type_id, 0)

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """
        (TestRTKMode) get_attributes should return a tuple of attribute values.
        """

        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRTKMode) set_attributes should return a zero error code on success
        """

        _attributes = (0, 'Test Failure Mode', '', '', '', '', '', 0.0, '', '',
                       'Default Mission', '', 0.0, 0.0, 0.0, '', 0.0, '', '',
                       '', '', '', '', 0, 0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKMode {0:d} " \
                               "attributes.".format(self.DUT.hardware_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_wrong_type(self):
        """
        (TestRTKMode) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = (0, 'Test Failure Mode', '', '', '', '', '', 0.0, '', '',
                       'Default Mission', '', 'zero.zero', 0.0, 0.0, '', 0.0,
                       '', '', '', '', '', '', 0, 0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RTK ERROR: Incorrect data type when " \
                               "converting one or more RTKMode " \
                               "attributes.")

    @attr(all=True, unit=True)
    def test02c_set_attributes_too_few_passed(self):
        """
        (TestRTKMode) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = (0, 'Test Failure Mode', '', '', '', '', '', 0.0, '', '',
                       'Default Mission', '', 0.0, 0.0, 0.0, '', 0.0, '', '',
                       '', '', '', '', 0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKMode.set_attributes().")