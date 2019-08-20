# Copyright 2018 Xanadu Quantum Technologies Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Unit tests for the Simulator plugin
"""
import pytest

import pennylane as qml
from pennylane import numpy as np
import pennylane_cirq
import cirq

# TODO:
# * Test the feature that qubits can be given + exception
# * Test all gate adjustments before measurements
# * Test that more samples are used when n > shots for a requested sample

class TestDeviceIntegration:
    """Tests that the SimulatorDevice integrates well with PennyLane"""

    def test_device_loading(self):
        """Tests that the cirq.simulator device is properly loaded"""

        dev = qml.device("cirq.simulator", wires=2)

        assert dev.num_wires == 2
        assert dev.shots == 0
        assert dev.short_name == "cirq.simulator"


class TestApply:
    """Tests that gates are correctly applied"""

    def test_simple_circuit(self):
        """Tests a simple circuit"""

        qubits = [cirq.GridQubit(0, 0), cirq.GridQubit(0, 1), cirq.GridQubit(1, 0), cirq.GridQubit(1, 1)]
        dev = qml.device("cirq.simulator", wires=4, qubits=qubits, shots=10)

        @qml.qnode(dev)
        def circuit():
            qml.PauliX(wires=0)
            qml.CZ(wires=[0, 1])
            qml.CNOT(wires=[2, 0])
            qml.PauliY(wires=1)
            qml.RX(0.342, wires=1)
            qml.CNOT(wires=[0, 1])
            qml.CNOT(wires=[2, 3])
            qml.CNOT(wires=[1, 3])
            qml.CNOT(wires=[0, 3])
            qml.RY(0.342, wires=1)
            qml.Hadamard(wires=1)
            qml.SWAP(wires=[1, 2])
            qml.RZ(0.342, wires=1)
            qml.Rot(0.342, 0.2, 0.1, wires=0)
            qml.PauliX(wires=0)
            qml.Hadamard(wires=2)
            qml.SWAP(wires=[0, 1])
            qml.CNOT(wires=[0, 1])
            qml.CNOT(wires=[1, 2])
            qml.CNOT(wires=[2, 0])

            return qml.expval(qml.PauliX(0)), qml.var(qml.PauliY(1)), qml.sample(qml.Hadamard(2), n=20), qml.expval(qml.Hermitian(np.array([[2, 1j], [-1j, 2]]), 3))

        print(circuit())

        raise Exception()
        

