import unittest
from dominators import Dominators
from cfg import Cfg


class TestDominators(unittest.TestCase):
    def test_build_simple(self):
        cfg = Cfg(label_to_successors={'entry':['a'], 'a':['b'], 'b':['a']})
        doms = Dominators()
        doms.build(cfg)

        self.assertEqual(doms.get_dominators('entry'), {'entry'})
        self.assertEqual(doms.get_dominators('a'), {'a', 'entry'})
        self.assertEqual(doms.get_dominators('b'), {'a', 'b', 'entry'})

    def test_build_not_natural_loop(self):
        cfg = Cfg(label_to_successors={'entry':['a', 'b'], 'a':['b'], 'b':['a']})
        doms = Dominators()
        doms.build(cfg)

        self.assertEqual(doms.get_dominators('entry'), {'entry'})
        self.assertEqual(doms.get_dominators('a'), {'a', 'entry'})
        self.assertEqual(doms.get_dominators('b'), {'b', 'entry'})
    
    def test_build_loop_with_if(self):
        cfg = Cfg(label_to_successors={
            'entry':['loop'],
            'loop':['body', 'exit'],
            'body':['then','endif'],
            'then':['endif'],
            'endif':['loop'],
            'exit':[]})
        doms = Dominators()
        doms.build(cfg)

        self.assertEqual(doms.get_dominators('entry'), {'entry'})
        self.assertEqual(doms.get_dominators('loop'), {'loop', 'entry'})
        self.assertEqual(doms.get_dominators('body'), {'body', 'loop', 'entry'})
        self.assertEqual(doms.get_dominators('then'), {'body', 'loop', 'entry', 'then'})
        self.assertEqual(doms.get_dominators('endif'), {'body', 'loop', 'entry', 'endif'})
        self.assertEqual(doms.get_dominators('exit'), {'exit', 'loop', 'entry'})

    def test_build_two_conditions(self):
        cfg = Cfg(label_to_successors={
            'entry':['cond1'],
            'cond1':['true1', 'false1'],
            'true1':['cond2'],
            'false1':['cond2'],
            'cond2':['true2', 'false2'],
            'true2':['exit'],
            'false2':['exit'],
            'exit':[]
            })
        doms = Dominators()
        doms.build(cfg)

        self.assertEqual(doms.get_dominators('entry'), {'entry'})
        self.assertEqual(doms.get_dominators('cond1'), {'cond1', 'entry'})
        self.assertEqual(doms.get_dominators('true1'), {'cond1', 'true1', 'entry'})
        self.assertEqual(doms.get_dominators('false1'), {'cond1', 'false1', 'entry'})
        self.assertEqual(doms.get_dominators('cond2'), {'cond2', 'cond1', 'entry'})
        self.assertEqual(doms.get_dominators('true2'), {'cond2', 'true2', 'cond1', 'entry'})
        self.assertEqual(doms.get_dominators('false2'), {'cond2', 'false2', 'cond1', 'entry'})
        self.assertEqual(doms.get_dominators('exit'), {'cond2', 'cond1', 'entry', 'exit'})
