from typing import Dict, Set
from cfg import BasicBlock, Cfg


class Dominators:
    cfg: Cfg
    dominators: Dict[str, Set[str]] = {}

    def build(self, cfg: Cfg):
        self.cfg = cfg
        self.dominators.clear()

        for label in self.cfg.get_all_labels():
            self.dominators[label] = set(self.cfg.get_all_labels())
        
        previous_dominators: Dict[str, Set[str]] = {}

        while(self.dominators != previous_dominators):
            previous_dominators = dict(self.dominators)
            for label in self.cfg.get_all_labels():
                block: BasicBlock = BasicBlock(self.cfg, label)
                predecessors_dominators = [self.dominators[pred] for pred in block.get_predecessors()]
                if len(predecessors_dominators) != 0:
                    dominators = set.intersection(*predecessors_dominators)
                else:
                    dominators = set()
                self.dominators[label] = set([label]) | dominators

    def get_dominators(self, block_label: str) -> Set[str]:
        return self.dominators[block_label]