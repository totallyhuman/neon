#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from modgrammar import *

import commands

class Program(Grammar):
    grammar = ZERO_OR_MORE(REF('Function') | '\n')

class Function(Grammar):
    grammar = (OPTIONAL(REF('LeftUnclosedString') | REF('LeftUnclosedList')),
               ZERO_OR_MORE(REF('Data') | REF('Loop') | REF('Command') | ' '))

class Data(Grammar):
    grammar = REF('Number') | REF('Text') | REF('List')

class Number(Grammar):
    grammar = REF('Complex') \
            | REF('ScientificNotation') \
            | REF('Float') \
            | REF('Integer')

class Integer(Grammar):
    grammar = REF('PositiveInteger') | REF('NegativeInteger')

class PositiveInteger(Grammar):
    grammar = REPEAT(REF('Digit'))

class NegativeInteger(Grammar):
    grammar = ('-', ZERO_OR_MORE(REF('Digit')))

class Float(Grammar):
    grammar = (OPTIONAL(REF('Integer')),
               '.',
               OPTIONAL(REF('PositiveInteger')))

class ScientificNotation(Grammar):
    grammar = (OPTIONAL(REF('Integer') | REF('Float')),
               'e',
               OPTIONAL(REF('Integer') | REF('Float')))

class Complex(Grammar):
    grammar = (OPTIONAL(REF('Integer') \
                      | REF('Float') \
                      | REF('ScientificNotation')),
               'j')

class Digit(Grammar):
    grammar = OR(*'0123456789')

class Text(Grammar):
    grammar = REF('String') | REF('Character')

class String(Grammar):
    grammar = REF('ClosedString') | REF('RightUnclosedString')

class ClosedString(Grammar):
    grammar = ('«', ZERO_OR_MORE(REF('ValidCharacter')), '»')

class LeftUnclosedString(Grammar):
    grammar = (ZERO_OR_MORE(REF('ValidCharacter')), '»')

class RightUnclosedString(Grammar):
    grammar = ('«', ZERO_OR_MORE(REF('ValidCharacter')), EOF)

class ValidCharacter(Grammar):
    grammar = OR(('\\', OR(*'«»')), EXCEPT(ANY, OR(*'«»')))

class Character(Grammar):
    grammar = ('‹', ANY)

class List(Grammar):
    grammar = REF('ClosedList') | REF('RightUnclosedList')

class ClosedList(Grammar):
    grammar = ('[', ZERO_OR_MORE(REF('Data') | SPACE), ']')

class LeftUnclosedList(Grammar):
    grammar = (ZERO_OR_MORE(REF('Data') | SPACE), ']')

class RightUnclosedList(Grammar):
    grammar = ('[', ZERO_OR_MORE(REF('Data') | SPACE), EOL)

class Loop(Grammar):
    grammar = (OR('∞', '∀', '(', '⟨', '⟩'),
               ZERO_OR_MORE(REF('Data') | REF('Loop') | REF('Command')),
               ')' | EOL)

class Command(Grammar):
    grammar = REF('FunctionCall') | OR(*commands.commands)

class FunctionCall(Grammar):
    grammar = WORD('⁰¹²³⁴⁵⁶⁷⁸⁹')
