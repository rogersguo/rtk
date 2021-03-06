#!/usr/bin/env python
"""
############################
Software Package Unit Module
############################
"""

# -*- coding: utf-8 -*-
#
#       rtk.software.Unit.py is part of The RTK Project
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

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import Configuration
    from software.Software import Model as Software
except ImportError:                         # pragma: no cover
    import rtk.Configuration as Configuration
    from rtk.software.Software import Model as Software

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Model(Software):                      # pylint: disable=R0902

    """
    The Unit data model contains the attributes and methods of a software Unit
    item.
    """

    def __init__(self):
        """
        Method to initialize a Unit data model instance.
        """

        super(Model, self).__init__()

        self.level_id = 3
        self.sm = 1.0

    def calculate_complexity_risk(self):
        """
        Method to calculate Software risk due to the software complexity.

        For software complexity risk (SX), this method uses the results of
        RL-TR-92-52, Worksheet 9D or 10D to determine the relative risk level.
        The risk is based on the number of software units in a software module
        and the complexity of each unit.

        sx = # of conditional branching statements +
             # of unconditional branching statements + 1

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Software complexity defaults to 1 since cb and ncb default to 0.
        self.sx = self.cb + self.ncb + 1

        return False

    def calculate_modularity_risk(self):
        """
        Method to calculate Software risk due to the software complexity.

        For software modularity risk (SM), this method uses the results of
        RL-TR-92-52, Worksheet 9D to determine the relative risk level.  The
        risk is based on the number of software units in a software module and
        the SLOC in each unit.

        SM = 1.0

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.sm = 1.0

        return False


class Unit(object):
    """
    The Unit data controller provides an interface between the Unit data model
    and an RTK view model.  A single Unit controller can manage one or more
    Unit data models.
    """

    def __init__(self):
        """
        Method to initialize a Unit data controller instance.
        """

        pass
