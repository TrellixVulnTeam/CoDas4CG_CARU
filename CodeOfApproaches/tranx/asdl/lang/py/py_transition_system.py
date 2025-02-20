# coding=utf-8

import ast

import astor

from asdl.lang.py.py_asdl_helper import asdl_ast_to_python_ast, python_ast_to_asdl_ast
from asdl.lang.py.py_utils import tokenize_code
from asdl.transition_system import TransitionSystem, GenTokenAction
import asdl.lang.py.bleu_by_qt as bt


class PythonTransitionSystem(TransitionSystem):
    def tokenize_code(self, code, mode=None):
        return tokenize_code(code, mode)

    def hyp_correct(self, hyp, example):
        ref_code = example.tgt_code
        # ref_py_ast = ast.parse(ref_code).body[0]
        ref_py_ast = ast.parse(ref_code)
        ref_reformatted_code = astor.to_source(ref_py_ast).strip()

        ref_code_tokens = tokenize_code(ref_reformatted_code)
        hyp_code_tokens = tokenize_code(hyp.code)
        # print(ref_code_tokens)
        # print('=====================================')
        # print(hyp_code_tokens)
        # print('++++++++++++++++++++++++++++++++++++++++++++')
        return ref_code_tokens == hyp_code_tokens

    def hyp_bleu(self, hyp, example):
        ref_code = example.tgt_code
        ref_py_ast = ast.parse(ref_code)
        ref_reformatted_code = astor.to_source(ref_py_ast).strip()

        ref_code_tokens = tokenize_code(ref_reformatted_code)
        hyp_code_tokens = tokenize_code(hyp.code)

        return bt.compute_bleu(ref_code_tokens, hyp_code_tokens)

    def surface_code_to_ast(self, code):
        # py_ast = ast.parse(code).body[0]
        py_ast = ast.parse(code)
        return python_ast_to_asdl_ast(py_ast, self.grammar)

    def ast_to_surface_code(self, asdl_ast):
        py_ast = asdl_ast_to_python_ast(asdl_ast, self.grammar)
        code = astor.to_source(py_ast).strip()

        return code

    def compare_ast(self, hyp_ast, ref_ast):
        hyp_code = self.ast_to_surface_code(hyp_ast)
        ref_reformatted_code = self.ast_to_surface_code(ref_ast)

        ref_code_tokens = tokenize_code(ref_reformatted_code)
        hyp_code_tokens = tokenize_code(hyp_code)

        return ref_code_tokens == hyp_code_tokens

    def get_primitive_field_actions(self, realized_field):
        actions = []
        if realized_field.value is not None:
            if realized_field.cardinality == 'multiple':  # expr -> Global(identifier* names)
                field_values = realized_field.value
            else:
                field_values = [realized_field.value]

            tokens = []
            if realized_field.type.name == 'string':
                for field_val in field_values:
                    tokens.extend(field_val.split(' ') + ['</primitive>'])
            else:
                for field_val in field_values:
                    tokens.append(field_val)

            for tok in tokens:
                actions.append(GenTokenAction(tok))

        return actions
