from enthought.traits.api import Range as _Range, Tuple as _Tuple
from enthought.traits.ui.api import TupleEditor

class EditorTraits(object):
    def get_editor(self, *args, **kwds):
        e = super(EditorTraits, self).get_editor(*args, **kwds)
        editor_t = {'auto_set':False,
                    'enter_set':True}
        metadata = self._metadata
        if 'editor_traits' in metadata:
            editor_t.update(metadata['editor_traits'])
        e.set(**editor_t)
        return e

class Range(EditorTraits, _Range):
    pass
    
class Tuple(EditorTraits, _Tuple):
    pass