import unittest
from model.amenity import Amenity

class TestAmenity(unittest.TestCase):

    def test_create_amenity(self):
        amenity = Amenity("Pool", "A large pool")
        self.assertEqual(amenity.name, "Pool")
        self.assertEqual(amenity.description, "A large pool")
        self.assertIsNotNone(amenity.id)
        self.assertIsNotNone(amenity.created_at)
        self.assertIsNotNone(amenity.updated_at)

if __name__ == '__main__':
    unittest.main()
