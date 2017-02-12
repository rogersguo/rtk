#!/usr/bin/env python
"""
##########################################
Incident Component Sub-Package Data Module
##########################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.incident.component.Component.py is part of The RTK Project
#
# All rights reserved.

# Import other RTK modules.
try:
    import Utilities
except ImportError:
    import rtk.Utilities as Utilities

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "Weibullguy" Rowland'


class Model(object):                       # pylint: disable=R0902, R0904
    """
    The Incident Component data model contains the attributes and methods for
    an Incident Component. The attributes of an Incident Component model are:

    :ivar int incident_id :default value: None
    :ivar int component_id :default value: None
    :ivar float age_at_incident :default value: 0.0
    :ivar int failure :default value: False
    :ivar int suspension :default value: False
    :ivar int cnd_nff :default value: False
    :ivar int occ_fault :default value: False
    :ivar int initial_installation :default value: False
    :ivar int interval_censored :default value: False
    :ivar int use_op_time :default value: False
    :ivar int use_cal_time :default value: False
    :ivar float ttf :default value: 0.0
    :ivar int mode_type :default value: 0
    """

    def __init__(self):
        """
        Method to initialize a Incident Component data model instance.
        """

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.incident_id = None
        self.component_id = None
        self.age_at_incident = 0.0
        self.failure = 0
        self.suspension = 0
        self.cnd_nff = 0
        self.occ_fault = 0
        self.initial_installation = 0
        self.interval_censored = 0
        self.use_op_time = 0
        self.use_cal_time = 0
        self.ttf = 0.0
        self.mode_type = 0

    def set_attributes(self, values):
        """
        Method to set the Incident Component data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        try:
            self.incident_id = int(values[0])
            self.component_id = int(values[1])
            self.age_at_incident = float(values[2])
            self.failure = values[3]
            self.suspension = values[4]
            self.cnd_nff = values[5]
            self.occ_fault = values[6]
            self.initial_installation = values[7]
            self.interval_censored = values[8]
            self.use_op_time = values[9]
            self.use_cal_time = values[10]
            self.ttf = float(values[11])
            self.mode_type = int(values[12])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Incident Component data
        model attributes.

        :return: (incident_id, component_id, age_at_incident, failure,
                  suspension, cnd_nff, occ_fault, initial_installation,
                  interval_censored, use_op_time, use_cal_time, ttf, mode_type)
        :rtype: tuple
        """

        _values = (self.incident_id, self.component_id, self.age_at_incident,
                   self.failure, self.suspension, self.cnd_nff, self.occ_fault,
                   self.initial_installation, self.interval_censored,
                   self.use_op_time, self.use_cal_time, self.ttf,
                   self.mode_type)

        return _values


class Component(object):
    """
    The Incident Component data controller provides an interface between the
    Incident Component data model and an RTK view model.  A single Incident
    Component controller can manage one or more Incident Component data models.
    The attributes of an Incident Component data controller are:

    :ivar _dao: the :py:class:`rtk.dao.DAO.DAO` to use when communicating with
                the RTK Project database.
    :ivar int _last_id: the last Incident Component ID used.
    :ivar dict dicComponents: Dictionary of the Incident Component data models
                              managed.  Key is the Component ID; value is a
                              pointer to the Incident Component data model
                              instance.
    """

    def __init__(self):
        """
        Method to initialize an Incident Component data controller instance.
        """

        # Initialize private scalar attributes.
        self._dao = None
        self._last_id = None

        # Initialize public dictionary attributes.
        self.dicComponents = {}

    def request_components(self, dao, incident_id):
        """
        Method to read the RTK Project database and load the Incident
        components associated with the selected Revision.  For each Incident
        component returned:

        #. Retrieve the inputs from the RTK Project database.
        #. Create an Incident Component data model instance.
        #. Set the attributes of the data model instance from the returned
           results.
        #. Add the instance to the dictionary of Incident Components being
           managed by this controller.

        :param rtk.DAO dao: the Data Access object to use for communicating
                            with the RTK Project database.
        :param int incident_id: the Incident ID to select the updates for.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        self._dao = dao

        self.dicComponents.clear()

        _query = "SELECT t1.fld_incident_id, t1.fld_component_id, \
                         t1.fld_age_at_incident, t1.fld_failure, \
                         t1.fld_suspension, t1.fld_cnd_nff, t1.fld_occ_fault, \
                         t1.fld_initial_installation, \
                         t1.fld_interval_censored, t1.fld_use_op_time, \
                         t1.fld_use_cal_time, t1.fld_ttf, t1.fld_mode_type, \
                         t2.fld_part_number \
                  FROM rtk_incident_detail AS t1 \
                  INNER JOIN rtk_hardware AS t2 ON fld_hardware_id \
                  WHERE t2.fld_hardware_id=t1.fld_component_id \
                  AND t1.fld_incident_id={0:d}".format(incident_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=False)

        try:
            _n_components = len(_results)
        except TypeError:
            _n_components = 0

        for i in range(_n_components):
            _component = Model()
            _component.set_attributes(_results[i])
            self.dicComponents[_results[i][1]] = _component

        return(_results, _error_code)

    def add_component(self, incident_id, component_id):
        """
        Adds a new Incident Component to the RTK Program's database.

        :param int incident_id: the Incident ID to add the new Component to.
        :param int n_components: the number of components to add to the
                                 Incident.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _query = "INSERT INTO rtk_incident_detail \
                  (fld_incident_id, fld_component_id) \
                  VALUES ({0:d}, {1:d})".format(incident_id, component_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        # If the new component was added successfully to the RTK Project
        # database:
        #   1. Create a new Incident Component model instance.
        #   2. Set the attributes of the new Incident Component model
        #      instance.
        #   3. Add the new Incident Component model to the controller
        #      dictionary.
        if _results:
            _component = Model()
            _component.incident_id = incident_id
            _component.component_id = component_id
            self.dicComponents[_component.component_id] = _component

        return(_results, _error_code)

    def delete_component(self, incident_id, component_id):
        """
        Deletes an Incident Component from the selected Incident.

        :param int incident_id: the ID of the incident to delete the
                                component from.
        :param int component_id: the ID of the component to delete.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _query = "DELETE FROM rtk_incident_detail \
                  WHERE fld_incident_id={0:d} \
                  AND fld_component_id={1:d}".format(incident_id, component_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        return(_results, _error_code)

    def save_all_components(self):
        """
        Saves all Incident Component data models managed by the controller.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        for _component in self.dicComponents.values():
            (_results,
             _error_code) = self.save_component(_component.component_id)

        return False

    def save_component(self, component_id):
        """
        Method to save the Incident Component model information to the open RTK
        Program database.

        :param int component_id: the ID of the Incident Component to save.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _component = self.dicComponents[component_id]

        _query = "UPDATE rtk_incident_detail \
                  SET fld_initial_installation={2:d}, fld_failure={3:d}, \
                      fld_suspension={4:d}, fld_occ_fault={5:d}, \
                      fld_cnd_nff={6:d}, fld_interval_censored={7:d}, \
                      fld_use_op_time={8:d}, fld_use_cal_time={9:d}, \
                      fld_ttf={10:f}, fld_mode_type={11:d} \
                  WHERE fld_incident_id={0:d} \
                  AND fld_component_id={1:d}".format(
                      _component.incident_id, _component.component_id,
                      _component.initial_installation, _component.failure,
                      _component.suspension, _component.occ_fault,
                      _component.cnd_nff, _component.interval_censored,
                      _component.use_op_time, _component.use_cal_time,
                      _component.ttf, _component.mode_type)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        return(_results, _error_code)
