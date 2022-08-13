import json
import sys

def optimize_func(function)->bool:
    isused = []
    changed: bool = False
    for instr in function['instrs']:
        if 'args' in instr:
            for arg in instr['args']:
                isused.append(arg)
    result = []
    for instr in function['instrs']:
        if 'dest' in instr and instr['dest'] not in isused:
            changed = True
            continue
        else:
            result.append(instr)
    function['instrs'] = result
    return changed

def global_dce()->None:
    jsonProgram = json.load(sys.__stdin__)
    for function in jsonProgram['functions']:
        changed = True
        while changed is True:
            changed = optimize_func(function)
    print(json.dumps(jsonProgram))

if __name__ == '__main__':
    global_dce()