# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKModel.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKModel Table
===============================================================================
"""

from sqlalchemy import Column, Integer, String        # pylint: disable=E0401

# Import other RTK modules.
from Utilities import error_handler, none_to_default  # pylint: disable=E0401
from dao.RTKCommonDB import RTK_BASE                  # pylint: disable=E0401


class RTKModel(RTK_BASE):
    """
    Class to represent the table rtk_model in the RTK Common database.
    """

    __tablename__ = 'rtk_model'
    __table_args__ = {'extend_existing': True}

    model_id = Column('fld_model_id', Integer, primary_key=True,
                      autoincrement=True, nullable=False)
    description = Column('fld_description', String(512),
                         default='Model Description')
    model_type = Column('fld_type', Integer, default='unknown')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKModel data model
        attributes.

        :return: (model_id, description, model_type)
        :rtype: tuple
        """

        _values = (self.model_id, self.description, self.model_type)

        return _values

    def set_attributes(self, attributes):
        """
        Method to set the current values of the RTKModel data model
        attributes.

        :param tuple attributes: tuple containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKModel {0:d} attributes.". \
            format(self.model_id)

        try:
            self.description = str(none_to_default(attributes[0],
                                                   'Model Description'))
            self.model_type = str(none_to_default(attributes[1], 'unkown'))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKModel.set_attributes()."
        except TypeError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKModel attributes."

        return _error_code, _msg
