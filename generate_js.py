import json

from person import load_people
from person import load_people

TEMPLATE = '''
var familyNetwork = {{
    nodes: {nodes_json},
    edges: {edges_json}
}};
'''

people = load_people()
people_values = {id: 1 for id in people.keys()}

for id, person in people.items():
    if person.spouse:
        people_values[person.spouse.id] += 2
    for parent in person.parents:
        people_values[id] += 2
        people_values[parent.id] += 2

nodes = [
    {
        'id': person.id, 
        'label': person.name,
        'value': people_values[person.id],
    }
    for person in people.values()
]


def get_parental_edge(person, parent):
    return {
        'from': person.id,
        'to': parent.id,
        'arrows': 'to',
        'color': {
            'color': 'black'
        },
    }


def get_spouse_edge(person, spouse):
    return {
        'from': person.id,
        'to': spouse.id,
        'color': {
            'color': 'lightgreen'
        },
    }


edges = []
processed_spouses = set([])

for person in people.values():
    for parent in person.parents:
        edges.append(get_parental_edge(person, parent))
    if person.spouse and person not in processed_spouses:
        edges.append(get_spouse_edge(person, person.spouse))
        processed_spouses.add(person.spouse)


print("Generated {} nodes and {} edges.".format(len(nodes), len(edges)))

generated_js = TEMPLATE.format(
    nodes_json=json.dumps(nodes, indent=2),
    edges_json=json.dumps(edges, indent=2),
)

with open('family-network.js', 'w') as family_network_file:
    family_network_file.write(generated_js)

