#!/usr/bin/env python
"""
###################################################################
Hardware.Component.Switch.Sensitive Switch Package Sensitive Module
###################################################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.switch.Sensitive.py is part of the RTK Project
#
# All rights reserved.

import gettext
import locale

try:
    import Configuration
    import Utilities
    from hardware.component.switch.Switch import Model as Switch
except ImportError:                         # pragma: no cover
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities
    from rtk.hardware.component.switch.Switch import Model as Switch

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Sensitive(Switch):
    """
    The Sensitive Switch data model contains the attributes and methods of a
    Sensitive Switch component.  The attributes of a Sensitive Switch are:

    :cvar int subcategory: Switch subcategory.

    :ivar int load_type: the MIL-HDBK-217FN2 load type input.
    :ivar int n_contacts: the MIL-HDBK-217FN2 number of active contacts input.
    :ivar float cycles_per_hour: the MIL-HDBK-217FN2 cycles per hour input.
    :ivar float actuation_differential: the MIL-HDBK-217FN2 actuation
                                        differential (inches) input.
    :ivar float piCYC: the MIL-HDBK-217FN2 switch cycle factor.
    :ivar float piL: the MIL-HDBK-217FN2 load type factor.

    Covers specification MIL-S-8805.

    Hazard Rate Models:
        # MIL-HDBK-217FN2, section 14.2.
    """

    # MIL-HDBK-217FN2 hazard rate calculation variables.

    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_piE = [1.0, 3.0, 18.0, 8.0, 29.0, 10.0, 18.0, 13.0, 22.0, 46.0, 0.5,
                25.0, 67.0, 1200.0]
    _lst_piQ_count = [1.0, 20.0]
    _lst_lambdab_count = [0.15, 0.44, 2.7, 1.2, 4.3, 1.5, 2.7, 1.9, 3.3, 6.8,
                          0.74, 3.7, 9.9, 180.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 68

    def __init__(self):
        """
        Method to initialize a Sensitive Switch data model instance.
        """

        super(Sensitive, self).__init__()

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.load_type = 0
        self.n_contacts = 0                 # Number of active contacts
        self.cycles_per_hour = 0.0
        self.actuation_differential = 0.0
        self.piCYC = 0.0
        self.piL = 0.0

    def set_attributes(self, values):
        """
        Method to set the Sensitive Switch data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Switch.set_attributes(self, values)

        try:
            self.load_type = int(values[117])
            self.n_contacts = int(values[118])
            self.cycles_per_hour = float(values[99])
            self.actuation_differential = float(values[100])
            self.piCYC = float(values[101])
            self.piL = float(values[102])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Sensitive Switch data
        model attributes.

        :return: (load_type, cycles_per_hour, actuation_differential, piCYC,
                  piL)
        :rtype: tuple
        """

        _values = Switch.get_attributes(self)

        _values = _values + (self.load_type, self.n_contacts,
                             self.cycles_per_hour, self.actuation_differential,
                             self.piCYC, self.piL)

        return _values

    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Sensitive Switch data
        model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
# WARNING: Refactor calculate_part; current McCabe Complexity metric = 13.
        from math import exp

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piCYC * piL * piE'

            # Set the base hazard rate for the model.
            if self.quality == 1:       # MIL-SPEC
                if self.actuation_differential > 0.002:
                    self.base_hr = 0.1 + 0.00045 * self.n_contacts
                else:
                    self.base_hr = 0.1 + 0.0009 * self.n_contacts
            else:
                if self.actuation_differential > 0.002:
                    self.base_hr = 0.1 + 0.23 * self.n_contacts
                else:
                    self.base_hr = 0.1 + 0.63 * self.n_contacts
            self.hazard_rate_model['lambdab'] = self.base_hr

            # Set the cycling factor for the model.
            if self.cycles_per_hour <= 1.0:
                self.piCYC = 1.0
            else:
                self.piCYC = float(self.cycles_per_hour)
            self.hazard_rate_model['piCYC'] = self.piCYC

            # Set the load stress factor for the model.
            _stress = self.operating_current / self.rated_current
            if self.load_type == 1:         # Resistive
                self.piL = exp((_stress / 0.8)**2.0)
            elif self.load_type == 2:       # Inductive
                self.piL = exp((_stress / 0.4)**2.0)
            elif self.load_type == 3:       # Lamp
                self.piL = exp((_stress / 0.2)**2.0)
            self.hazard_rate_model['piL'] = self.piL

        return Switch.calculate_part(self)