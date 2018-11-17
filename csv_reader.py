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

    SONS_WIFE = "Son's wife"
    DAUGHTERS_HUSBAND = "Daughter's husband"
    WIFES_FATHER = "Wife's father"
    WIFES_MOTHER = "Wife's mother"
    HUSBANDS_FATHER = "Husband's father"
    HUSBANDS_MOTHER = "Husband's mother"

    HUSBANDS_BROTHER = "Husband's brother"
    HUSBANDS_SISTER = "Husband's sister"
    WIFES_BROTHER = "Wife's brother"
    WIFES_SISTER = "Wifes' sister"

    BROTHERS_WIFE = "Brother's wife"
    SISTERS_HUSBAND = "Sister's husband"

    MOTHERS_BROTHER = "Mother's brother"
    MOTHERS_SISTER = "Mother's sister"
    FATHERS_BROTHER = "Father's brother"
    FATHERS_SISTER = "Father's sister"

    BROTHERS_SON = "Brother's son"
    BROTHERS_DAUGHTER = "Brother's daughter"
    SISTERS_SON = "Sister's son"
    SISTERS_DAUGHTER = "Sister's daughter"


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
