import collections
import configparser
import logging
import os

import yaml

"""Load a testset."""


class Question(object):
    """Represent testset area question as an object."""

    def __init__(self, filename, area):
        logging.info(f"Creating question from {filename}")
        self._meta_path = filename
        self.area = area

        self._name = None
        self._type = None
        self._timeout = None
        self._question = None
        self._answers = None
        self._correct = None

    def load_meta(self):
        with open(self._meta_path, 'r') as fp:
            metadata = yaml.load(fp, Loader=yaml.Loader)
            self._name = os.path.basename(self._meta_path).split('.')[0]
            self._type = metadata['type']
            self._timeout = int(metadata['timeout'])
            self._question = metadata['question']
            self._answers = metadata['answers']
            self._correct = metadata['correct']

    def dump_meta(self):
        with open(self._meta_path, 'w') as fp:
            data = {
                "type": self.type,
                "timeout": self.timeout,
                "question": self.question,
                "answers": self.answers,
                "correct": self.correct,
            }
            yaml.dump(data, fp)

    def __repr__(self):
        return f"<Question({self.name}, {self.type}, {self.timeout})>"

    @property
    def whoami(self):
        return f"{self.area.whoami}/{self.name}"

    @property
    def name(self):
        if self._name is None:
            self.load_meta()
        return self._name

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
        logging.debug(f"Linting question from {self._meta_path}")
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

    def dump(self):
        logging.debug(f"Dumping question to {self._meta_path}")
        self.dump_meta()

    @classmethod
    def convert(cls, from_dir, to_file):
        """Convert old-formated testset area question and dump to new file."""
        logging.info(f"Converting question from {from_dir} to {to_file}")
        self = cls(to_file)

        config = configparser.ConfigParser()
        config.read(os.path.join(from_dir, "config"))
        assert "question" in config

        self._type = config["question"]["type"]
        if self._type != "abc":
            raise Exception(f"Sorry, I do not know how to handle question with type {self._type}. Skipping it")
        self._timeout = int(config["question"]["timeout"])
        self._question = config["question"]["question"]
        if self._question.startswith("@"):
            with open(os.path.join(from_dir, self._question[1:])) as fp:
                self._question = fp.read().strip()
        self._answers = {}
        with open(os.path.join(from_dir, config["question"]["answers"][1:])) as fp:
            for line in fp:
                answer_id = line[0]
                answer_text = line[2:].strip()
                self._answers[answer_id] = answer_text
        self._correct = config["question"]["correct"]

        self.dump()

        return self


class QuestionsDict(collections.OrderedDict):
    """Lazily load questions."""

    def __init__(self, dirname, area):
        self._dirname = dirname
        self._area = area
        self._keys_loaded = False

    def __getitem__(self, key):
        if key not in super().keys() or super().__getitem__(key) is None:
            p = os.path.join(self._dirname, key + '.yaml')
            question = Question(p, self._area)
            super().__setitem__(key, question)
        return super().__getitem__(key)

    def keys(self):
        if not self._keys_loaded:
            for item in os.listdir(self._dirname):
                if os.path.isfile(os.path.join(self._dirname, item)) \
                   and item.endswith('.yaml') \
                   and item != 'metadata.yaml':
                    key = item.split('.')[0]
                    super().__setitem__(key, None)
            self._keys_loaded = True
        return super().keys()

    def values(self):
        for key in self.keys():
            yield self.__getitem__(key)

    @classmethod
    def convert(cls, from_dir, to_dir):
        """Dispatch conversion of questions from old to new format."""
        self = cls(to_dir)

        for item in os.listdir(from_dir):
            if os.path.exists(os.path.join(from_dir, item, 'config')):
                question_from = os.path.join(from_dir, item)
                question_to = os.path.join(to_dir, item + '.yaml')

                try:
                    question = Question.convert(question_from, question_to)
                except Exception as e:
                    logging.warning(e)
                    continue

                self.__setitem__(os.path.basename(question_to), question)

        self._keys_loaded = True

        return self


class Area(object):
    """Represent testset area as an object."""

    def __init__(self, dirname, testset):
        logging.info(f"Creating area from {dirname}")
        self._dirname = dirname
        self.testset = testset
        self._meta_path = os.path.join(self._dirname, 'metadata.yaml')

        self._name = None
        self._questions_to_ask = None
        self.questions = QuestionsDict(self._dirname, self)

    def load_meta(self):
        with open(self._meta_path, 'r') as fp:
            metadata = yaml.load(fp, Loader=yaml.Loader)
            self._name = os.path.basename(self._dirname)
            self._questions_to_ask = int(metadata['questions_to_ask'])

    def dump_meta(self):
        with open(self._meta_path, 'w') as fp:
            data = {
                "questions_to_ask": self._questions_to_ask,
            }
            yaml.dump(data, fp)

    def __gt__(self, other):
        return self._dirname > other._dirname

    def __repr__(self):
        return f"<Area({self._dirname}, {self.questions_to_ask})>"

    @property
    def whoami(self):
        return f"{self.testset.whoami}/{self.name}"

    @property
    def name(self):
        if self._name is None:
            self.load_meta()
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

    def dump(self):
        logging.debug(f"Dumping area to {self._dirname}")
        self.dump_meta()

        for question in self.questions.values():
            question.dump()

    @classmethod
    def convert(cls, from_dir, to_dir):
        """Convert old-formated testset area and dump to new directory."""
        logging.info(f"Converting area from {from_dir} to {to_dir}")
        self = cls(to_dir)

        with open(os.path.join(from_dir, 'questions_to_test.txt')) as fp:
            self._questions_to_ask = int(fp.read().strip())

        self.questions = QuestionsDict.convert(from_dir, to_dir)

        self.dump()

        return self


class AreasDict(collections.OrderedDict):
    """Lazily load areas."""

    def __init__(self, dirname, testset):
        self._dirname = dirname
        self._testset = testset
        self._keys_loaded = False

    def __getitem__(self, key):
        if key not in super().keys() or super().__getitem__(key) == None:
            area = Area(os.path.join(self._dirname, key), self._testset)
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

    @classmethod
    def convert(cls, from_dir, to_dir):
        """Dispatch conversion of areas from old to new format."""
        self = cls(to_dir)

        for item in os.listdir(from_dir):
            if os.path.exists(os.path.join(from_dir, item, 'questions_to_test.txt')):
                area_from = os.path.join(from_dir, item)
                area_to = os.path.join(to_dir, item)

                os.mkdir(area_to)

                area = Area.convert(area_from, area_to)
                self.__setitem__(os.path.basename(item), area)

        self._keys_loaded = True

        return self


class TestSet(object):
    """Represent testset as an object."""

    def __init__(self, dirname):
        logging.info(f"Creating testset from {dirname}")
        self._dirname = dirname
        self._meta_path = os.path.join(self._dirname, 'metadata.yaml')

        self._name = None
        self._description = None
        self._version = None
        self.areas = AreasDict(self._dirname, self)

    def __repr__(self):
        return f"<TestSet({self._dirname}, {self.version})>"

    @property
    def whoami(self):
        return self.name

    @property
    def name(self):
        if self._name is None:
            self.load_meta()
        return self._name

    @property
    def description(self):
        if self._description is None:
            self.load_meta()
        return self._description

    @property
    def version(self):
        if self._version is None:
            self.load_meta()
        return self._version

    def load_meta(self):
        with open(self._meta_path, 'r') as fp:
            metadata = yaml.load(fp, Loader=yaml.Loader)
            self._name = os.path.basename(os.path.dirname(self._meta_path))
            self._description = metadata['description']
            self._version = int(metadata['version'])

    def dump_meta(self):
        data = {
            "description": self.description,
            "version": self.version,
        }
        with open(self._meta_path, 'w') as fp:
            yaml.dump(data, fp)

    def lint(self):
        logging.debug(f"Linting testset from {self._dirname}")
        assert self.version > 0

        assert len(self.areas.keys()) > 0
        for area in self.areas.values():
            area.lint()

    def show(self):
        print(f"Description: {self.description}")
        print(f"Version: {self.version}")
        print("Areas:")
        for area in self.areas.values():
            area.show()

    def dump(self):
        logging.debug(f"Dumping testset to {self._dirname}")
        self.dump_meta()

        for area in self.areas.values():
            area.dump()

    @classmethod
    def convert(cls, from_dir, to_dir):
        """Convert old-formated testset and dump to new directory."""
        logging.info(f"Converting testset from {from_dir} to {to_dir}")
        self = cls(to_dir)

        with open(os.path.join(from_dir, "description")) as fp:
            self._name = fp.read().strip()
        self._version = 1

        self.areas = AreasDict.convert(from_dir, to_dir)

        self.dump()

        return self
