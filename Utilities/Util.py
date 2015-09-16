#! /usr/bin/env python

# coding=uft-8


from weakref import ref
from types import MethodType


class Functor(object):
    def __init__(self, pFunc, *args, **kwargs):
        # Shared issues.
        self.vArgs = args
        self.dKwargs = kwargs
        # MethodType
        if type(pFunc) is MethodType:
            self.bIsMethodType = True
            self.wrpObj = ref(pFunc.im_self)
            self.wrpFunc = ref(pFunc.im_func)
        # Function
        else:
            self.bIsMethodType = False
            self.wrpFunc = ref(pFunc)

    def __call__(self):
        if self.bIsMethodType:
            if self.wrpObj():
                return self.wrpFunc()(
                    self.wrpObj(), *self.vArgs, **self.dKwargs)
            else:
                return None
        else:
            return self.wrpFunc()(*self.vArgs, **self.dKwargs)


def main():
    # FunctionTestWithArgs
    def func1(name):
        print name
    a = Functor(func1, 'lixu')
    a()

    # FunctionTestWithoutArgs
    def func2():
        print '123'
    b = Functor(func2)
    b()

    # MethodTest
    class test1(object):
        def func1(self):
            print '456'

        def func2(self, name):
            print name

    c = test1()
    d = Functor(c.func1)
    e = Functor(c.func2, 'baiyinshuo')
    d()
    e()

    del c
    print d()
    print e()


if __name__ == '__main__':
    main()
