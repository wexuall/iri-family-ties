import csv
from enum import Enum
from typing import NamedTuple

class Relation(Enum):
    FATHER = 'Father'
    MOTHER = 'Mother'
    SON = 'Son'
    DAUGHTER = 'Daughter'
    HUSBAND = 'Husband'
    WIFE = 'Wife'
    BROTHER = 'Brother'
    SISTER = 'Sister'
    SONS_WIFE = 'Son\'s wife'
    DAUGHTERS_HUSBAND = 'Daughter\'s husband'
    WIFES_FATHER = 'Wife\'s father'
    WIFES_MOTHER = 'Wife\'s mother'
    HUSBANDS_FATHER = 'Husband\'s father'
    HUSBANDS_MOTHER = 'Husband\'s mother'


class Relationship(NamedTuple):
    person: str
    relative: str
    relation: str


def read_csv(filename):
    with open(filename, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')

        next(reader)

        supported_relations = [relation.value for relation in Relation]
        return [
            Relationship(
                person=row[0],
                relative=row[1],
                relation=Relation(row[2]),
            )
            for row in reader
            if row[3] != 'FLAG' and row[2] in supported_relations
        ]
