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
import logging
from os.path import isdir as os_path_isdir
from os import listdir as os_listdir
from os.path import join as os_path_join
import pip
from pip.operations import freeze
from pip.req import parse_requirements


_logger = logging.getLogger(__name__)

REQS_FILES = ['requirements.txt', 'reqs.txt']


def current_freeze():
    '''Getting current `pip freeze` packages in dict'''
    return {
        dist.project_name: dist.version
        for dist in freeze.get_installed_distributions()
    }


def install(package):
    '''Install package via pip programmatically'''
    # TODO: need add support package.options
    command = ['install', '--user']
    install_command = command[:]
    if package.req:
        install_command += [str(package.req)]
    elif package.link:
        install_command += [str(package.link)]
    else:
        pass
    if install_command != command:
        pip.main(install_command)


def install_pip_requirements(req_file):
    '''Install dependencies from requirements `req_file`'''
    for item in parse_requirements(req_file, session='somesession'):
        if isinstance(item, pip.req.InstallRequirement):
            _logger.info('required package: {}'.format(item.name))

            if item.req is not None and len(str(item.req.specifier)) > 0:
                _logger.info('  {}'.format(str(item.req.specifier)))

            if item.link is not None:
                _logger.info('  from: {}'.format(item.link.url))
                _logger.info('  filename: {}'.format(item.link.filename))
                _logger.info('  egg: {}'.format(item.link.egg_fragment))

            if len(item.options) > 0:
                for opt_type, opts in item.options.iteritems():
                    _logger.info('  {}:'.format(opt_type))
                    if isinstance(opts, list):
                        for opt in opts:
                            _logger.info('    {}'.format(opt))
                    elif isinstance(opts, dict):
                        for k, v in opts.iteritems():
                            _logger.info('    {}: {}'.format(k, v))
            install(item)


def get_req_file(path):
    '''Return `requirements.txt` or `reqs.txt` file if exists'''
    req_file = False
    if os_path_isdir(path):
        files = os_listdir(path)
        filtered = [x for x in files if x in REQS_FILES]
        if filtered:
            req_file = os_path_join(
                path, next(x for x in filtered)
            )
        else:
            req_file = False
    return req_file
