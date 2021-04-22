class LeftGrowingList(object):
    def __init__(self, init_list = None):
        self.mem = init_list if init_list is not None else []
        self.start_index = 0

    # This makes that
    # free_space >= needed_space
    def _ensure_enough_space(self, needed_space):
        free_space = self.start_index

        if free_space < needed_space:
            # expands the space by a factor of 2

            extra_space = max(len(self.mem), needed_space - free_space)
            new_mem = [None] * extra_space + self.mem

            # This ensures that
            # len(new_mem) >= len(self.mem)
            # new_free_space >= needed_space
            
            self.mem = new_mem
            # this makes that free_space += extra_space
            self.start_index += extra_space
    
    def popleft(self):
        if len(self.mem) == self.start_index:
            return None 

        retval = self.mem[self.start_index]

        self.start_index += 1
        return retval

    def extendleft(self, alist):
        needed_space = len(alist)
        self._ensure_enough_space(needed_space)
        self.start_index -= needed_space

        self.mem[self.start_index : self.start_index + needed_space] = alist

    def appendleft(self, value):
        self._ensure_enough_space(1)
        self.start_index -= 1

        self.mem[self.start_index] = value

    def __repr__(self):
        return self.mem[self.start_index:].__repr__()

    def __str__(self):
        return self.mem[self.start_index:].__str__()

    def to_list(self):
        return self.mem[self.start_index:]
