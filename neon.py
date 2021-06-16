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
    
    def __contains__(self, i):
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

def sanitize(string):
    string = string.replace('"""', '\\"""')
    string = string.replace('\\«', '«')
    string = string.replace('\\»', '»')

    return string

def neon_eval(literal):
    string = literal.string

    if isinstance(literal, parser.Complex):
        if string == 'j':
            return 1j
        
        return ast.literal_eval(string)

    if isinstance(literal, parser.ScientificNotation):
        if string == 'e':
            return 1e2
        if literal.elements[0] is None:
            return ast.literal_eval('1' + string)
        if literal.elements[2] is None:
            return ast.literal_eval(string + '2')
        
        return ast.literal_eval(string)

    if isinstance(literal, parser.Float):
        if string == '.':
            return 0.5
        if string == '-.':
            return -0.5
        
        return ast.literal_eval(string)

    if isinstance(literal, parser.Integer):
        if string == '-':
            return -1
        
        return ast.literal_eval(string)

    if isinstance(literal, parser.LeftUnclosedString):
        return ast.literal_eval('"""' + sanitize(string)[:-1] + '"""')

    if isinstance(literal, parser.RightUnclosedString):
        return ast.literal_eval('"""' + sanitize(string)[1:] + '"""')

    if isinstance(literal, parser.ClosedString):
        return ast.literal_eval('"""' + sanitize(string)[1:-1] + '"""')

    if isinstance(literal, parser.Character):
        return string[1]

    if isinstance(literal, parser.LeftUnclosedList):
        ret = []

        for i in literal.elements[0].elements:
            if i.string != ' ':
                ret.append(neon_eval(i))
        
        return ret

    if isinstance(literal, (parser.ClosedList, parser.RightUnclosedList)):
        ret = []

        for i in literal.elements[1].elements:
            if i.string != ' ':
                ret.append(neon_eval(i))
        
        return ret

    return neon_eval(literal.elements[0])
