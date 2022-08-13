from typing import Any, Dict


InstrType = Dict[str, Any]

def is_definition(instr: InstrType) -> bool:
    return 'dest' in instr

