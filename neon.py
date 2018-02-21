#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ast
import collections

import commands
import parser

CODE_PAGE = ('⌀⌁⌃⌄⌅⌆⌇⌈⌉⌊⌋\n⌂⌖⌜⌝⁰¹²³⁴⁵⁶⁷⁸⁹¤×⌑÷⌞⌟ !"#$%&\'()*+,-./0123456789:;<'
             '=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{'
             '``}~⌐¬⌌⌍±⌔⌓○⌕⌤⊠⟨⌶⟩⌬∮⌙⌯⌎⌏∓⌰⌱⌽⌳⌲⌴≠≈≡⍂⌮⍅⍆⍑⍍⍦⍧∘⌾Δ⍋≎≤≀≥⍁⌭√Σ⍊⍔∝∞⍀⍉∇⍒⊢'
             '⊣≺≻⊲⊳⍬⍭⍳⍴⍵⋮⌿∴⊄∩⊅∈∋∧⊶⊷↕↑↔⋅⋱…⋰∵⊂∪⊃∉∌∨∥∦←↓→↖↗⊕⊖⊗⊘⊙⊜⋉⋈⋊⏚∀⇐↭⇒↙↘πσθλμ'
             'φΩ«»‹›')

class Stack:
    def __init__(self, items = None):
        if items is None:
            self.items = []
        else:
            self.items = items
    
    def __iter__(self):
        while self.items:
            yield self.items.pop()
    
    def __contains__(self):
        return i in self.items

    def __repr__(self):
        if self.items:
            return 'Stack({})'.format(self.items)
        
        return 'Stack()'
    
    def __str__(self):
        return repr(self)

    def push(self, items, idx = None):
        if idx is None:
            self.items.extend(items)
        else:
            self.items[:idx] += items
    
    def pop(self, idx = None):
        if idx is None:
            return self.items.pop()
        
        return self.items.pop(idx)
    
    def peek(self, idx = None):
        if idx is None:
            return self.items[-1]
        
        return self.items[idx]

State = collections.namedtuple('State', ['stack', 'functions', 'register'])

def parse_literal(literal):
    str = literal.string

    if isinstance(literal, (parser.Data,
                            parser.Number,
                            parser.Text,
                            parser.String,
                            parser.Character,
                            parser.List)):
        return parse_literal(literal.elements[0])

    if isinstance(literal, parser.Complex):
        if str == 'j':
            return 1j
        
        return ast.literal_eval(str)
    if isinstance(literal, parser.ScientificNotation):
        if str == 'e':
            return 1e2
        if literal.elements[0] is None:
            return ast.literal_eval('1' + str)
        if literal.elements[2] is None:
            return ast.literal_eval(str + '2')
        
        return ast.literal_eval(str)
    if isinstance(literal, parser.Float):
        if str == '.':
            return 0.5
        if str == '-.':
            return -0.5
        
        return ast.literal_eval(str)
    if isinstance(literal, parser.Integer):
        if str == '-':
            return -1
        
        return ast.literal_eval(str)
    if isinstance(literal, parser.LeftUnclosedString):
        str = str.replace('"""', '\\"""')
        str = str.replace('\n', '\\n')
        str = str.replace('\\«', '«')
        str = str.replace('\\»', '»')

        return ast.literal_eval('"""' + str[:-1] + '"""')
    if isinstance(literal, parser.RightUnclosedString):
        str = str.replace('"""', '\\"""')
        str = str.replace('\n', '\\n')
        str = str.replace('\\«', '«')
        str = str.replace('\\»', '»')

        return ast.literal_eval('"""' + str[1:] + '"""')
    if isinstance(literal, parser.ClosedString):
        str = str.replace('"""', '\\"""')
        str = str.replace('\n', '\\n')
        str = str.replace('\\«', '«')
        str = str.replace('\\»', '»')

        return ast.literal_eval('"""' + str[1:-1] + '"""')
    if isinstance(literal, parser.Character):
        return str[1]
    if isinstance(literal, parser.LeftUnclosedList):
        ret = []

        for i in literal.elements[0].elements:
            if i.string != ' ':
                ret.append(parse_literal(i))
        
        return ret
    if isinstance(literal, (parser.ClosedList, parser.RightUnclosedList)):
        ret = []

        for i in literal.elements[1].elements:
            if i.string != ' ':
                ret.append(parse_literal(i))
        
        return ret

    return state