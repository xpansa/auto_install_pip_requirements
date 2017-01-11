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
from openerp import api, models, modules
from .utils import install_pip_requirements, get_req_file


class Module(models.Model):
    _name = 'ir.module.module'
    _inherit = 'ir.module.module'

    @api.multi
    def install_pip_dependencies(self):
        for module in self:
            mod_path = modules.get_module_path(module.name)
            req_file = get_req_file(mod_path)
            if req_file:
                install_pip_requirements(req_file)
        return True

    @api.multi
    def button_immediate_install(self):
        self.install_pip_dependencies()
        return super(Module, self).button_immediate_install()

    @api.multi
    def button_immediate_upgrade(self):
        self.install_pip_dependencies()
        return super(Module, self).button_immediate_upgrade()

    # TODO: need implement uninstall pip dependencies here
    # @api.multi
    # def button_install_cancel(self):
    #     self.uninstall_pip_dependencies()
    #     return super(Module, self).button_install_cancel()
