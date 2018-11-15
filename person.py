import json

PEOPLE_FILENAME = 'people.json'


class Person():
    def __init__(self, id, name=None, spouse=None, parents=None):
        self.id = id
        self.name = name
        self.spouse = spouse
        self.parents = parents if parents is not None else set([])

    def __str__(self):
        return '{}: {}'.format(self.id, self.name)


class PersonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Person):
            return {
                'id': obj.id,
                'name': obj.name,
                'spouse': obj.spouse.id if obj.spouse else None,
                'parents': [parent.id for parent in obj.parents],
            }
        return json.JSONEncoder.default(self, obj)


def load_people():
    with open(PEOPLE_FILENAME, 'r') as people_file:
        raw_people = json.load(people_file)

    people = {}
    for raw_person in raw_people:
        people[raw_person['id']] = Person(
            raw_person['id'],
            name=raw_person['name'],
        )

    for raw_person in raw_people:
        person = people[raw_person['id']]
        person.spouse = people[raw_person['spouse']] if raw_person.get('spouse') else None
        person.parents = set([people[parent_id] for parent_id in raw_person['parents']])

    return people


def save_people(people):
    with open(PEOPLE_FILENAME, 'w') as people_file:
        json.dump(list(people), people_file, cls=PersonEncoder, indent=2)
