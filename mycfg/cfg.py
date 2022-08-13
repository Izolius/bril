from typing import Any, Dict, List
from mycfg import build_blocks

InstrType = Dict[str, Any]

class Cfg:
    label2block: Dict[str, List[InstrType]] = {}
    label_to_output_labels: Dict[str, List[str]] = {}
    blocks: List[List[InstrType]] = []

    def __init__(self, body):
        self.label2block = {}
        self.label_to_output_labels = {}
        for block, label, output_labels in build_blocks(body):
            if label == '':
                label = "block{}".format(len(self.label2block))
            self.label2block[label] = block
            self.label_to_output_labels[label] = output_labels
            self.blocks.append(block)

    def get_entry_label(self) -> str:
        return [k for k,v in self.label2block.items() if v == self.blocks[0]][0]

    def get_block_by_label(self, label: str) -> List[InstrType]:
        return self.label2block[label]

    def get_successors_by_label(self, label: str) -> List[str]:
        return self.label_to_output_labels[label]

    def get_predecessors_by_label(self, label:str) -> List[str]:
        predecessors: List[str] = []
        for current_label, successor_labels in self.label_to_output_labels.items():
            for successor_label in successor_labels:
                if successor_label == label:
                    predecessors.append(current_label)
        return predecessors

    def get_all_labels(self):
        return [k for k,v in self.label2block.items()]
        