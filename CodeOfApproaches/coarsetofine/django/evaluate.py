from __future__ import division
import os
import argparse
import torch
import codecs
import glob
import re

import table
import table.IO
import opts
import bleu_by_qt as bl

parser = argparse.ArgumentParser(description='evaluate.py')
opts.translate_opts(parser)
opt = parser.parse_args()
torch.cuda.set_device(opt.gpu)
opt.anno = os.path.join(opt.root_dir, opt.dataset, '{}.json'.format(opt.split))
opt.pre_word_vecs = os.path.join(opt.root_dir, opt.dataset, 'embedding')

if opt.beam_size > 0:
    opt.batch_size = 1


def main():
    dummy_parser = argparse.ArgumentParser(description='train.py')
    opts.model_opts(dummy_parser)
    opts.train_opts(dummy_parser)
    dummy_opt = dummy_parser.parse_known_args([])[0]

    js_list = table.IO.read_anno_json(opt.anno, opt)

    metric_name_list = ['tgt']
    prev_best = (None, None)
    for fn_model in glob.glob(opt.model_path):
        opt.model = fn_model
        print(fn_model)
        print(opt.anno)

        translator = table.Translator(opt, dummy_opt.__dict__)
        data = table.IO.TableDataset(
            js_list, translator.fields, 0, None, False)
        test_data = table.IO.OrderedIterator(
            dataset=data, device=opt.gpu, batch_size=opt.batch_size, train=False, sort=True, sort_within_batch=False)

        # inference
        r_list = []
        for batch in test_data:
            r = translator.translate(batch)
            r_list += r
        r_list.sort(key=lambda x: x.idx)
        assert len(r_list) == len(js_list), 'len(r_list) != len(js_list): {} != {}'.format(
            len(r_list), len(js_list))

        # evaluation
        b = 0.0
        i = 0
        for pred, gold in zip(r_list, js_list):
            print(gold['tgt'])
            print('---------------------------')

            l=[]
            for a in pred.tgt:
                if a == 'NEWLINE':
                    a = '\n'
                if a == 'NL':
                    a = '\n'
                if a == 'INDENT':
                    a = '    '
                if a == 'DEDENT':
                    a = ''
                l.append(a)
            # print(l)
            b += bl.compute_bleu(gold['tgt'], l)
            if i < 300:
                f = open('../py/%i.py' % i, 'w')
                s = ''
                for t in l:
                # for t in pred.tgt:
                    s += (t + ' ')
                # print(s)
                s = s.replace(' \n ','\n').replace(' \n','\n').replace('\n ','\n').replace(' (','(').replace('( ','(').replace(' )',')').replace(') ',')').\
                    replace(' [','[').replace('[ ','[').replace(' ]',']').replace('] ',']').replace(' ,',',').replace(' .','.').\
                    replace('. ','.')
                # s = re.sub(r'[\s]*\n[\s]*', '\n', s)
                s = s.replace('\n ', '\n')
                print(s)
                f.write(s)
            i = i + 1
            # pred.eval(gold)
        print('Results:')
        for metric_name in metric_name_list:
            bleu = b / len(r_list)
            print('{}:{:.2%}'.format(metric_name, bleu))
            if metric_name == 'tgt' and (prev_best[0] is None or bleu > prev_best[1]):
                prev_best = (fn_model, bleu)
            # c_correct = sum((x.correct[metric_name] for x in r_list))
            # acc = c_correct / len(r_list)
            # print('{}: {} / {} = {:.2%}'.format(metric_name,
            #                                     c_correct, len(r_list), acc))
            # if metric_name == 'tgt' and (prev_best[0] is None or acc > prev_best[1]):
            #     prev_best = (fn_model, acc)

    if (opt.split == 'dev') and (prev_best[0] is not None):
        with codecs.open(os.path.join(opt.root_dir, opt.dataset, 'dev_best.txt'), 'w', encoding='utf-8') as f_out:
            f_out.write('{}\n'.format(prev_best[0]))


if __name__ == "__main__":
    main()
