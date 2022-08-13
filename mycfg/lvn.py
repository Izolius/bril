import json
import sys
from typing import Any, Dict, List
from mycfg import create_blocks

InstrType = Dict[str, Any]

def replace_args_with_indexes(instr: InstrType, var2index: Dict[str, int]):
    if 'args' in instr:
        for idx, arg in enumerate(instr['args'][:]):
            instr['args'][idx] = var2index[arg]

def replace_arg_indexes_with_arg_names(instr: InstrType, var_names: List[str]):
    if 'args' in instr:
        for idx, arg in enumerate(instr['args'][:]):
            instr['args'][idx] = var_names[arg]

def build_value(instr: InstrType, var2index: Dict[str, int], values: List[str])->str:
    instr_copy: InstrType = instr.copy()
    if 'dest' in instr_copy:
        instr_copy.pop('dest')
    if 'op' in instr_copy and instr_copy['op'] == 'id':
        return values[instr_copy['args'][0]]
    if 'args' in instr_copy:
        # instr_copy['args'] = ["{}".format(arg) for arg in instr_copy['args']]
        instr_copy['args'] = instr_copy['args'][:]
        instr_copy['args'].sort()
    return json.dumps(instr_copy)

def reconstruct_eq(instr: InstrType, source_var_index: int, values: List[str]):
    if ('const' in values[source_var_index]):
        source_instr = json.loads(values[source_var_index])
        instr['op'] = 'const'
        instr['value'] = source_instr['value']
        
    else:
        instr['op'] = 'id'
        instr['args']=[source_var_index]

def is_reassigned_after(block: List[InstrType], after_idx: int, var_name: str)->bool:
    for idx in range(after_idx+1, len(block)-1):
        if 'dest' in block[idx] and block[idx]['dest'] == var_name:
            return True
    return False

def save_unknown_args(instr: InstrType, instr_idx: int, var2index: Dict[str, int], values: List[str], var_names: List[str]):
    if 'args' in instr:
        for arg in instr['args']:
            if arg in var2index:
                continue
            values.append("{}.{}".format(arg, instr_idx))
            var_names.append(arg)
            var2index[arg] = len(values)-1

def optimize_block(block: List[InstrType]):
    var2index: Dict[str, int] = {}
    values: List[str] = []
    var_names: List[str] = []

    for instr_idx, instr in enumerate(block):
        save_unknown_args(instr, instr_idx, var2index, values, var_names)
        replace_args_with_indexes(instr, var2index)
        if 'dest' in instr:
            var_name: str = instr['dest']
            value = build_value(instr, var2index, values)
            # print(value)
            if value in values:
                reconstruct_eq(instr, values.index(value), values)
            else:
                values.append(value)
                if is_reassigned_after(block, instr_idx, var_name):
                    var2index[var_name]=values.index(value)
                    var_name = "lvn.{}".format(instr_idx)
                    instr['dest'] = var_name
                var_names.append(var_name)
            var2index[var_name]=values.index(value)

            # print("--------------")
            # print(value)
            # print("--------------")
            # print(values)
            # print("--------------")
            # print(var2index)
            # print("--------------")
            # print(instr)
            # print("--------------")
        replace_arg_indexes_with_arg_names(instr, var_names)
    
    # print("--------------")
    # print(values)
    # print("--------------")
    # print(var_names)

def lvn()->None:
    jsonProgram = json.load(sys.__stdin__)
    for function in jsonProgram['functions']:
        new_body = []
        for block in create_blocks(function['instrs']):
            optimize_block(block)
            new_body.extend(block)
        function['instrs'] = new_body
    print(json.dumps(jsonProgram))

if __name__ == '__main__':
    lvn()
