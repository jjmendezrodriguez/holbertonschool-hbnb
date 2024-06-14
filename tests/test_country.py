import unittest
from model.country import Country

class TestCountry(unittest.TestCase):

    def test_create_country(self):
        country = Country("Sample Country", "SC")
        self.assertEqual(country.name, "Sample Country")
        self.assertEqual(country.code, "SC")
        self.assertIsNotNone(country.id)
        self.assertIsNotNone(country.created_at)
        self.assertIsNotNone(country.updated_at)

if __name__ == '__main__':
    unittest.main()
