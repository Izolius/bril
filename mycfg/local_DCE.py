import json
import sys
from typing import Any, Dict, List
from mycfg import create_blocks

InstrType = Dict[str, Any]

def optimize_block(block: List[InstrType])->bool:
    assigns: Dict[str, InstrType] = {}
    changed: bool = False
    for instr in block[:]:
        if 'args' in instr:
            for arg in instr['args']:
                if arg in assigns:
                    assigns.pop(arg)
        if 'dest' in instr:
            if instr['dest'] in assigns:
                block.remove(assigns[instr['dest']])
                changed = True
            assigns[instr['dest']] = instr
    return changed

def local_dce()->None:
    jsonProgram = json.load(sys.__stdin__)
    for function in jsonProgram['functions']:
        new_body = []
        for block in create_blocks(function['instrs']):
            changed: bool = True
            while changed:
                changed = optimize_block(block)
            new_body.extend(block)
        function['instrs'] = new_body
    print(json.dumps(jsonProgram))

if __name__ == '__main__':
    local_dce()
    