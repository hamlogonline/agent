from weakref import ref as weak_ref

class Observable():

    _observers = dict()

    def __setattr__(self, name, new_value):
        super().__setattr__(name, new_value)
        if name in self._observers:
            for (func_ref, self_ref) in self._observers[name]:
                func_ref = func_ref()
                if self_ref is not None:
                    self_ref = self_ref()
                    if self_ref is None:
                        continue
                    func_ref(self_ref)
                else:
                    if func_ref is None:
                        continue
                    func_ref(new_value)

    def add_observer(self, name, observer):
        if name in self.__dict__:
            try:
                observer_ref = (weak_ref(observer.__func__), weak_ref(observer.__self__))
            except:
                observer_ref = (weak_ref(observer), None)
            try:
                self._observers[name].add(observer_ref)
            except:
                self._observers[name] = set([observer_ref])
        else:
            raise ValueError('Cannot observe nonexistent variable')
