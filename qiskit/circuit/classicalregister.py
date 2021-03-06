# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2017.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
Classical register reference object.
"""
import itertools
from warnings import warn
import inspect

from qiskit.exceptions import QiskitError
from .register import Register
from .bit import Bit


class Clbit(Bit):
    """Implement a classical bit."""

    def __init__(self, register, index):
        if isinstance(register, ClassicalRegister):
            super().__init__(register, index)
        else:
            raise QiskitError('Clbit needs a ClassicalRegister and %s was provided' %
                              type(register).__name__)

    @property
    def __class__(self):
        # This is for supporting isinstance(cr[0], Clbit)
        # It should be removed after 0.9
        code_context = inspect.getouterframes(inspect.currentframe(), 2)[1].code_context
        for context in code_context:
            if 'tuple' in context:
                warn('Bit-as-tuple is deprecated. Replace isinstance(cr[0], tuple) for '
                     'isinstance(cr[0], Clbit).', DeprecationWarning, stacklevel=2)
                return tuple
        return Clbit


class ClassicalRegister(Register):
    """Implement a classical register."""

    # Counter for the number of instances in this class.
    instances_counter = itertools.count()
    # Prefix to use for auto naming.
    prefix = 'c'
    bit_type = Clbit

    def qasm(self):
        """Return OPENQASM string for this register."""
        return "creg %s[%d];" % (self.name, self.size)
