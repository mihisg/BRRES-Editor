"""class Observer:
    def onNodeUpdate(self, node):
        pass

    def onRenameUpadte(self, node):
        pass

    def onChildUpdate(self, node):
        pass
"""
class SubSection:
    """
        Represents a brres-subsection, base class for mdl0, tex0, ...
        """

    @property
    def TAG(self):
        raise NotImplementedError()

    @property
    def EXTENSION(self):
        raise NotImplementedError()

    def __init__(self, name, parent):
        self.parent = parent
        self.name = name
        self.observers = []
        self.isModified = False

    def rename(self, name):
        if name != self.name:
            oldName = self.name
            self.name = name
            self.markModified(False)
            #self.notifyRename(oldName)
            return True
        return False

    def markModified(self, notifyObservers=True):
        if notifyObservers:
            pass#self.notifyObservers()
        if not self.isModified:
            self.isModified = True
            if self.parent:
                self.parent.markModified(False)

    def markUnmodified(self):
        self.isModified = False

    def unpack(self, data):
        raise NotImplementedError()

    def pack(self):
        raise NotImplementedError()

    """def notifyRename(self, oldName):
        if self.observers:
            for o in self.observers:
                o.onRenameUpdate(self, oldName)
        self.notifyParentObservers()"""

    """def notifyParentObservers(self):
        parent = self.parent
        if parent and parent.observers:
            for o in parent.observers:
                o.onChildUpdate()"""

    """def registerObserver(self, observer):
        if self.observers is None:
            self.observers = [observer]
        elif observer not in self.observers:
            self.observers.append(observer)"""

    """def unregister(self, observer):
        try:
            self.observers.remove(observer)
        except ValueError as e:
            print(f"Could not remove observer {observer} because it is not contained in the list: {e} ")"""

    """def notifyObservers(self):
        if self.observers:
            for o in self.observers:
                o.onNodeUpdate()
        self.notifyParentObservers()"""
