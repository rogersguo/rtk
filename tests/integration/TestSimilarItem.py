#!/usr/bin/env python -O
"""
This is the test class for testing Similar Item module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.integration.TestSimilarItem.py is part of The RTK Project
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

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk", )

import unittest
from nose.plugins.attrib import attr

import dao.DAO as _dao
from analyses.similar_item.SimilarItem import Model, SimilarItem

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestSimilarItemController(unittest.TestCase):
    """
    Class for testing the SimilarItem data controller class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the SimilarItem class.
        """

        _database = '/tmp/tempdb.rtk'
        self._dao = _dao(_database)
        self._dao.execute("PRAGMA foreign_keys = ON", commit=False)

        self.DUT = SimilarItem()
        self.DUT.dao = self._dao

    @attr(all=True, integration=True)
    def test0_request_similar_item(self):
        """
        (TestSimilarItem) request_similar_item should return 0 on success
        """

        self.assertEqual(self.DUT.request_similar_item()[1], 0)

    @attr(all=True, integration=True)
    def test1_add_similar_item(self):
        """
        (TestSimilarItem) add_similar_item should return (True, 0) on success
        """

        self.assertEqual(self.DUT.request_similar_item()[1], 0)
        (_results,
         _error_code) = self.DUT.add_similar_item(8, 0)

        self.assertTrue(isinstance(self.DUT.dicSimilarItem[8], Model))
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test2_calculate_topic_633(self):
        """
        (TestSimilarItem) calculate should return 0 on success when performing a Topic 6.3.3 analysis
        """

        self.DUT.request_similar_item()
        self.DUT.dicSimilarItem[2].from_environment = 1
        self.DUT.dicSimilarItem[2].to_environment = 3
        self.DUT.dicSimilarItem[2].from_quality = 4
        self.DUT.dicSimilarItem[2].to_quality = 3
        self.DUT.dicSimilarItem[2].from_temperature = 42.8
        self.DUT.dicSimilarItem[2].to_temperature = 31.5

        self.assertFalse(self.DUT.calculate(2, 0.005, 1))

        self.assertEqual(self.DUT.dicSimilarItem[2].change_factor_1, 2.5)
        self.assertEqual(self.DUT.dicSimilarItem[2].change_factor_2, 0.3)
        self.assertEqual(self.DUT.dicSimilarItem[2].change_factor_3, 1.1)

        self.assertAlmostEqual(self.DUT.dicSimilarItem[2].result_1, 0.00606060)

    @attr(all=True, integration=True)
    def test3_calculate_user_defined(self):
        """
        (TestSimilarItem) calculate should return 0 on success when performing a user-defined analysis
        """

        self.DUT.request_similar_item()

        self.DUT.dicSimilarItem[2].function_1 = 'hr * pi1 * pi2 * pi3 * pi4 * pi5 * pi6'
        self.DUT.dicSimilarItem[2].function_2 = 'hr * pi4 * pi5 * pi6 * (uf1 / uf2)'

        self.DUT.dicSimilarItem[2].change_factor_1 = 0.95
        self.DUT.dicSimilarItem[2].change_factor_2 = 1.10
        self.DUT.dicSimilarItem[2].change_factor_3 = 0.85
        self.DUT.dicSimilarItem[2].change_factor_4 = 0.90
        self.DUT.dicSimilarItem[2].change_factor_5 = 1.05
        self.DUT.dicSimilarItem[2].change_factor_6 = 1.15
        self.DUT.dicSimilarItem[2].user_float_1 = 3.5
        self.DUT.dicSimilarItem[2].user_float_2 = 1.25

        self.assertFalse(self.DUT.calculate(2, 0.005, 2))

        self.assertAlmostEqual(self.DUT.dicSimilarItem[2].result_1, 0.00482652)
        self.assertAlmostEqual(self.DUT.dicSimilarItem[2].result_2, 0.01521449)

    @attr(all=True, integration=True)
    def test4_save_similar_item(self):
        """
        (TestSimilarItem) save_similar_item returns (True, 0) on success
        """

        self.DUT.request_similar_item()
        self.assertEqual(self.DUT.save_similar_item(2), (True, 0))

    @attr(all=True, integration=True)
    def test5_save_all_similar_item(self):
        """
        (TestSimilarItem) save_all_similar_item returns False on success
        """

        self.DUT.request_similar_item()
        self.assertEqual(self.DUT.save_all_similar_item(),
                         [(2, 0), (102, 0), (8, 0), (105, 0), (115, 0),
                          (88, 0)])
