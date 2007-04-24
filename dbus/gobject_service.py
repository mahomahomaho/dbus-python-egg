"""Support code for implementing D-Bus services via GObjects."""

# Copyright (C) 2007 Collabora Ltd. <http://www.collabora.co.uk/>
#
# Licensed under the Academic Free License version 2.1
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Library General Public License as published by
# the Free Software Foundation; either version 2.1 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import gobject
import dbus.service

class ExportedGObjectType(dbus.service.InterfaceType, gobject.GObjectMeta):
    """A metaclass which inherits from both GObjectMeta and
    `dbus.service.InterfaceType`. Used as the metaclass for `ExportedGObject`.
    """

class ExportedGObject(dbus.service.Object, gobject.GObject):
    """A GObject which is exported on the D-Bus.

    Because GObject and `dbus.service.Object` both have custom metaclasses,
    the naive approach using simple multiple inheritance won't work. This
    class has `ExportedGObjectType` as its metaclass, which is sufficient
    to make it work correctly.
    """
    __metaclass__ = ExportedGObjectType