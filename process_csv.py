import sys

from person import Person
from person import save_people
from csv_reader import read_csv
from csv_reader import Relation

CSV_FILENAME = sys.argv[1]

COMMON_PARENT_NAME = 'NO NAME PARENT'
NEW_CHILD_NAME = 'NO NAME PERSON'


relationships = read_csv(CSV_FILENAME)

people = {}
name_to_person = {}
next_person_id = 1


RELATION_ORDER = {
    Relation.FATHER: 0,
    Relation.MOTHER: 0,
    Relation.HUSBAND: 0,
    Relation.WIFE: 0,
    Relation.SON: 1,
    Relation.DAUGHTER: 1,
    Relation.BROTHER: 10,
    Relation.SISTER: 10,
    Relation.SONS_WIFE: 20,
    Relation.DAUGHTERS_HUSBAND: 20,
    Relation.WIFES_FATHER: 21,
    Relation.WIFES_MOTHER: 21,
    Relation.HUSBANDS_FATHER: 21,
    Relation.HUSBANDS_MOTHER: 21,
}


def create_person(name):
    global next_person_id
    person = Person(
        id=next_person_id,
        name=name,
    )
    next_person_id += 1

    people[person.id] = person
    name_to_person[name] = person

    return person


def get_or_create_person(name):
    if name in name_to_person:
        return name_to_person[name]
    return create_person(name)


def make_siblings(person, relative):
    if not person.parents and not relative.parents:
        common_parent = create_person(COMMON_PARENT_NAME)
        person.parents.add(common_parent)
        relative.parents.add(common_parent)
        return

    all_parents = person.parents.union(relative.parents)
    person.parents = all_parents
    relative.parents = all_parents


def make_child_in_law(person, relative):
    if person.spouse:
        if relative in person.spouse.parents:
            return
        person.spouse.parents.add(relative)
        return

    new_child = create_person(NEW_CHILD_NAME)
    person.spouse = new_child
    new_child.parents.add(relative)

relationships = sorted(relationships, key=lambda relationship: RELATION_ORDER[relationship.relation])

for relationship in relationships:
    person = get_or_create_person(relationship.person)
    relative = get_or_create_person(relationship.relative)

    if relationship.relation in [Relation.FATHER, Relation.MOTHER]:
        relative.parents.add(person)
    
    if relationship.relation in [Relation.SON, Relation.DAUGHTER]:
        person.parents.add(relative)
    
    if relationship.relation in [Relation.HUSBAND, Relation.WIFE]:
        person.spouse = relative
        relative.spouse = person

    if relationship.relation in [Relation.BROTHER, Relation.SISTER]:
        make_siblings(person, relative)

    if relationship.relation in [Relation.SONS_WIFE, Relation.DAUGHTERS_HUSBAND]:
        make_child_in_law(person, relative)
    
    if relationship.relation in [Relation.WIFES_FATHER, Relation.WIFES_MOTHER, Relation.HUSBANDS_FATHER, Relation.HUSBANDS_MOTHER,]:
        make_child_in_law(relative, person)

print('{} relationships processed'.format(len(relationships)))

save_people(people.values())
