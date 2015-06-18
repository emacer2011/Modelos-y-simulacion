#!/usr/bin/python2.7
# -*- coding: utf-8 -*-


def singleton(klass):
    if not klass._instance:
        klass._instance = klass()
    return klass._instance


class Reloj(object):
    _instance = None

    def __init__(self):
        self.valor = 0

    def get_reloj(self):
        return self.valor

    def set_reloj(self, new_valor):
        self.valor = new_valor
