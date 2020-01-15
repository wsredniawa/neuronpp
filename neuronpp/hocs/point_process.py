from neuronpp.hocs.hoc import Hoc


class PointProcess(Hoc):
    def __init__(self, hoc_obj, name, parent, mod_name):
        Hoc.__init__(self, hoc_obj=hoc_obj, parent=parent, name=name)
        self.mod_name = mod_name

    def __repr__(self):
        return "{}_{}_{}_{}".format(self.parent, self.__class__.__name__, self.mod_name, self.name)
