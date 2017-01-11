##############################################################################
#
#    `Module Auto Install PIP Dependencies` for Odoo 8
#    Copyright (C) 2016 Xpansa Group (<http://xpansa.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
# -*- coding: utf-8 -*-
from __future__ import absolute_import
import unittest2

import openerp
from openerp import SUPERUSER_ID
import common

from .utils import current_freeze

ADMIN_USER_ID = common.ADMIN_USER_ID

reg_manager = openerp.modules.registry.RegistryManager


def registry(model):
    return reg_manager.get(common.get_db_name())[model]


def cursor():
    return reg_manager.get(common.get_db_name()).cursor()


def get_module(module_name):
    registry = reg_manager.get(common.get_db_name())
    return registry.get(module_name)


def reload_registry():
    openerp.modules.registry.RegistryManager.new(
        common.get_db_name(), update_module=True)


def search_registry(model_name, domain):
    cr = cursor()
    model = registry(model_name)
    record_ids = model.search(cr, SUPERUSER_ID, domain, {})
    cr.close()
    return record_ids


def install_module(module_name):
    ir_module_module = registry('ir.module.module')
    cr = cursor()
    module_ids = ir_module_module.search(
        cr, SUPERUSER_ID,
        [('name', '=', module_name)], {})
    assert len(module_ids) == 1
    ir_module_module.button_install(cr, SUPERUSER_ID, module_ids, {})
    cr.commit()
    cr.close()
    reload_registry()


def uninstall_module(module_name):
    ir_module_module = registry('ir.module.module')
    cr = cursor()
    module_ids = ir_module_module.search(
        cr, SUPERUSER_ID,
        [('name', '=', module_name)], {})
    assert len(module_ids) == 1
    ir_module_module.button_uninstall(cr, SUPERUSER_ID, module_ids, {})
    cr.commit()
    cr.close()
    reload_registry()


def in_pip_freeze(package_name):
    # TODO: need use specific version of package
    return package_name in current_freeze


class test_auto_install_pip_requirements(unittest2.TestCase):
    """
    Test the install/uninstall of a test module. The module is available in
    `openerp.tests` which should be present in the addons-path.
    """

    def test_01_install(self):
        """ Check a few things showing the module is installed. """
        install_module('test_auto_install_pip_requirements')
        assert get_module('test_auto_install_pip_requirements.model')

        assert search_registry(
            'ir.model.fields',
            [('model', '=', 'test_auto_install_pip_requirements.model')])

        assert(in_pip_freeze('sampleproject'))

    # TODO: after implement button_install_cancel for module
    # def test_02_uninstall(self):
    #     """ Check a few things showing the module is uninstalled. """
    #     uninstall_module('test_auto_install_pip_requirements')
    #     assert not get_module('test_auto_install_pip_requirements.model')

    #     assert not search_registry(
    #         'ir.model.fields',
    #         [('model', '=', 'test_auto_install_pip_requirements.model')])


if __name__ == '__main__':
    unittest2.main()
