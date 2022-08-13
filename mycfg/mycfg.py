import json
import sys

TERMINATORS = ['jmp', 'br', 'ret']

def get_intput_output_labels(current_block, instr):
    if len(current_block) > 0 and 'label' in current_block[0]:
        input_label = current_block[0]['label']
    else:
        input_label = ''
    if 'labels' in instr:
        output_label = instr['labels']
    elif 'label' in instr:
        output_label = [instr['label']]
    else:
        output_label = []
    return input_label, output_label

def build_blocks(body):
    current_block=[]
    for instr in body:
        if 'op' in instr:
            current_block.append(instr)
            if instr['op'] in TERMINATORS:
                input_label, output_labels = get_intput_output_labels(current_block, instr)
                yield current_block, input_label, output_labels
                current_block = []
        elif len(current_block) == 0 and 'label' in instr:
            current_block.append(instr)
        else:
            input_label, output_labels = get_intput_output_labels(current_block, instr)
            yield current_block, input_label, output_labels
            current_block = [instr]
    if len(current_block) != 0:
        input_label, output_labels = get_intput_output_labels(current_block, {})
        yield current_block, input_label, output_labels

def create_blocks(body):
    current_block=[]
    for instr in body:
        if 'op' in instr:
            current_block.append(instr)
            if instr['op'] in TERMINATORS:
                yield current_block
                current_block = []
        else:
            yield current_block
            current_block = [instr]
    if len(current_block) != 0:
        yield current_block

def build_cfg(body):
    label2block = {}
    block2output_labels = []
    cfg = []
    for block, label, output_labels in build_blocks(body):
        if label == '':
            label = "block{}".format(len(block2output_labels))
        label2block[label] = block
        print(output_labels)
        block2output_labels.append((block, output_labels))
        
    for block, output_labels in block2output_labels:
        output_blocks = [label2block[label] for label in output_labels]
        cfg.append((block, output_blocks))
    return cfg


def mycfg():
    jsonProgram = json.load(sys.__stdin__)
    for function in jsonProgram['functions']:
        for block, output_blocks in build_cfg(function['instrs']):
            print(block)
            # print(output_blocks)
        # for block in build_blocks(function['instrs']):
        #     print(block)

if __name__ == '__main__':
    mycfg()