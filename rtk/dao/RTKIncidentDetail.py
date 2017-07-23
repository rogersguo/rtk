#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKIncidentDetail.py is part of The RTK Project
#
# All rights reserved.

"""
==============================
The RTKIncidentDetail Table
==============================
"""

# Import the database models.
from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

# Import other RTK modules.
try:
    import Configuration as Configuration
except ImportError:
    import rtk.Configuration as Configuration
try:
    import Utilities as Utilities
except ImportError:
    import rtk.Utilities as Utilities
try:
    from dao.RTKCommonDB import Base
except ImportError:
    from rtk.dao.RTKCommonDB import Base

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'


class RTKIncidentDetail(Base):
    """
    Class to represent the table rtk_incident_detail in the RTK Program
    database.

    This table shares a One-to-One relationship with rtk_incident.
    """

    __tablename__ = 'rtk_incident_detail'
    __table_args__ = {'extend_existing': True}

    incident_id = Column('fld_incident_id', Integer,
                         ForeignKey('rtk_incident.fld_incident_id'),
                         primary_key=True, nullable=False)
    hardware_id = Column('fld_hardware_id', Integer, default=0)

    age_at_incident = Column('fld_age_at_incident', Float, default=0.0)
    cnd_nff = Column('fld_cnd_nff', Integer, default=0)
    failure = Column('fld_failure', Integer, default=0)
    initial_installation = Column('fld_initial_installation', Integer,
                                      default=0)
    interval_censored = Column('fld_interval_censored', Integer, default=0)
    mode_type_id = Column('fld_mode_type_id', Integer, default=0)
    occ_fault = Column('fld_occ_fault', Integer, default=0)
    suspension = Column('fld_suspension', Integer, default=0)
    ttf = Column('fld_ttf', Float, default=0.0)
    use_cal_time = Column('fld_use_cal_time', Integer, default=0)
    use_op_time = Column('fld_use_op_time', Integer, default=0)

    # Define the relationships to other tables in the RTK Program database.
    incident = relationship('RTKIncident', back_populates='incident_detail')

    def get_attributes(self):
        """
        Method to retrieve the current values of the Incident Component data
        model attributes.

        :return: (incident_id, hardware_id, age_at_incident, cnd_nff, failure,
                  initial_installation, interval_censored, mode_type,
                  occ_fault, suspension, ttf, use_cal_time, use_op_time)
        :rtype: tuple
        """

        _values = (self.incident_id, self.hardware_id, self.age_at_incident,
                   self.cnd_nff, self.failure, self.initial_installation,
                   self.interval_censored, self.mode_type_id, self.occ_fault,
                   self.suspension, self.ttf, self.use_cal_time,
                   self.use_op_time)

        return _values

    def set_attributes(self, values):
        """
        Method to set the Incident Component data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_error_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKIncidentDetail {0:d} attributes.". \
               format(self.incident_id)

        try:
            self.age_at_incident = float(values[0])
            self.cnd_nff = int(values[1])
            self.failure = int(values[2])
            self.initial_installation = int(values[3])
            self.interval_censored = int(values[4])
            self.mode_type_id = int(values[5])
            self.occ_fault = int(values[6])
            self.suspension = int(values[7])
            self.ttf = float(values[8])
            self.use_op_time = int(values[9])
            self.use_cal_time = int(values[10])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKIncidentDetail.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKIncidentDetail attributes."

        return _error_code, _msg