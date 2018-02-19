#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import commands
import parser

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
