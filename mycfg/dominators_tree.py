from typing import Dict, List, Set
from cfg import Cfg
from dominators import Dominators


class DominatorsTree:
    cfg: Cfg
    tree: Dict[str, Set[str]] = {}
    root: str
    
    def build(self, cfg: Cfg, dominators: Dominators)->None:
        self.cfg = cfg
        depth: List[Set[str]] = [set()] * len(dominators.dominators)
        node_depth: Dict[str, int] = {}
        max_depth: int = -1
        self.root = cfg.get_entry_label()
        for label in cfg.get_all_labels():
            self.tree[label] = set()

        for node, doms in dominators.dominators:
            cur_depth = len(doms)
            depth[cur_depth].add(node)
            node_depth[node] = cur_depth
            if (cur_depth > max_depth):
                max_depth = cur_depth
        
        self.tree.update(self.root, set(depth[2]))

        for node, doms in dominators.dominators:
            if node == self.root:
                continue
            max_depth_dom: str
            max_depth = -1
            for dom in doms:
                if node == dom:
                    continue
                if (node_depth[dom] > max_depth):
                    max_depth = node_depth[dom]
                    max_depth_dom = dom
            if max_depth == -1:
                print(f"{node} with doms:{doms} doesn't have parent node")
                break
            self.tree[max_depth_dom].add(node)
