""" This is my first python class """
class firstclass:
    """ Initializing of method """
    def __init__(self):
        #self._bar = 1
        self._frontier = {'Up', 'Down'}

    @property
    def bar(self):
        """ Bar property setter """
        return self._bar
    @bar.setter
    def bar(self, value):
        print('setting value of ',value)
        self._bar = value

    @bar.getter
    def bar(self):
        print("in getter of bar")
        return self._bar



foo = firstclass()
print(foo._frontier)
foo.bar = 10
print(foo.bar)




