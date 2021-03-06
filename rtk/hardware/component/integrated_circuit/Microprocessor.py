#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.integrated_circuit.Microprocessor.py is part of
#       the RTK Project
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
##################################################################
Hardware.Component.IntegratedCircuit Package Microprocessor Module
##################################################################
"""

import gettext
import locale

try:
    import Configuration
    import Utilities
    from hardware.component.integrated_circuit.IntegratedCircuit import \
         Model as IntegratedCircuit
except ImportError:                         # pragma: no cover
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities
    from rtk.hardware.component.integrated_circuit.IntegratedCircuit import \
         Model as IntegratedCircuit

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


class Microprocessor(IntegratedCircuit):
    """
    The Microprocessor IC data model contains the attributes and methods of a
    Microprocessor IC component.  The attributes of a Microprocessor IC are:

    :cvar subcategory: default value: 4

    :ivar base_hr: default value: 0.0
    :ivar reason: default value: ""
    :ivar piE: default value: 0.0

    Hazard Rate Models:
        # MIL-HDBK-217F, section 5.1.
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _C1 = [[0.06, 0.12, 0.24, 0.48], [0.14, 0.28, 0.56, 1.12]]
    _piE = [1.0, 6.0, 12.0, 5.0, 16.0, 6.0, 8.0, 7.0, 9.0, 24.0, 0.5, 13.0,
            34.0, 610.0]
    _piQ = [0.25, 1.0, 2.0]
    _lst_lambdab_count = [[[0.028, 0.061, 0.098, 0.091, 0.13, 0.12, 0.13, 0.17,
                            0.22, 0.18, 0.028, 0.11, 0.24, 3.30],
                           [0.052, 0.110, 0.180, 0.160, 0.23, 0.21, 0.24, 0.32,
                            0.39, 0.31, 0.052, 0.20, 0.41, 5.60],
                           [0.110, 0.230, 0.360, 0.330, 0.47, 0.44, 0.49, 0.65,
                            0.81, 0.65, 0.110, 0.42, 0.86, 12.0]],
                          [[0.048, 0.089, 0.130, 0.120, 0.16, 0.16, 0.17, 0.24,
                            0.28, 0.22, 0.048, 0.15, 0.28, 3.40],
                           [0.093, 0.170, 0.240, 0.220, 0.29, 0.30, 0.32, 0.45,
                            0.52, 0.40, 0.093, 0.27, 0.50, 5.60],
                           [0.190, 0.340, 0.490, 0.450, 0.60, 0.61, 0.66, 0.90,
                            1.10, 0.82, 0.190, 0.54, 1.00, 12.0]]]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 4                         # Subcategory ID in the common DB.

    def __init__(self):
        """
        Initialize a Microprocessor IC data model instance.
        """

        super(Microprocessor, self).__init__()

        # Initialize private list attributes.
        self._lambdab_count = []

        # Initialize public scalar attributes.
        self.technology = 0
        self.package = 0
        self.n_bits = 0
        self.n_pins = 0
        self.years_production = 0.0
        self.case_temperature = 0.0
        self.C1 = 0.0
        self.C2 = 0.0
        self.piL = 0.0

    def set_attributes(self, values):
        """
        Sets the Microprocessor IC data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = IntegratedCircuit.set_attributes(self, values[:134])

        try:
            self.technology = int(values[134])
            self.package = int(values[135])
            self.n_bits = int(values[136])
            self.n_pins = int(values[137])
            self.years_production = float(values[138])
            self.case_temperature = float(values[139])
            self.C1 = float(values[140])
            self.C2 = float(values[141])
            self.piL = float(values[142])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Retrieves the current values of the Microprocessor IC data model
        attributes.

        :return: (technology, package, n_bits, n_pins, years_production,
                  case_temperature, C1, C2, piL)
        :rtype: tuple
        """

        _values = IntegratedCircuit.get_attributes(self)

        _values = _values + (self.technology, self.package, self.n_bits,
                             self.n_pins, self.years_production,
                             self.case_temperature, self.C1, self.C2, self.piL)

        return _values

    def calculate_part(self):
        """
        Calculates the hazard rate for the Microprocessor IC data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
# WARNING: Refactor calculate_part; current McCabe Complexity metric = 14.
        from math import exp

        self.hazard_rate_model = {}

        # Quality factor.
        self.piQ = self._piQ[self.quality - 1]
        self.hazard_rate_model['piQ'] = self.piQ

        if self.hazard_rate_type == 1:
            self.hazard_rate_model['equation'] = 'lambdab * piQ'
            if self.n_bits > 0 and self.n_bits < 9:
                self._lambdab_count = self._lst_lambdab_count[self.technology - 1][0]
            elif self.n_bits > 8 and self.n_bits < 17:
                self._lambdab_count = self._lst_lambdab_count[self.technology - 1][1]
            elif self.n_bits > 16 and self.n_bits < 33:
                self._lambdab_count = self._lst_lambdab_count[self.technology - 1][2]

        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = '(C1 * piT + C2 * piE) * piQ * piL'

            # Die complexity failure rate.
            if self.n_bits < 9:                             # pragma: nocover
                self.C1 = self._C1[self.technology - 1][0]
            elif self.n_bits > 8 and self.n_bits < 17:
                self.C1 = self._C1[self.technology - 1][1]
            elif self.n_bits > 16 and self.n_bits < 33:     # pragma: nocover
                self.C1 = self._C1[self.technology - 1][2]
            self.hazard_rate_model['C1'] = self.C1

            # Temperature factor.
            self.junction_temperature = self.case_temperature + \
                                        self.operating_power * \
                                        self.thermal_resistance

            self.piT = 0.1 * exp((-0.65 / 8.617E-5) *
                                 ((1.0 / (self.junction_temperature + 273.0)) -
                                  (1.0 / 296.0)))
            self.hazard_rate_model['piT'] = self.piT

            # Package failure rate.
            if self.package in [1, 2, 3]:
                _constant = [2.8E-4, 1.08]
            elif self.package == 4:         # pragma: nocover
                _constant = [9.0E-5, 1.51]
            elif self.package == 5:         # pragma: nocover
                _constant = [3.0E-5, 1.82]
            elif self.package == 6:         # pragma: nocover
                _constant = [3.0E-5, 2.01]
            else:                           # pragma: nocover
                _constant = [3.6E-4, 1.08]
            self.C2 = _constant[0] * self.n_pins**_constant[1]
            self.hazard_rate_model['C2'] = self.C2

            # Learning factor.
            self.piL = 0.01 * exp(5.35 - 0.35 * self.years_production)
            self.hazard_rate_model['piL'] = self.piL

            # Environmental correction factor.
            self.piE = self._piE[self.environment_active - 1]

        return IntegratedCircuit.calculate_part(self)
