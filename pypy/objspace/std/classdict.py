from rpython.rlib import rerased
from rpython.rlib.objectmodel import iteritems_with_hash

from pypy.interpreter.error import OperationError, oefmt
from pypy.objspace.std.dictmultiobject import (
    DictStrategy, create_iterator_classes)
from pypy.objspace.std.typeobject import unwrap_cell


class ClassDictStrategy(DictStrategy):
    erase, unerase = rerased.new_erasing_pair("dictproxy")
    erase = staticmethod(erase)
    unerase = staticmethod(unerase)

    def __init__(self, space):
        DictStrategy.__init__(self, space)

    def getitem(self, w_dict, w_key):
        space = self.space
        w_lookup_type = space.type(w_key)
        if (space.is_w(w_lookup_type, space.w_text) or  # Most common path first
            space.abstract_issubclass_w(w_lookup_type, space.w_text)):
            return self.getitem_str(w_dict, space.text_w(w_key))
        elif space.abstract_issubclass_w(w_lookup_type, space.w_unicode):
            try:
                w_key = space.str(w_key)
            except OperationError as e:
                if not e.match(space, space.w_UnicodeEncodeError):
                    raise
                # non-ascii unicode is never equal to a byte string
                return None
            return self.getitem_str(w_dict, space.text_w(w_key))
        else:
            return None

    def getitem_str(self, w_dict, key):
        return self.unerase(w_dict.dstorage).getdictvalue(self.space, key)

    def setitem(self, w_dict, w_key, w_value):
        space = self.space
        if space.is_w(space.type(w_key), space.w_text):
            self.setitem_str(w_dict, self.space.text_w(w_key), w_value)
        else:
            raise oefmt(space.w_TypeError,
                        "cannot add non-string keys to dict of a type")

    def setitem_str(self, w_dict, key, w_value):
        w_type = self.unerase(w_dict.dstorage)
        try:
            w_type.setdictvalue(self.space, key, w_value)
        except OperationError as e:
            raise

    def setdefault(self, w_dict, w_key, w_default):
        w_result = self.getitem(w_dict, w_key)
        if w_result is not None:
            return w_result
        self.setitem(w_dict, w_key, w_default)
        return w_default

    def delitem(self, w_dict, w_key):
        space = self.space
        w_key_type = space.type(w_key)
        if space.is_w(w_key_type, space.w_text):
            key = self.space.text_w(w_key)
            if not self.unerase(w_dict.dstorage).deldictvalue(space, key):
                raise KeyError
        else:
            raise KeyError

    def length(self, w_dict):
        return len(self.unerase(w_dict.dstorage).dict_w)

    def w_keys(self, w_dict):
        space = self.space
        return space.newlist_text(self.unerase(w_dict.dstorage).dict_w.keys())

    def values(self, w_dict):
        return [unwrap_cell(self.space, w_value) for w_value in
                self.unerase(w_dict.dstorage).dict_w.itervalues()]

    def items(self, w_dict):
        space = self.space
        return [space.newtuple2(space.newtext(key), unwrap_cell(self.space, w_value))
                    for (key, w_value) in self.unerase(w_dict.dstorage).dict_w.iteritems()]

    def clear(self, w_dict):
        space = self.space
        w_type = self.unerase(w_dict.dstorage)
        if not w_type.is_heaptype():
            raise oefmt(space.w_TypeError,
                        "can't clear dictionary of type '%N'", w_type)
        w_type.dict_w.clear()
        w_type.mutated(None)

    def getiterkeys(self, w_dict):
        return self.unerase(w_dict.dstorage).dict_w.iterkeys()

    def getitervalues(self, w_dict):
        return self.unerase(w_dict.dstorage).dict_w.itervalues()

    def getiteritems_with_hash(self, w_dict):
        return iteritems_with_hash(self.unerase(w_dict.dstorage).dict_w)

    def wrapkey(space, key):
        return space.newtext(key)

    def wrapvalue(space, value):
        return unwrap_cell(space, value)

create_iterator_classes(ClassDictStrategy)
