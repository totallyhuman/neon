#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from modgrammar import *


class Program(Grammar):
    grammar = (OPTIONAL(REF('LeftUnclosedString') | REF('LeftUnclosedList')), ZERO_OR_MORE(REF('Data')))

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
    grammar = OR('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')

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
    grammar = OR(('\\', OR('«', '»')), EXCEPT(ANY, OR('«', '»')))

class Character(Grammar):
    grammar = ('‹', ANY)

class List(Grammar):
    grammar = REF('ClosedList') | REF('RightUnclosedList')

class ClosedList(Grammar):
    grammar = ('[', ZERO_OR_MORE(REF('Data') | SPACE), ']')

class LeftUnclosedList(Grammar):
    grammar = (ZERO_OR_MORE(REF('Data') | SPACE), ']')

class RightUnclosedList(Grammar):
    grammar = ('[', ZERO_OR_MORE(REF('Data') | SPACE), EOF)
