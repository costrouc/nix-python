"""
Support for reading and writting derivations

"""

from typing import List, Dict
import copy

# test
from _nix import isDerivation, storePathToHash, readDerivation


class Derivation:
    def __init__(self, outputs: List, inputSrcs: List, inputDrvs: Dict[str, str], platform: str, builder: str, args: List[str], env: Dict[str, str]):
        self.outputs = outputs
        self.inputSrcs = inputSrcs
        self.inputDrvs = inputDrvs
        self.platform = platform
        self.builder = builder
        self.args = args
        self.env = env

    @staticmethod
    def _parse_outputs(outputs):
        _outputs = {}

        def _parse_output(output):
            _outputs[output[0]] = {
                'path': output[1],
                'hashAlgo': output[2],
                'hash': output[3]
            }

        for output in outputs:
            _parse_output(output)
        return _outputs

    @staticmethod
    def _parse_input_derivations(inputDrvs):
        return {k: v for k, v in inputDrvs}

    @staticmethod
    def _parse_environment(env):
        return {k: v for k, v in env}

    @classmethod
    def from_filename(cls, filename):
        """Read input derivation from filename"""
        with open(filename, 'r') as f:
            return cls.from_string(f.read())

    @classmethod
    def from_string(cls, content: str) -> 'Derivation':
        """Read input derivation from string"""
        if not content.startswith('Derive'):
            raise ValueError(f'string is not a derivation does not start with "Derive"')

        derivation = eval(content[len('Derive'):])

        if len(derivation) != 7:
            raise ValueError(f'string is not a derivation does not have 7 != {len(derivation)} fields')

        return cls(
            outputs=cls._parse_outputs(derivation[0]),
            inputDrvs=cls._parse_input_derivations(derivation[1]),
            inputSrcs=derivation[2],
            platform=derivation[3],
            builder=derivation[4],
            args=derivation[5],
            env=cls._parse_environment(derivation[6]),
        )

    @classmethod
    def from_dict(cls, d: dict):
        """Read input derivations from dictionary"""
        return cls(**d)

    def as_dict(self) -> dict:
        return copy.deepcopy({
            'outputs': self.outputs,
            'inputsSrcs': self.inputSrcs,
            'inputDrvs': self.inputDrvs,
            'platform': self.platform,
            'builder': self.builder,
            'args': self.args,
            'env': self.env
        })
