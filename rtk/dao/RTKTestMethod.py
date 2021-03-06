# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKTestMethod.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKTestMethod Table
===============================================================================
"""
# pylint: disable=E0401
from sqlalchemy import BLOB, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship               # pylint: disable=E0401

# Import other RTK modules.
from Utilities import error_handler, none_to_default  # pylint: disable=E0401
from dao.RTKCommonDB import RTK_BASE                  # pylint: disable=E0401


class RTKTestMethod(RTK_BASE):
    """
    Class to represent the table rtk_test_method in the RTK Program database.

    This table shared a Many-to-One relationship with rtk_op_stress.
    """

    __tablename__ = 'rtk_test_method'
    __table_args__ = {'extend_existing': True}

    stress_id = Column('fld_stress_id', Integer,
                       ForeignKey('rtk_op_stress.fld_stress_id'),
                       nullable=False)
    test_id = Column('fld_test_id', Integer, primary_key=True,
                     autoincrement=True, nullable=False)

    description = Column('fld_description', String(512), default='')
    boundary_conditions = Column('fld_boundary_conditions', String(512),
                                 default='')
    remarks = Column('fld_remarks', BLOB, default='')

    # Define the relationships to other tables in the RTK Program database.
    op_stress = relationship('RTKOpStress', back_populates='test_method')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKTestMethod data model
        attributes.

        :return: (stress_id, test_id, description, boundary_conditions,
                  remarks)
        :rtype: tuple
        """

        _attributes = (self.stress_id, self.test_id, self.description,
                       self.boundary_conditions, self.remarks)

        return _attributes

    def set_attributes(self, attributes):
        """
        Method to set the RTKTestMethod data model attributes.

        :param tuple attributes: values to assign to instance attributes.
        :return: (_error_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKTestMethod {0:d} attributes.". \
               format(self.test_id)

        try:
            self.description = str(none_to_default(attributes[0], ''))
            self.boundary_conditions = str(none_to_default(attributes[1], ''))
            self.remarks = str(none_to_default(attributes[2], ''))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKTestMethod.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKTestMethod attributes."

        return _error_code, _msg
