import json
import sys
from typing import Any, Dict, List, Tuple
from cfg import Cfg
from instruction_utils import is_definition
from mycfg import create_blocks

InstrType = Dict[str, Any]
Definitions = Dict[str, InstrType]
definition_index: Dict[str, int] = {}


def merge(defs: List[Definitions])-> Definitions:
    merged_defs: Definitions = {}
    for definition in defs:
        merged_defs.update(definition)

    return merged_defs



def transfer(cfg: Cfg, block_label: str, in_defs: Definitions)->Definitions:
    block = cfg.get_block_by_label(block_label)
    definitions: Definitions = dict(in_defs)
    for instr in block:
        if is_definition(instr):
            definitions[get_definition_name(instr, block_label, block)] = instr

    return definitions

def is_out_defs_equal(out_defs1: Definitions, out_defs2: Definitions)->bool:
    return set([k for k,v in out_defs1.items()]) == set([k for k,v in out_defs2.items()])

def get_definition_name(instr: InstrType, block_label: str, block: List[InstrType])->str:
    index = block.index(instr)
    return f"{block_label}_{instr['dest']}_{index}"


def reaching_definitions(cfg: Cfg) -> Tuple[Dict[str, Definitions], Dict[str, Definitions]]:
    in_defs: Dict[str, Definitions] = {}
    out_defs: Dict[str, Definitions] = {}

    in_defs[cfg.get_entry_label()] = {}
    for label in cfg.get_all_labels():
        out_defs[label] = {}

    worklist: List[str] = cfg.get_all_labels()
    while len(worklist) !=  0:
        b = worklist.pop(0)
        in_defs[b] = merge([out_defs[p] for p in cfg.get_predecessors_by_label(b)])
        old_out_defs = out_defs[b]
        out_defs[b] = transfer(cfg, b, in_defs[b])
        if not is_out_defs_equal(old_out_defs, out_defs[b]):
            worklist.extend(cfg.get_successors_by_label(b))
    return in_defs, out_defs

def df() -> None:
    # json_program = json.load(sys.__stdin__)
    with open(sys.argv[1], encoding = 'utf-8') as file:
        json_program = json.load(file)
        for function in json_program['functions']:
            cfg = Cfg(function['instrs'])
            in_defs, out_defs = reaching_definitions(cfg)
            for label in cfg.get_all_labels():
                print(f"name: {label}, in: {in_defs[label].keys()}, out: {out_defs[label].keys()}\n")
    # print(json.dumps(json_program))

if __name__ == '__main__':
    df()
