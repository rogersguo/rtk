# -*- coding: utf-8 -*-
#
#       rtk.function.Function.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
###############################################################################
Function Package Data Module
###############################################################################
"""

# Import modules for localization support.
import gettext

from pubsub import pub                          # pylint: disable=E0401

# Import other RTK modules.
from datamodels import RTKDataModel             # pylint: disable=E0401
from datamodels import RTKDataController        # pylint: disable=E0401
from dao import RTKFunction                     # pylint: disable=E0401

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

_ = gettext.gettext


class Model(RTKDataModel):
    """
    The Function data model contains the attributes and methods of a function.
    A :py:class:`rtk.function.Function` will consist of one or more Functions.
    The attributes of a Function data model are:
    """

    _tag = 'Functions'

    def __init__(self, dao):
        """
        Method to initialize a Function data model instance.
        """

        RTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.last_id = None

    def select(self, function_id):
        """
        Method to retrieve the instance of the RTKFunction data model for the
        Function ID passed.

        :param int function_id: the ID Of the Function to retrieve.
        :return: the instance of the RTKFunction class that was requested or
                 None if the requested Function ID does not exist.
        :rtype: :py:class:`rtk.dao.RTKFunction.RTKFunction`
        """

        return RTKDataModel.select(self, function_id)

    def select_all(self, revision_id):
        """
        Method to retrieve all the Functions from the RTK Program database.
        Then add each to

        :param int revision_id: the Revision ID to select the Functions for.
        :return: tree; the Tree() of RTKFunction data models.
        :rtype: :py:class:`treelib.Tree`
        """

        _session = RTKDataModel.select_all(self)

        for _function in _session.query(RTKFunction).filter(
                RTKFunction.revision_id == revision_id).all():
            # We get and then set the attributes to replace any None values
            # (NULL fields in the database) with their default value.
            _attributes = _function.get_attributes()
            _function.set_attributes(_attributes[2:])
            self.tree.create_node(_function.name, _function.function_id,
                                  parent=_function.parent_id, data=_function)

        _session.close()

        return self.tree

    def insert(self, **kwargs):
        """
        Method to add a Function to the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _function = RTKFunction()
        _function.revision_id = kwargs['revision_id']
        _function.parent_id = kwargs['parent_id']
        _error_code, _msg = RTKDataModel.insert(self, [_function, ])

        if _error_code == 0:
            self.tree.create_node(_function.name, _function.function_id,
                                  parent=0, data=_function)
            self.last_id = _function.function_id

        return _error_code, _msg

    def delete(self, function_id):
        """
        Method to remove the function associated with Function ID.

        :param int function_id: the ID of the Function to be removed.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        try:
            _function = self.tree.get_node(function_id).data
            _error_code, _msg = RTKDataModel.delete(self, _function)

            if _error_code == 0:
                self.tree.remove_node(function_id)

        except AttributeError:
            _error_code = 2005
            _msg = 'RTK ERROR: Attempted to delete non-existent Function ' \
                   'ID {0:d}.'.format(function_id)

        return _error_code, _msg

    def update(self, function_id):
        """
        Method to update the function associated with Function ID to the RTK
        Program database.

        :param int function_id: the Function ID of the Function to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _error_code, _msg = RTKDataModel.update(self, function_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RTK ERROR: Attempted to save non-existent Function ID ' \
                   '{0:d}.'.format(function_id)

        return _error_code, _msg

    def update_all(self):
        """
        Method to save all Functions to the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = 'RTK SUCCESS: Saving all Functions.'

        for _node in self.tree.all_nodes():
            try:
                _error_code, _msg = self.update(_node.data.function_id)

                # Break if something goes wrong and return.
                if _error_code != 0:
                    print 'FIXME: Handle non-zero error codes in ' \
                          'rtk.function.Function.Model.update_all().'

            except AttributeError:
                print 'FIXME: Handle AttributeError in ' \
                      'rtk.function.Function.Model.update_all().'

        return _error_code, _msg

    def calculate_reliability(self, function_id):
        """
        Method to calculate the logistics MTBF and mission MTBF.

        :param int function_id: the Function ID to calculate.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _function = self.tree.get_node(function_id).data

        _error_code = 0
        _msg = 'RTK SUCCESS: Calculating reliability metrics for Function ' \
               'ID {0:d}.'.format(_function.function_id)

        # Calculate the logistics MTBF.
        try:
            _function.mtbf_logistics = 1.0 / _function.hazard_rate_logistics
        except(ZeroDivisionError, OverflowError):
            _function.mtbf_logistics = 0.0
            _error_code = 3008
            _msg = "RTK ERROR: Zero Division or Overflow Error '" \
                   "when calculating the logistics MTBF for Function ID " \
                   "{1:d}.  Logistics hazard rate: {0:f}.".\
                   format(_function.hazard_rate_logistics,
                          _function.function_id)

        # Calculate the mission MTBF.
        try:
            _function.mtbf_mission = 1.0 / _function.hazard_rate_mission
        except(ZeroDivisionError, OverflowError):
            _function.mtbf_mission = 0.0
            _error_code = 3008
            _msg = "RTK ERROR: Zero Division or Overflow Error " \
                   "when calculating the mission MTBF for Function ID " \
                   "{1:d}.  Mission hazard rate: {0:f}.".\
                format(_function.hazard_rate_logistics, _function.function_id)

        return _error_code, _msg

    def calculate_availability(self, function_id):
        """
        Method to calculate the logistics availability and mission
        availability.

        :param int function_id: the Function ID to calculate.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _function = self.tree.get_node(function_id).data

        _error_code = 0
        _msg = 'RTK SUCCESS: Calculating availability metrics for Function ' \
               'ID {0:d}.'.format(_function.function_id)

        # Calculate logistics availability.
        try:
            _function.availability_logistics = _function.mtbf_logistics \
                                               / (_function.mtbf_logistics +
                                                  _function.mttr)
        except(ZeroDivisionError, OverflowError):
            _function.availability_logistics = 1.0
            _error_code = 3009
            _msg = "RTK ERROR: Zero Division or Overflow Error " \
                   "when calculating the mission MTBF for Function ID " \
                   "{2:d}.  Logistics MTBF: {0:f} and MTTR: {1:f}.".\
                   format(_function.mtbf_logistics, _function.mttr,
                          _function.function_id)

        # Calculate mission availability.
        try:
            _function.availability_mission = _function.mtbf_mission \
                                             / (_function.mtbf_mission +
                                                _function.mttr)
        except(ZeroDivisionError, OverflowError):
            _function.availability_mission = 1.0
            _error_code = 3009
            _msg = "RTK ERROR: Zero Division or Overflow Error " \
                   "when calculating the mission MTBF for Function ID " \
                   "{2:d}.  Mission MTBF: {0:f} and MTTR: {1:f}.".\
                   format(_function.mtbf_mission, _function.mttr,
                          _function.function_id)

        return _error_code, _msg


class Function(RTKDataController):
    """
    The Function data controller provides an interface between the Function
    data model and an RTK view model.  A single Function controller can manage
    one or more Function data models.  The attributes of a Function data
    controller are:

    :ivar last_id: the last Function ID used.  Default value = None.
    :ivar dicFunctions: Dictionary of the Function data models controlled.  Key
                        is the Function ID; value is a pointer to the Function
                        data model instance.  Default value = {}.
    :ivar dao: the :py:class:`rtk.dao.DAO` to use when communicating with the
               RTK Project database.  Default value = None.
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Method to initialize a Function data controller instance.

        :param dao: the RTK Program DAO instance to pass to the Function Data
                    Model.
        :type dao: :py:class:`rtk.dao.DAO`
        :param configuration: the Configuration instance associated with the
                              current instance of the RTK application.
        :type configuration: :py:class:`rtk.Configuration.Configuration`
        """

        RTKDataController.__init__(self, configuration, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._dtm_function = Model(dao)

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def request_select(self, function_id):
        """
        Method to request the Function Data Model to retrieve the RTKFunction
        model associated with the Function ID.

        :param int function_id: the Function ID to retrieve.
        :return: the RTKFunction model requested.
        :rtype: `:py:class:rtk.dao.DAO.RTKFunction` model
        """

        return self._dtm_function.select(function_id)

    def request_select_all(self, revision_id):
        """
        Method to retrieve the Function tree from the Function Data Model.

        :param int revision_id: the Revision ID to select the Functions for.
        :return: tree; the treelib Tree() of RTKFunction models in the
                 Function tree.
        :rtype: dict
        """

        return self._dtm_function.select_all(revision_id)

    def request_insert(self, revision_id, parent_id):
        """
        Method to request the Function Data Model to add a new Function to the
        RTK Program database.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _error_code, _msg = self._dtm_function.insert(revision_id=revision_id,
                                                      parent_id=parent_id)

        if _error_code == 0 and not self._test:
            pub.sendMessage('insertedFunction',
                            function_id=self._dtm_function.last_id,
                            parent_id=parent_id)
        else:
            _msg = _msg + '  Failed to add a new Function to the RTK Program ' \
                'database.'

        return RTKDataController.handle_results(self, _error_code, _msg, None)

    def request_delete(self, function_id):
        """
        Method to request the Function Data Model to delete a Function from the
        RTK Program database.

        :param int function_id: the Function ID to delete.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _error_code, _msg = self._dtm_function.delete(function_id)

        return RTKDataController.handle_results(self, _error_code, _msg,
                                                'deletedFunction')

    def request_update(self, function_id):
        """
        Method to request the Function Data Model save the RTKFunction
        attributes to the RTK Program database.

        :param int function_id: the ID of the function to save.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _error_code, _msg = self._dtm_function.update(function_id)

        return RTKDataController.handle_results(self, _error_code, _msg,
                                                'savedFunction')

    def request_update_all(self):
        """
        Method to request the Function Data Model to save all RTKFunction
        model attributes to the RTK Program database.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _error_code, _msg = self._dtm_function.update_all()

        return RTKDataController.handle_results(self, _error_code, _msg, None)

    def request_calculate_reliability(self, function_id):
        """
        Method to request reliability attributes be calculated for the
        Function ID passed.

        :param int function_id: the Function ID to calculate.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _error_code, \
            _msg = self._dtm_function.calculate_reliability(function_id)

        return RTKDataController.handle_results(self, _error_code, _msg,
                                                'calculatedFunction')

    def request_calculate_availability(self, function_id):
        """
        Method to request availability attributes be calculated for the
        Function ID passed.

        :param int function_id: the Function ID to calculate.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _error_code, \
            _msg = self._dtm_function.calculate_availability(function_id)

        return RTKDataController.handle_results(self, _error_code, _msg,
                                                'calculatedFunction')
