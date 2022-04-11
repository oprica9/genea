from configparser import ConfigParser
import errors


class Configuration:
    def __init__(self):
        self.max_iter = 150
        self._pop_size = 10
        self._mating_num = 10
        self._mutation_num = 10
        self._mut_rate = 0.2
        self._discard_num = 0
        self.child_percentage = 0.5
        self._min_bound = -5
        self._max_bound = 5
        self._alpha = 0.5
        self._sigma = 0.2
        self.seed = 0
        self.file_path = ""

    @property
    def pop_size(self):
        return self._pop_size

    @pop_size.setter
    def pop_size(self, n):
        if n < 2:
            raise errors.InvalidConfigError("Population must be an integer larger than 1")
        self._pop_size = n

    @property
    def mating_num(self):
        return self._mating_num

    @mating_num.setter
    def mating_num(self, n):
        if n < 2:
            raise errors.InvalidConfigError("Mating number must be an integer larger than 1")
        self._mating_num = n

    @property
    def mutation_num(self):
        return self._mutation_num

    @mutation_num.setter
    def mutation_num(self, n):
        if n < 0:
            raise errors.InvalidConfigError("Mating number must be an integer larger than or equal to 0")
        self._mutation_num = n

    @property
    def mut_rate(self):
        return self._mut_rate

    @mut_rate.setter
    def mut_rate(self, n):
        if n < 0 or n > 1:
            raise errors.InvalidConfigError("Mutation rate must be a real number in range [0, 1]")
        self._mut_rate = n

    @property
    def discard_num(self):
        return self._discard_num

    @discard_num.setter
    def discard_num(self, n):
        if n < 0:
            raise errors.InvalidConfigError("Discard number must be an integer larger than or equal to 0")
        self._discard_num = n

    @property
    def min_bound(self):
        return self._min_bound

    @min_bound.setter
    def min_bound(self, n):
        if n >= self._max_bound:
            raise errors.InvalidConfigError("Min bound must be an integer less than max bound")
        self._min_bound = n

    @property
    def max_bound(self):
        return self._max_bound

    @max_bound.setter
    def max_bound(self, n):
        if n < self._min_bound:
            raise errors.InvalidConfigError("Max bound must be an integer greater than min bound")
        self._max_bound = n

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, n):
        if n < 0 or n > 1:
            raise errors.InvalidConfigError("Alpha must be a real number in range [0, 1]")
        self._alpha = n

    @property
    def sigma(self):
        return self._sigma

    @sigma.setter
    def sigma(self, n):
        if n < 0 or n > 1:
            raise errors.InvalidConfigError("Sigma must be a real number in range [0, 1]")
        self._sigma = n

    def __str__(self):
        return f"max_iter = {self.max_iter}\n " + \
               f"pop_size = {self.pop_size}\n " + \
               f"mating_num = {self.mating_num}\n " + \
               f"mutation_num = {self.mutation_num}\n " + \
               f"mutation_rate = {self.mut_rate}\n " + \
               f"discard_num = {self.discard_num}\n " + \
               f"child_percentage = {self.child_percentage}\n " + \
               f"min_opseg = {self.min_bound}\n " + \
               f"max_opseg = {self.max_bound}\n " + \
               f"alpha = {self.alpha}\n " + \
               f"sigma = {self.sigma}\n " + \
               f"seed = {self.seed}\n "


def load_config(path):
    parser = ConfigParser()
    parser.read(path)
    if len(parser.sections()) == 0:
        if path != "config.ini":
            raise errors.InvalidConfigError("Invalid config file")
        else:
            return Configuration()

    config = Configuration()

    for e in parser.sections():
        for name, value in parser.items(e):
            if name == "max_iter":
                config.max_iter = int(value)
            if name == "pop_size":
                config.pop_size = int(value)
            if name == "mating_num":
                config.mating_num = int(value)
            if name == "mutation_num":
                config.mutation_num = int(value)
            if name == "mutation_rate":
                config.mutation_rate = float(value)
            if name == "discard_num":
                config.discard_num = float(value)
            if name == "child_percentage":
                config.child_percentage = float(value)
            if name == "min_opseg":
                config.min_bound = float(value)
            if name == "max_opseg":
                config.max_bound = float(value)
            if name == "alpha":
                config.alpha = float(value)
            if name == "sigma":
                config.sigma = float(value)
            if name == "seed":
                config.seed = int(value)
            if name == "file_path":
                config.file_path = value

    return config
