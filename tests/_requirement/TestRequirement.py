#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit.TestRequirement.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing Requirement module algorithms and models."""

import sys
from os.path import dirname
from datetime import date

sys.path.insert(
    0,
    dirname(dirname(dirname(__file__))) + "/rtk", )

import unittest
from nose.plugins.attrib import attr

from sqlalchemy.orm import scoped_session
from treelib import Tree
import pandas as pd

import Utilities as Utilities
from Configuration import Configuration
from datamodels import RTKDataMatrix
from requirement import dtmRequirement, dtcRequirement
from dao import DAO
from dao import RTKRequirement

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2017 Andrew "weibullguy" Rowland'


class TestRequirementDataModel(unittest.TestCase):
    """Class for testing the Requirement data model class."""

    def setUp(self):
        """Set up the test fixture for the Requirement class."""
        self.Configuration = Configuration()

        self.Configuration.RTK_BACKEND = 'sqlite'
        self.Configuration.RTK_PROG_INFO = {
            'host': 'localhost',
            'socket': 3306,
            'database': '/tmp/TestDB.rtk',
            'user': '',
            'password': ''
        }

        self.Configuration.DEBUG_LOG = \
            Utilities.create_logger("RTK.debug", 'DEBUG', '/tmp/RTK_debug.log')
        self.Configuration.USER_LOG = \
            Utilities.create_logger("RTK.user", 'INFO', '/tmp/RTK_user.log')

        # Create a data access object and connect to a test database.
        self.dao = DAO()
        _database = self.Configuration.RTK_BACKEND + ':///' + \
            self.Configuration.RTK_PROG_INFO['database']
        self.dao.db_connect(_database)

        self.dao.RTK_SESSION.configure(
            bind=self.dao.engine, autoflush=False, expire_on_commit=False)
        self.session = scoped_session(self.dao.RTK_SESSION)

        self.DUT = dtmRequirement(self.dao)

    @attr(all=True, unit=True)
    def test00_requirement_create(self):
        """(TestRequirementModel) __init__ should return a Requirement model."""
        self.assertTrue(isinstance(self.DUT, dtmRequirement))
        self.assertTrue(isinstance(self.DUT.tree, Tree))
        self.assertTrue(isinstance(self.DUT.dao, DAO))

    @attr(all=True, unit=True)
    def test01a_select_all(self):
        """(TestRequirementModel): select_all() should return a Tree() object populated with RTKRequirement instances on success."""
        _tree = self.DUT.select_all(1)

        self.assertTrue(isinstance(_tree, Tree))
        self.assertTrue(isinstance(_tree.get_node(1).data, RTKRequirement))

    @attr(all=True, unit=True)
    def test02a_select(self):
        """(TestRequirementModel): select() should return an instance of the RTKRequirement data model on success."""
        self.DUT.select_all(1)
        _requirement = self.DUT.select(1)

        self.assertTrue(isinstance(_requirement, RTKRequirement))
        self.assertEqual(_requirement.requirement_id, 1)
        self.assertEqual(_requirement.requirement_code, 'REL-0001')

    @attr(all=True, unit=True)
    def test02b_select_non_existent_id(self):
        """(TestRequirementModel): select() should return None when a non-existent Requirement ID is requested."""
        _requirement = self.DUT.select(100)

        self.assertEqual(_requirement, None)

    @attr(all=True, unit=True)
    def test03a_insert_sibling(self):
        """(TestRequirementModel): insert() should return False on success when inserting a sibling Requirement."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.insert(revision_id=1, parent_id=0)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Adding one or more items to '
                         'the RTK Program database.')
        self.assertEqual(self.DUT.last_id, 3)

    @attr(all=True, unit=True)
    def test03b_insert_child(self):
        """(TestRequirementModel): insert() should return False on success when inserting a child (derived) Requirement."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.insert(
            revision_id=1, parent_id=self.DUT.last_id)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Adding one or more items to '
                         'the RTK Program database.')
        self.assertEqual(self.DUT.last_id, 4)

    @attr(all=True, unit=True)
    def test04a_delete(self):
        """(TestRequirementModel): delete() should return a zero error code on success."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.delete(4)
        _error_code, _msg = self.DUT.delete(3)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Deleting an item from the RTK '
                         'Program database.')

    @attr(all=True, unit=True)
    def test04b_delete_non_existent_id(self):
        """(TestRequirementModel): delete() should return a non-zero error code when passed a Requirement ID that doesn't exist."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.delete(300)

        self.assertEqual(_error_code, 2005)
        self.assertEqual(_msg, '  RTK ERROR: Attempted to delete non-existent '
                         'Requirement ID 300.')

    @attr(all=True, unit=True)
    def test05a_update(self):
        """(TestRequirementModel): update() should return a zero error code on success."""
        self.DUT.select_all(1)

        _requirement = self.DUT.select(1)
        _requirement.requirement_code = 'REL-0001'

        _error_code, _msg = self.DUT.update(1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')

    @attr(all=True, unit=True)
    def test05b_update_non_existent_id(self):
        """(TestRequirementModel): update() should return a non-zero error code when passed a Requirement ID that doesn't exist."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update(100)

        self.assertEqual(_error_code, 2006)
        self.assertEqual(_msg, 'RTK ERROR: Attempted to save non-existent '
                         'Requirement ID 100.')

    @attr(all=True, unit=True)
    def test06a_update_all(self):
        """(TestRequirementModel): update_all() should return a zero error code on success."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update_all()

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')


class TestRequirementDataController(unittest.TestCase):
    """Class for testing the Requirement data controller class."""

    def setUp(self):
        """Set up the test fixture for the Requirement class."""
        self.Configuration = Configuration()

        self.Configuration.RTK_BACKEND = 'sqlite'
        self.Configuration.RTK_PROG_INFO = {
            'host': 'localhost',
            'socket': 3306,
            'database': '/tmp/TestDB.rtk',
            'user': '',
            'password': ''
        }

        self.Configuration.RTK_DEBUG_LOG = \
            Utilities.create_logger("RTK.debug", 'DEBUG',
                                    '/tmp/RTK_debug.log')
        self.Configuration.RTK_USER_LOG = \
            Utilities.create_logger("RTK.user", 'INFO',
                                    '/tmp/RTK_user.log')

        # Create a data access object and connect to a test database.
        self.dao = DAO()
        _database = self.Configuration.RTK_BACKEND + ':///' + \
            self.Configuration.RTK_PROG_INFO['database']
        self.dao.db_connect(_database)

        self.dao.RTK_SESSION.configure(
            bind=self.dao.engine, autoflush=False, expire_on_commit=False)
        self.session = scoped_session(self.dao.RTK_SESSION)

        self.DUT = dtcRequirement(self.dao, self.Configuration, test='True')

    @attr(all=True, unit=True)
    def test00_controller_create(self):
        """(TestRequirementController) __init__ should return a Requirement Data Controller."""
        self.assertTrue(isinstance(self.DUT, dtcRequirement))
        self.assertTrue(isinstance(self.DUT._dtm_data_model, dtmRequirement))
        self.assertTrue(
            isinstance(self.DUT._dmx_rqmt_hw_matrix, RTKDataMatrix))
        self.assertTrue(
            isinstance(self.DUT._dmx_rqmt_sw_matrix, RTKDataMatrix))
        self.assertTrue(
            isinstance(self.DUT._dmx_rqmt_val_matrix, RTKDataMatrix))

    @attr(all=True, unit=True)
    def test01a_request_select_all(self):
        """(TestRequirementController) request_select_all() should return a Tree of RTKRequirement models."""
        _tree = self.DUT.request_select_all(1)

        self.assertTrue(isinstance(_tree.get_node(1).data, RTKRequirement))

    @attr(all=True, unit=True)
    def test01b_request_select_all_matrix(self):
        """(TestRequirementController): select_all_matrix() should return a tuple containing the matrix, column headings, and row headings."""
        (_matrix, _column_hdrs,
         _row_hdrs) = self.DUT.request_select_all_matrix(1, 'rqrmnt_hrdwr')

        self.assertTrue(isinstance(_matrix, pd.DataFrame))
        self.assertEqual(_column_hdrs, {1: u'S1', 2: u'S1:SS1', 3: u'S1:SS2'})
        self.assertEqual(_row_hdrs, {1: u'REL-0001', 2: u'PERF-0001'})

    @attr(all=True, unit=True)
    def test02a_request_select(self):
        """(TestRequirementController) request_select() should return an RTKRequirement model."""
        self.DUT.request_select_all(1)

        _requirement = self.DUT.request_select(1)

        self.assertTrue(isinstance(_requirement, RTKRequirement))

    @attr(all=True, unit=True)
    def test02b_request_select_non_existent_id(self):
        """(TestRequirementController) request_select() should return None when requesting a Requirement that doesn't exist."""
        self.assertEqual(self.DUT.request_select(100), None)

    @attr(all=True, unit=True)
    def test03a_request_insert(self):
        """(TestRequirementController) request_insert() should return False on success."""
        self.DUT.request_select_all(1)

        self.assertFalse(self.DUT.request_insert(revision_id=1, parent_id=0))

    @attr(all=True, unit=True)
    def test03b_insert_matrix_row(self):
        """(TestRequirementController) request_insert_matrix() should return False on successfully inserting a row."""
        (_matrix, _column_hdrs,
         _row_hdrs) = self.DUT.request_select_all_matrix(1, 'rqrmnt_hrdwr')

        self.assertFalse(
            self.DUT.request_insert_matrix('rqrmnt_hrdwr', 4, 'COST-0001'))
        self.assertEqual(self.DUT._dmx_rqmt_hw_matrix.dic_row_hdrs[4],
                         'COST-0001')

    @attr(all=True, unit=True)
    def test03c_insert_matrix_duplicate_row(self):
        """(TestRequirementController) request_insert_matrix() should return True when attempting to insert a duplicate row."""
        (_matrix, _column_hdrs,
         _row_hdrs) = self.DUT.request_select_all_matrix(1, 'rqrmnt_hrdwr')

        self.assertTrue(
            self.DUT.request_insert_matrix('rqrmnt_hrdwr', 2, 'COST-0001'))

    @attr(all=True, unit=True)
    def test03d_insert_matrix_column(self):
        """(TestRequirementController) request_insert_matrix() should return False on successfully inserting a column."""
        (_matrix, _column_hdrs,
         _row_hdrs) = self.DUT.request_select_all_matrix(1, 'rqrmnt_hrdwr')

        self.assertFalse(
            self.DUT.request_insert_matrix(
                'rqrmnt_hrdwr', 4, 'S1:SS1:A1', row=False))
        self.assertEqual(self.DUT._dmx_rqmt_hw_matrix.dic_column_hdrs[4],
                         'S1:SS1:A1')

    @attr(all=True, unit=True)
    def test04a_request_delete(self):
        """(TestRequirementController) request_delete() should return False on success."""
        self.DUT.request_select_all(1)
        self.DUT.request_insert(revision_id=1, parent_id=0)

        self.assertFalse(self.DUT.request_delete(3))

    @attr(all=True, unit=True)
    def test04b_request_delete_non_existent_id(self):
        """(TestRequirementController) request_delete() should return True when attempting to delete a non-existent Requirement."""
        self.DUT.request_select_all(1)

        self.assertTrue(self.DUT.request_delete(100))

    @attr(all=True, unit=True)
    def test04c_request_delete_matrix_row(self):
        """(TestRequirementController) request_delete_matrix() should return False on successfully deleting a row."""
        self.DUT.request_select_all_matrix(1, 'rqrmnt_hrdwr')
        self.DUT.request_insert_matrix('rqrmnt_hrdwr', 4, 'COST-0001')

        self.assertFalse(self.DUT.request_delete_matrix('rqrmnt_hrdwr', 4))

    @attr(all=True, unit=True)
    def test04d_request_delete_matrix_non_existent_row(self):
        """(TestRequirementController) request_delete_matrix() should return True when attempting to delete a non-existent row."""
        self.DUT.request_select_all_matrix(1, 'rqrmnt_hrdwr')

        self.assertTrue(self.DUT.request_delete_matrix('rqrmnt_hrdwr', 4))

    @attr(all=True, unit=True)
    def test04e_request_delete_matrix_column(self):
        """(TestRequirementController) request_delete_matrix() should return False on successfully deleting a column."""
        self.DUT.request_select_all_matrix(1, 'rqrmnt_hrdwr')
        self.DUT.request_insert_matrix(
            'rqrmnt_hrdwr', 4, 'S1:SS1:A1', row=False)

        self.assertFalse(
            self.DUT.request_delete_matrix('rqrmnt_hrdwr', 4, row=False))

    @attr(all=True, unit=True)
    def test05a_request_update(self):
        """(TestRequirementController) request_update() should return False on success."""
        self.DUT.request_select_all(1)

        self.assertFalse(self.DUT.request_update(1))

    @attr(all=True, unit=True)
    def test05b_request_update_non_existent_id(self):
        """(TestRequirementController) request_update() should return True when attempting to save a non-existent Requirement."""
        self.DUT.request_select_all(1)

        self.assertTrue(self.DUT.request_update(100))

    @attr(all=True, unit=True)
    def test05c_request_update_matrix(self):
        """(TestRequirementController) request_update_matrix() should return False on success."""
        self.DUT.request_select_all_matrix(1, 'rqrmnt_hrdwr')

        self.assertFalse(self.DUT.request_update_matrix(1, 'rqrmnt_hrdwr'))

    @attr(all=True, unit=True)
    def test05d_request_update_non_existent_matrix(self):
        """(TestRequirementController) request_update_matrix() should return True when attempting to update a non-existent matrix."""
        self.DUT.request_select_all_matrix(1, 'rqrmnt_hrdwr')

        self.assertTrue(self.DUT.request_update_matrix(1, 'rqrmnt_rqrmnt'))

    @attr(all=True, unit=True)
    def test06a_request_update_all(self):
        """(TestRequirementController) request_update_all() should return False on success."""
        self.DUT.request_select_all(1)

        self.assertFalse(self.DUT.request_update_all())

    @attr(all=True, unit=True)
    def test07a_request_get_attributes(self):
        """(TestRequirementController) request_get_attributes() should return a dict of {attribute name:attribute value} pairs."""
        self.DUT.request_select_all(1)

        _attributes = self.DUT.request_get_attributes(1)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(_attributes['requirement_code'], 'REL-0001')

    @attr(all=True, unit=True)
    def test07b_request_set_attributes(self):
        """(TestRequirementController) request_set_attributes() should return a zero error code on success."""
        self.DUT.request_select_all(1)

        _attributes = {
        'owner': u'',
        'priority': 0,
        'parent_id': 0,
        'requirement_code': 'REL-0001',
        'q_complete_4': 0,
        'requirement_type': u'',
        'q_complete_5': 0,
        'validated_date': date.today(),
        'revision_id': 1,
        'requirement_id': 1,
        'q_consistent_8': 0,
        'q_consistent_7': 0,
        'q_consistent_6': 0,
        'q_consistent_5': 0,
        'q_consistent_4': 0,
        'q_consistent_3': 0,
        'q_consistent_2': 0,
        'q_consistent_1': 0,
        'q_clarity_3': 0,
        'specification': u'',
        'q_complete_0': 0,
        'q_complete_1': 0,
        'q_complete_2': 0,
        'q_complete_3': 0,
        'page_number': u'',
        'figure_number': u'',
        'q_complete_6': 0,
        'q_complete_7': 0,
        'q_complete_8': 0,
        'q_complete_9': 0,
        'q_consistent_0': 0,
        'q_clarity_6': 0,
        'q_clarity_7': 0,
        'q_clarity_4': 0,
        'q_clarity_5': 0,
        'q_clarity_2': 0,
        'description': 'REL-0001',
        'q_clarity_0': 0,
        'q_clarity_1': 0,
        'q_verifiable_4': 0,
        'derived': 0,
        'q_verifiable_0': 0,
        'q_verifiable_1': 0,
        'q_clarity_8': 0,
        'q_verifiable_3': 0,
        'q_verifiable_2': 0,
        'validated': 0,
        'q_verifiable_5': 0
    }

        _error_code, _msg = self.DUT.request_set_attributes(1, _attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating RTKRequirement 1 attributes.')

    @attr(all=True, unit=True)
    def test07c_request_last_id(self):
        """(TestRequirementController) request_last_id() should return the last Requirement ID used in the RTK Program database."""
        self.DUT.request_select_all(1)

        _last_id = self.DUT.request_last_id()

        self.assertEqual(_last_id, 4)
