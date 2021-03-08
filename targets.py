"""Cache of target ETH address we are trying to crack."""

import yaml


def targets(stream=None):
    """Load targets from a yaml stream (or return default)."""
    if stream:
        return yaml.safe_load(stream)
    else:
        # return a hardcoded copy of top-100 addresses
        return [
            '0x64F9bfc22E2bB82baAA895317De7B69dB423d45F '
