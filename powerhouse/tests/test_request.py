from django.test import TestCase
from django.test import Client

class TreeTest(TestCase):
    def setUp(self):
        self.client = Client()

    def testPrune(self):
        response = self.client.get('/tree/input?indicator_ids[]=31&indicator_ids[]=32&indicator_ids[]=1')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            [{"id": 2,
                "name": "Demographics",
                "sub_themes": [{"categories": [{"id": 11,
                    "indicators": [{"id": 1, "name": "total"}],
                    "name": "Crude death rate",
                    "unit": "(deaths per 1000 people)"}],
                    "id": 4,
                    "name": "Births and Deaths"}]},
                {"id": 3,
                "name": "Jobs",
                "sub_themes": [{"categories": [{"id": 23,
                    "indicators": [{"id": 31, "name": "Total"},
                    {"id": 32, "name": "Female"}],
                    "name": "Unemployment rate, 15–24 years, usual",
                    "unit": "(percent of labor force)"}],
                    "id": 8,
                    "name": "Unemployment"}]}]
        )

    def testPruneDiffCat(self):
        response = self.client.get('/tree/input?indicator_ids[]=166&indicator_ids[]=7&indicator_ids[]=4')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            [{"id": 2,
                "name": "Demographics",
                "sub_themes": [{"categories": [{"id": 12,
                    "indicators": [{"id": 4, "name": "0-14 or 65+ years"}],
                    "name": "Dependency ratio",
                    "unit": "(percent)"},
                    {"id": 13,
                    "indicators": [{"id": 7, "name": "All ages"}],
                    "name": "Gender ratio",
                    "unit": "(percent)"}],
                    "id": 5,
                    "name": "Age and Sex"}]},
                {"id": 10,
                "name": "Health",
                "sub_themes": [{"categories": [{"id": 90,
                    "indicators": [{"id": 166, "name": "Male"}],
                    "name": "Under-five mortality rate",
                    "unit": "(deaths per 1,000 live births)"}],
                    "id": 34,
                    "name": "Mortality and morbidity"}]}]
        )

    def testPruneDiffSthme(self):
        response = self.client.get('/tree/input?indicator_ids[]=329&indicator_ids[]=308&indicator_ids[]=310&indicator_ids[]=1')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            [{"id": 2,
                "name": "Demographics",
                "sub_themes": [{"categories": [{"id": 10,
                    "indicators": [{"id": 308, "name": "Total"}],
                    "name": "Crude birth rate",
                    "unit": "(live births per 1000 people)"},
                    {"id": 11,
                    "indicators": [{"id": 1, "name": "total"}],
                    "name": "Crude death rate",
                    "unit": "(deaths per 1000 people)"}],
                    "id": 4,
                    "name": "Births and Deaths"},
                {"categories": [{"id": 15,
                    "indicators": [{"id": 310, "name": "Total"}],
                    "name": "Scheduled Tribe (ST)",
                    "unit": "(percent)"}],
                    "id": 6,
                    "name": "Religion and social groups"}]},
                {"id": 10,
                "name": "Health",
                "sub_themes": [{"categories": [{"id": 77,
                    "indicators": [{"id": 329, "name": "Total"}],
                    "name": "Wasting",
                    "unit": "(percent of children, 0-4 years)"}],
                    "id": 31,
                    "name": "Nutrition"}]}]
        )

    def testEmptyIndicatorIds(self):
        response = self.client.get('/tree/input?')
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'error': 'check your input'}
        )

    def testInvalidTreeSource(self):
        response = self.client.get('/tree/test?indicator_ids[]=32')
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'error': 'Requested tree source is not available'}
        )