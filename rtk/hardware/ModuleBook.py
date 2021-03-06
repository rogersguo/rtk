#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.hardware.ModuleBook.py is part of The RTK Project
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
############################
Hardware Package Module View
############################
"""

import sys

# Import modules for localization support.
import gettext
import locale

# Modules required for the GUI.
try:
    import pygtk
    pygtk.require('2.0')
except ImportError:
    sys.exit(1)
try:
    import gtk
except ImportError:
    sys.exit(1)
try:
    import gtk.glade
except ImportError:
    sys.exit(1)

# Import other RTK modules.
try:
    import Configuration
    import gui.gtk.Widgets as Widgets
except ImportError:
    import rtk.Configuration as Configuration
    import rtk.gui.gtk.Widgets as Widgets
from ListBook import ListView
from WorkBook import WorkView

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class ModuleView(object):
    """
    The Module Book view displays all the Hardware items associated with the
    RTK Project in a hierarchical list.  The attributes of a Module Book view
    are:

    :ivar _model: the :py:class:`rtk.hardware.Hardware.Model` data model that
                  is currently selected.

    :ivar _lst_col_order: list containing the order of the columns in the
                          Module View :py:class:`gtk.TreeView`.
    :ivar _workbook: the :class:`rtk.hardware.WorkBook.WorkView` associated
                     with this instance of the Module View.
    :ivar dtcBoM: the :py:class:`rtk.RTK.RTK` master data controller to use for
                  accessing the Hardware data models.
    :ivar dtcAllocation: the :py:class:`rtk.analyses.allocation.Allocation`
                          data controller to use for accessing the Allocation
                          data models.
    :ivar treeview: the :py:class:`gtk.TreeView` displaying the hierarchical
                    list of Hardware.
    """

    def __init__(self, controller, rtk_view, position):
        """
        Method to initialize the Module Book view for the Hardware package.

        :param controller: the instance of the :py:class:`rtk.RTK.RTK` master
                           data controller to use with this view.

        :param gtk.Notebook rtk_view: the gtk.Notebook() to add the Hardware
                                      view into.
        :param int position: the page position in the gtk.Notebook() to insert
                             the Hardware view.  Pass -1 to add to the end.
        """

        # Define private dictionary attributes.

        # Define private list attributes.
        self._lst_handler_id = []

        # Define private scalar attributes.
        self._model = None
        self._allocation_model = None

        # Define public dictionary attribute

        # Define public list attributes.

        # Define public scalar attributes.
        self.mdcRTK = controller

        # Create the main Hardware class treeview.
        # FIXME: Update the hardware.xml file to accomodate the prediction stuff.
        (self.treeview,
         self._lst_col_order) = Widgets.make_treeview('Hardware', 3,
                                                      Configuration.RTK_COLORS[4],
                                                      Configuration.RTK_COLORS[5])

        _selection = self.treeview.get_selection()

        self.treeview.set_tooltip_text(_(u"Displays the hierarchical list of "
                                         u"the system hardware."))

        self._lst_handler_id.append(_selection.connect('changed',
                                                       self._on_row_changed))
        self._lst_handler_id.append(
            self.treeview.connect('button_release_event',
                                  self._on_button_press))

        i = 0
        for _column in self.treeview.get_columns():
            _cell = _column.get_cell_renderers()[0]
            try:
                if _cell.get_property('editable'):
                    _cell.connect('edited', self._on_cell_edited,
                                  self._lst_col_order[i])
            except TypeError:
                pass
            i += 1

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.add(self.treeview)
        _scrollwindow.show_all()

        _icon = Configuration.ICON_DIR + '32x32/hardware.png'
        _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
        _image = gtk.Image()
        _image.set_from_pixbuf(_icon)

        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" + _(u"Hardware") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the system hardware structure "
                                  u"for the selected revision."))

        _hbox = gtk.HBox()
        _hbox.pack_start(_image)
        _hbox.pack_end(_label)
        _hbox.show_all()

        rtk_view.notebook.insert_page(_scrollwindow, tab_label=_hbox,
                                      position=position)

        # Create a List View to associate with this Module View.
        self.listbook = ListView(self)

        # Create a Work View to associate with this Module View.
        self.workbook = WorkView(self)

    def request_load_data(self):
        """
        Loads the Hardware Module Book view gtk.TreeModel() with hardware
        information.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        (_hardware,
         __) = self.mdcRTK.dtcHardwareBoM.request_bom(self.mdcRTK.revision_id)
        self.mdcRTK.dtcAllocation.request_allocation()
        self.mdcRTK.dtcHazard.request_hazard()
        self.mdcRTK.dtcSimilarItem.request_similar_item()

        # Only load the hardware associated with the selected Revision.
        _hardware = [_h for _h in _hardware
                     if _h[0] == self.mdcRTK.revision_id]
        _top_items = [_h for _h in _hardware if _h[23] == -1]

        # Load all the FMECA and PoF analyses.
        for _h in _hardware:
            self.mdcRTK.dtcFMEA.request_fmea(_h[1], None,
                                             self.mdcRTK.revision_id)
            self.mdcRTK.dtcPoF.request_pof(self.mdcRTK.project_dao, _h[1])

        # Clear the Hardware Module View gtk.TreeModel().
        _model = self.treeview.get_model()
        _model.clear()

        # Recusively load the Hardware Module View gtk.TreeModel().
        self._load_treeview(_top_items, _hardware, _model)

        # Select the first row in the gtk.TreeView().
        _row = _model.get_iter_root()
        self.treeview.expand_all()
        self.treeview.set_cursor('0', None, False)
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.treeview.get_column(0)
            self.treeview.row_activated(_path, _column)

        return False

    def _load_treeview(self, parents, hardware, model, row=None):
        """
        Method to recursively load the gtk.TreeModel().  Recursive loading is
        needed to accomodate the hierarchical structure of Hardware.

        :param list parents: the list of top-level Hardware items to load.
        :param list hardware: the complete list of Hardware to use for finding
                              the child Hardware for each parent.
        :param gtk.TreeModel model: the Hardware Module View gtk.TreeModel().
        :keyword gtk.TreeIter row: the parent gtk.TreeIter().
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _icon = Configuration.ICON_DIR + '32x32/assembly.png'
        _assembly_icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
        _icon = Configuration.ICON_DIR + '32x32/component.png'
        _component_icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
        for _hardware in parents:
            if _hardware[23] == -1:
                row = None
            if _hardware[24] == 0:
                _data = list(_hardware) + [_assembly_icon]
            elif _hardware[24] == 1:
                _data = list(_hardware) + [_component_icon]
            _piter = model.append(row, _data)
            _parent_id = _hardware[1]

            # Find the child hardware of the current parent hardware.  These
            # will be the new parent hardware to pass to this method.
            _parents = [_h for _h in hardware if _h[23] == _parent_id]
            self._load_treeview(_parents, hardware, model, _piter)

        return False

    def update(self, position, new_text):
        """
        Updates the selected row in the Module Book gtk.TreeView() with changes
        to the Hardware data model attributes.  Called by other views when the
        Hardware data model attributes are edited via their gtk.Widgets().

        :ivar int position: the ordinal position in the Module Book
                            gtk.TreeView() of the data being updated.
        :ivar new_text: the new value of the attribute to be updated.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        (_model, _row) = self.treeview.get_selection().get_selected()
        _model.set(_row, self._lst_col_order[position], new_text)

        return False

    def update_all(self):
        """
        Recursively updates each row in the Module Book gtk.TreeView() with
        changes to the Hardware data model attributes.  Primarily used to
        update the gtk.TreeView() with calculation results.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        def _update_row(model, __path, row):
            """
            Updates a single row.

            :ivar gtk.TreeModel model: the gtk.TreeModel() to update.
            :ivar gtk.TreePath __path: the gtk.TreePath() of the row to be
                                       updated.
            :ivar gtk.TreeIter row: the gtk.TreeIter() of the row to be
                                    updated.
            :return: False if successful or True if an error is encountered.
            :rtype: bool
            """

            _hardware_id = model.get_value(row, 1)
            _hardware = self.mdcRTK.dtcHardwareBoM.dicHardware[_hardware_id]

            # Update cost calculation results.
            model.set(row, self._lst_col_order[6], _hardware.cost)
            model.set(row, self._lst_col_order[7], _hardware.cost_failure)
            model.set(row, self._lst_col_order[8], _hardware.cost_hour)

            # Update maintainability calculation results.
            model.set(row, self._lst_col_order[51],
                      _hardware.availability_logistics)
            model.set(row, self._lst_col_order[52],
                      _hardware.availability_mission)
            model.set(row, self._lst_col_order[53],
                      _hardware.avail_log_variance)
            model.set(row, self._lst_col_order[54],
                      _hardware.avail_mis_variance)

            # Update reliability calculation results.
            model.set(row, self._lst_col_order[59],
                      _hardware.hazard_rate_active)
            model.set(row, self._lst_col_order[60],
                      _hardware.hazard_rate_dormant)
            model.set(row, self._lst_col_order[61],
                      _hardware.hazard_rate_logistics)
            model.set(row, self._lst_col_order[63],
                      _hardware.hazard_rate_mission)
            model.set(row, self._lst_col_order[65],
                      _hardware.hazard_rate_percent)
            model.set(row, self._lst_col_order[66],
                      _hardware.hazard_rate_software)
            model.set(row, self._lst_col_order[67],
                      _hardware.hazard_rate_specified)
            model.set(row, self._lst_col_order[69],
                      _hardware.hr_active_variance)
            model.set(row, self._lst_col_order[70],
                      _hardware.hr_dormant_variance)
            model.set(row, self._lst_col_order[71],
                      _hardware.hr_logistics_variance)
            model.set(row, self._lst_col_order[72],
                      _hardware.hr_mission_variance)
            model.set(row, self._lst_col_order[73],
                      _hardware.hr_specified_variance)
            model.set(row, self._lst_col_order[74], _hardware.mtbf_logistics)
            model.set(row, self._lst_col_order[75], _hardware.mtbf_mission)
            model.set(row, self._lst_col_order[76], _hardware.mtbf_specified)
            model.set(row, self._lst_col_order[77],
                      _hardware.mtbf_log_variance)
            model.set(row, self._lst_col_order[78],
                      _hardware.mtbf_miss_variance)
            model.set(row, self._lst_col_order[79],
                      _hardware.mtbf_spec_variance)
            model.set(row, self._lst_col_order[81],
                      _hardware.reliability_logistics)
            model.set(row, self._lst_col_order[82],
                      _hardware.reliability_mission)
            model.set(row, self._lst_col_order[83], _hardware.rel_log_variance)
            model.set(row, self._lst_col_order[84],
                      _hardware.rel_miss_variance)

            return False

        _model = self.treeview.get_model()
        _model.foreach(_update_row)

        return False

    def _on_button_press(self, treeview, event):
        """
        Callback method for handling mouse clicks on the Hardware package
        Module Book gtk.TreeView().

        :param gtk.TreeView treeview: the Hardware class gtk.TreeView().
        :param gtk.gdk.Event event: the gtk.gdk.Event() that called this method
                                    (the important attribute is which mouse
                                    button was clicked).
                                    * 1 = left
                                    * 2 = scrollwheel
                                    * 3 = right
                                    * 4 = forward
                                    * 5 = backward
                                    * 8 =
                                    * 9 =

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        if event.button == 1:
            _selection = treeview.get_selection()
            self._on_row_changed(_selection)
        elif event.button == 3:
            print "Pop-up a menu!"

        return False

    def _on_row_changed(self, selection):
        """
        Callback method to handle events for the Hardware package Module Book
        gtk.TreeView().  It is called whenever a Module Book gtk.TreeView()
        row is activated.

        :param gtk.TreeSelection selection: the Hardware class gtk.TreeView()'s
                                            gtk.TreeSelection().
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        selection.handler_block(self._lst_handler_id[0])

        (_model, _row) = selection.get_selected()
        try:
            _hardware_id = _model.get_value(_row, 1)
        except TypeError:
            _hardware_id = None

        if _hardware_id is not None:
            self._model = self.mdcRTK.dtcHardwareBoM.dicHardware[_hardware_id]

            self.workbook.load(self._model)
            self.listbook.load(_hardware_id)

        selection.handler_unblock(self._lst_handler_id[0])

        return False

    def _on_cell_edited(self, __cell, __path, new_text, index):
        """
        Callback method to handle events for the Hardware package Module Book
        gtk.CellRenderer().  It is called whenever a Module Book
        gtk.CellRenderer() is edited.

        :param gtk.CellRenderer __cell: the gtk.CellRenderer() that was edited.
        :param str __path: the path of the gtk.CellRenderer() that was edited.
        :param str new_text: the new text in the gtk.CellRenderer() that was
                             edited.
        :param int index: the position in the Hardware pacakge Module Book
                          gtk.TreeView().
        :return: false if successful and True if an error is encountered.
        :rtype: bool
        """
        # WARNING: Refactor _on_cell_edited; current McCabe Complexity metric = 24.
        if index == 2:
            self._model.alt_part_number = new_text
        elif index == 3:
            self._model.attachments = new_text
        elif index == 4:
            self._model.cage_code = new_text
        elif index == 6:
            self._model.cost = float(new_text)
        elif index == 9:
            self._model.description = new_text
        elif index == 10:
            self._model.duty_cycle = float(new_text)
        elif index == 13:
            self._model.figure_number = new_text
        elif index == 14:
            self._model.humidity = float(new_text)
        elif index == 15:
            self._model.lcn = new_text
        elif index == 18:
            self._model.mission_time = float(new_text)
        elif index == 19:
            self._model.name = new_text
        elif index == 20:
            self._model.nsn = new_text
        elif index == 22:
            self._model.page_number = new_text
        elif index == 25:
            self._model.part_number = new_text
        elif index == 26:
            self._model.quantity = int(new_text)
        elif index == 27:
            self._model.ref_des = new_text
        elif index == 30:
            self._model.remarks = new_text
        elif index == 31:
            self._model.rpm = float(new_text)
        elif index == 32:
            self._model.specification_number = new_text
        elif index == 34:
            self._model.temperature_active = float(new_text)
        elif index == 35:
            self._model.temperature_dormant = float(new_text)
        elif index == 36:
            self._model.vibration = float(new_text)
        elif index == 37:
            self._model.year_of_manufacture = int(new_text)

        self.workbook.load(self._model)

        return False
