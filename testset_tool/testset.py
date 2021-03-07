import collections
import logging
import os

import yaml

"""Load a testset."""


class Question(object):
    """Represent testset area question as an object."""

    def __init__(self, filename):
        logging.info(f"Creating question from {filename}")
        self._filename = filename

        self._type = None
        self._timeout = None
        self._question = None
        self._answers = None
        self._correct = None

    def load_meta(self):
        with open(self._filename, 'r') as fp:
            metadata = yaml.load(fp, Loader=yaml.Loader)
            self._type = metadata['type']
            self._timeout = int(metadata['timeout'])
            self._question = metadata['question']
            self._answers = metadata['answers']
            self._correct = metadata['correct']

    def __repr__(self):
        return f"<Question({self.filename}, {self.type}, {self.timeout})>"

    @property
    def type(self):
        if self._type is None:
            self.load_meta()
        return self._type

    @property
    def timeout(self):
        if self._timeout is None:
            self.load_meta()
        return self._timeout

    @property
    def question(self):
        if self._question is None:
            self.load_meta()
        return self._question

    @property
    def answers(self):
        if self._answers is None:
            self.load_meta()
        return self._answers

    @property
    def correct(self):
        if self._correct is None:
            self.load_meta()
        return self._correct

    def lint(self):
        logging.debug(f"Linting question from {self._filename}")
        assert self.type == 'abc'
        assert self.timeout > 0
        assert isinstance(self.question, str) and len(self.question) > 0
        assert isinstance(self.answers, dict)
        assert self.correct in self.answers

    def show(self):
        print(f"      - Type: {self.type}")
        print(f"        Timeout: {self.timeout}")
        print(f"        Question: {self.question}")
        print(f"        Correct: {self.correct}")
        print("        Answers:")
        for answer, value in self.answers.items():
            print(f"            {answer}) {value}")


class QuestionsDict(collections.OrderedDict):
    """Lazily load questions."""

    def __init__(self, dirname):
        self._dirname = dirname
        self._keys_loaded = False

    def __getitem__(self, key):
        if super().__getitem__(key) is None:
            question = Question(os.path.join(self._dirname, key))
            super().__setitem__(key, question)
        return super().__getitem__(key)

    def keys(self):
        if not self._keys_loaded:
            for item in os.listdir(self._dirname):
                if os.path.isfile(os.path.join(self._dirname, item)) \
                   and (item.endswith('.yaml') or item.endswith('.yml')) \
                   and item != 'metadata.yaml':
                    super().__setitem__(item, None)
            self._keys_loaded = True
        return super().keys()

    def values(self):
        for key in self.keys():
            yield self.__getitem__(key)


class Area(object):
    """Represent testset area as an object."""

    def __init__(self, dirname):
        logging.info(f"Creating area from {dirname}")
        self._dirname = dirname
        self._name = os.path.basename(dirname)

        self._questions_to_ask = None
        self.questions = QuestionsDict(self._dirname)

    def load_meta(self):
        with open(os.path.join(self._dirname, 'metadata.yaml'), 'r') as fp:
            metadata = yaml.load(fp, Loader=yaml.Loader)
            self._questions_to_ask = int(metadata['questions_to_ask'])

    def __gt__(self, other):
        return self._dirname > other._dirname

    def __repr__(self):
        return f"<Area({self.basename}, {self.questions_to_ask})>"

    @property
    def name(self):
        return self._name

    @property
    def questions_to_ask(self):
        if self._questions_to_ask is None:
            self.load_meta()
        return self._questions_to_ask

    def lint(self):
        logging.debug(f"Linting area from {self._dirname}")
        assert len(self.name) > 0
        assert self.questions_to_ask > 0
        assert self.questions_to_ask <= len(self.questions.keys())

        for question in self.questions.values():
            question.lint()

    def show(self):
        print(f"  - Area: {self.name}")
        print(f"    Questions to ask: {self.questions_to_ask}")
        print("    Questions:")
        for question in self.questions.values():
            question.show()


class AreasDict(collections.OrderedDict):
    """Lazily load areas."""

    def __init__(self, dirname):
        self._dirname = dirname
        self._keys_loaded = False

    def __getitem__(self, key):
        if super().__getitem__(key) is None:
            area = Area(os.path.join(self._dirname, key))
            super().__setitem__(key, area)
        return super().__getitem__(key)

    def keys(self):
        if not self._keys_loaded:
            for item in os.listdir(self._dirname):
                if os.path.exists(os.path.join(self._dirname, item, 'metadata.yaml')):
                    super().__setitem__(os.path.basename(item), None)
            self._keys_loaded = True
        return super().keys()

    def values(self):
        for key in self.keys():
            yield self.__getitem__(key)


class TestSet(object):
    """Represent testset as an object."""

    def __init__(self, dirname):
        logging.info(f"Creating testset from {dirname}")
        self._dirname = dirname

        self._name = None
        self._version = None
        self.areas = AreasDict(self._dirname)

    def __repr__(self):
        return f"<TestSet({self._dirname}, {self.version})>"

    @property
    def name(self):
        if self._name is None:
            self.load_meta()
        return self._name

    @property
    def version(self):
        if self._version is None:
            self.load_meta()
        return self._version

    def load_meta(self):
        with open(os.path.join(self._dirname, 'metadata.yaml'), 'r') as fp:
            metadata = yaml.load(fp, Loader=yaml.Loader)
            self._name = metadata['name']
            self._version = int(metadata['version'])

    def lint(self):
        logging.debug(f"Linting testset from {self._dirname}")
        assert self.version > 0

        assert len(self.areas.keys()) > 0
        for area in self.areas.values():
            area.lint()

    def show(self):
        print(f"Name: {self.name}")
        print(f"Version: {self.version}")
        print("Areas:")
        for area in self.areas.values():
            area.show()
