import json
from django.test import TestCase
from powerhouse.models import Tree

class PruneTest(TestCase):
    def setUp(self):
      with open('powerhouse/sample_data.json', 'r') as json_file:
        self.input = json.load(json_file)

    def test_prune(self):
        tree = Tree(self.input)
        tree.prune([1])
        self.assertEqual(
            tree.to_json()['themes'], [{
            "id": 2,
            "name": "Demographics",
            "sub_themes": [
            {
                "categories": [
                {
                    "id": 11,
                    "indicators": [
                    {
                        "id": 1,
                        "name": "total"
                    }
                    ],
                    "name": "Crude death rate",
                    "unit": "(deaths per 1000 people)"
                }
                ],
                "id": 4,
                "name": "Births and Deaths"
            }
            ]
        }])

        tree1 = Tree(self.input)
        tree1.prune([1, 31, 32, 329, 308, 310])
        self.assertEqual(
            tree1.to_json()['themes'], [{'id': 2,
            'name': 'Demographics',
            'sub_themes': [{'categories': [{'id': 10,
                'indicators': [{'id': 308, 'name': 'Total'}],
                'name': 'Crude birth rate',
                'unit': '(live births per 1000 people)'},
                {'id': 11,
                'indicators': [{'id': 1, 'name': 'total'}],
                'name': 'Crude death rate',
                'unit': '(deaths per 1000 people)'}],
                'id': 4,
                'name': 'Births and Deaths'},
            {'categories': [{'id': 15,
                'indicators': [{'id': 310, 'name': 'Total'}],
                'name': 'Scheduled Tribe (ST)',
                'unit': '(percent)'}],
                'id': 6,
                'name': 'Religion and social groups'}]},
            {'id': 3,
            'name': 'Jobs',
            'sub_themes': [{'categories': [{'id': 23,
                'indicators': [{'id': 31, 'name': 'Total'},
                {'id': 32, 'name': 'Female'}],
                'name': 'Unemployment rate, 15–24 years, usual',
                'unit': '(percent of labor force)'}],
                'id': 8,
                'name': 'Unemployment'}]},
            {'id': 10,
            'name': 'Health',
            'sub_themes': [{'categories': [{'id': 77,
                'indicators': [{'id': 329, 'name': 'Total'}],
                'name': 'Wasting',
                'unit': '(percent of children, 0-4 years)'}],
                'id': 31,
                'name': 'Nutrition'}]}])

        tree2 = Tree(self.input)
        tree2.prune([])
        self.assertEqual(
            tree2.to_json()['themes'], [])

        tree3 = Tree(self.input)
        tree3.prune([-1])
        self.assertEqual(
            tree3.to_json()['themes'], [])