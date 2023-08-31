from typing import Any, Dict, List, Set
from mycfg import build_blocks

InstrType = Dict[str, Any]

class Cfg:
    label2block: Dict[str, List[InstrType]] = {}
    label_to_output_labels: Dict[str, List[str]] = {}
    blocks: List[List[InstrType]] = []

    def __init__(self, body = [], label_to_successors: Dict[str, List[str]] = {}):
        if len(label_to_successors) == 0:
            self.label2block = {}
            self.label_to_output_labels = {}
            for block, label, output_labels in build_blocks(body):
                if label == '':
                    label = "block{}".format(len(self.label2block))
                self.label2block[label] = block
                self.label_to_output_labels[label] = output_labels
                self.blocks.append(block)
        else:
            self.label_to_output_labels = dict(label_to_successors)
            self.label2block = dict(map(lambda label: (label, []), label_to_successors.keys()))
            self.blocks = [[] for label in label_to_successors.keys()]

    def get_entry_label(self) -> str:
        return [k for k,v in self.label2block.items() if v == self.blocks[0]][0]

    def get_block_by_label(self, label: str) -> List[InstrType]:
        return self.label2block[label]

    def get_successors_by_label(self, label: str) -> List[str]:
        return self.label_to_output_labels[label]

    def get_predecessors_by_label(self, label:str) -> List[str]:
        if label in self.label2block:
            return BasicBlock(self, label).get_predecessors()
        else:
            return []

    def get_all_labels(self):
        return [k for k,v in self.label2block.items()]

class BasicBlock:
    label: str = ""
    cfg: Cfg
    def __init__(self, cfg: Cfg, label: str):
        self.cfg = cfg
        self.label = label
    
    def get_predecessors(self) -> List[str]:
        predecessors: List[str] = []
        for current_label, successor_labels in self.cfg.label_to_output_labels.items():
            for successor_label in successor_labels:
                if successor_label == self.label:
                    predecessors.append(current_label)
        return predecessors

    def get_successors(self) -> List[str]:
        return self.cfg.label_to_output_labels[self.label]
