#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from modgrammar import *

import commands

class Command(Grammar):
    grammar = OR(*'⌀⌁⌃⌄⌅⌆⌇⌈⌉⌊⌋⌂⌖⌜⌝⁰¹²³⁴⁵⁶⁷⁸⁹¤×⌑÷⌞⌟!"#$%&\'*+,-./:;<=>?@ABCDEF'
                  'GHIJKLMNOPQRSTUVWXYZ\^_`abcdefghijklmnopqrstuvwxyz{|}~⌐¬⌌⌍'
                  '±⌔⌓○⌕⌤⊠⌶⌬∮⌙⌯⌎⌏∓⌰⌱⌽⌳⌲⌴≠≈≡⍂⌮⍅⍆⍑⍍⍦⍧∘⌾Δ⍋≎≤≀≥⍁⌭√Σ⍊⍔∝⍀⍉∇⍒⊢⊣≺≻⊲⊳⍬'
                  '⍭⍳⍴⍵⋮⌿∴⊄∩⊅∈∋∧⊶⊷↕↑↔⋅⋱…⋰∵⊂∪⊃∉∌∨∥∦←↓→↖↗⊕⊖⊗⊘⊙⊜⋉⋈⋊⏚⇐↭⇒↙↘πσθλμφΩ'
                )

class Digit(Grammar):
    grammar = OR(*'0123456789')

class PositiveInteger(Grammar):
    grammar = REPEAT(Digit)

class NegativeInteger(Grammar):
    grammar = ('-', ZERO_OR_MORE(Digit))

class Integer(Grammar):
    grammar = PositiveInteger | NegativeInteger

class Float(Grammar):
    grammar = (OPTIONAL(Integer), '.', OPTIONAL(PositiveInteger))

class ScientificNotation(Grammar):
    grammar = (OPTIONAL(Integer | Float), 'e', OPTIONAL(Integer | Float))

class Complex(Grammar):
    grammar = (OPTIONAL(Integer  | Float  | ScientificNotation), 'j')

class Number(Grammar):
    grammar = Complex | ScientificNotation | Float | Integer

class Character(Grammar):
    grammar = ('‹', ANY)

class ValidCharacter(Grammar):
    grammar = OR(('\\', OR(*'«»')), EXCEPT(ANY, OR(*'«»')))

class ClosedString(Grammar):
    grammar = ('«', ZERO_OR_MORE(ValidCharacter), '»')

class LeftUnclosedString(Grammar):
    grammar = (ZERO_OR_MORE(ValidCharacter), '»')

class RightUnclosedString(Grammar):
    grammar = ('«', ZERO_OR_MORE(ValidCharacter), EOF)

class String(Grammar):
    grammar = ClosedString | RightUnclosedString

class Text(Grammar):
    grammar = String | Character

class ClosedList(Grammar):
    grammar = ('[', ZERO_OR_MORE(REF('Literal') | SPACE), ']')

class LeftUnclosedList(Grammar):
    grammar = (ZERO_OR_MORE(REF('Literal') | SPACE), ']')

class RightUnclosedList(Grammar):
    grammar = ('[', ZERO_OR_MORE(REF('Literal') | SPACE), EOL | EOF)

class List(Grammar):
    grammar = ClosedList | RightUnclosedList

class Literal(Grammar):
    grammar = Number | Text | List

class Loop(Grammar):
    grammar = (OR('∞', '∀', '(', '⟨', '⟩'),
               ZERO_OR_MORE(Literal | REF('Loop') | Command), ')' | EOL)

class Function(Grammar):
    grammar = (OPTIONAL(LeftUnclosedString | LeftUnclosedList),
               ZERO_OR_MORE(Literal | Loop | Command | ' '))

class Program(Grammar):
    grammar = ZERO_OR_MORE(Function | '\n')

parse_program  = Program.parser().parse_string
parse_function = Function.parser().parse_string
parse_literal  = Literal.parser().parse_string
