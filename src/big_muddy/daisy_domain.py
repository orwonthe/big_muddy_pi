class Domain:
    """ A Domain is an object that knows wehter it is a block vs turnout aad console vs serve """

    @property
    def purpose(self):
        return f'{self.first_term} {self.second_term}'

    def is_same_domain(self, other):
        return (self.is_console == other.is_console) and (self.is_block == other.is_block)


class BlockMixin:
    """ A block and not a turnout """

    @property
    def first_term(self):
        return "block"

    @property
    def is_block(self):
        return True

    @property
    def is_turnout(self):
        return False


class TurnoutMixin:
    """ A turnout and not a block """

    @property
    def first_term(self):
        return "turnout"

    @property
    def is_block(self):
        return False

    @property
    def is_turnout(self):
        return True


class ConsoleMixin:
    """ A console and not a servo """

    @property
    def second_term(self):
        return "console"

    @property
    def is_console(self):
        return True

    @property
    def is_servo(self):
        return False


class ServoMixin:
    """ A servo and not a console """

    @property
    def second_term(self):
        return "servo"

    @property
    def is_console(self):
        return False

    @property
    def is_servo(self):
        return True


class DomainLists:
    """ A DomainLists keep four lists of Domain objects and can find the correct list """
    def __init__(self):
        self.block_servos = []
        self.turnout_servos = []
        self.block_consoles = []
        self.turnout_consoles = []

    def append(self, item, domain=None):
        if domain is None:
            domain = item
        self.domain_list(domain).append(item)

    def domain_list(self, domain):
        if domain.is_servo:
            if domain.is_block:
                return self.block_servos
            else:
                return self.turnout_servos
        else:
            if domain.is_block:
                return self.block_consoles
            else:
                return self.turnout_servos
