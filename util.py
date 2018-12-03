import logging


class LimitedSet():
    def __init__(self, limit=100):
        self.limit = limit
        self.current = 0
        self.data = [None]*limit

    def has_element(self, element):
        if element in self.data:
            logging.info('old url {}'.format(str(element)))
            return True
        else:
            self.current += 1
            self.data[(self.current) % self.limit] = element
            logging.info('new url {}'.format(str(element)))
            return False


if __name__ == '__main__':
    limited_set = LimitedSet()
    print(limited_set.has_element(1))  # F
    print(limited_set.has_element(1))  # T
    print(limited_set.has_element(2))  # F
    print(limited_set.has_element(3))  # F
    print(limited_set.has_element(4))  # F
    print(limited_set.has_element(1))  # F
    print(limited_set.has_element(1))  # T
    print(limited_set.has_element(1))  # T
