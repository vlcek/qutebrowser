# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

# Copyright 2015-2017 Florian Bruhin (The Compiler) <mail@qutebrowser.org>
#
# This file is part of qutebrowser.
#
# qutebrowser is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# qutebrowser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with qutebrowser.  If not, see <http://www.gnu.org/licenses/>.

import pytest

import pytest_bdd as bdd

from PyQt5.QtCore import PYQT_VERSION


bdd.scenarios('yankpaste.feature')


@pytest.fixture(autouse=True)
def init_fake_clipboard(quteproc):
    """Make sure the fake clipboard will be used."""
    quteproc.send_cmd(':debug-set-fake-clipboard')


@bdd.when(bdd.parsers.parse('I set the text field to "{value}"'))
def set_text_field(request, quteproc, value):
    if request.config.webengine and PYQT_VERSION >= 0x50700:
        cmd = ":jseval --world=0 set_text('{}')".format(value)
    else:
        cmd = ":jseval set_text('{}')".format(value)
    quteproc.send_cmd(cmd)
    quteproc.wait_for_js('textarea set to: ' + value)
