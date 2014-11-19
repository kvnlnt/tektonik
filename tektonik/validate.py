class Validate:

    @staticmethod
    def property(value, name):
        if len(value) == 0:
            raise ValueError("{} is not a valid property".format(value))
        return value
