# from django.test import TestCase
# from .models import ProfilePrediction, Prediction
# from django.contrib.auth.models import User

# class PredictionModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.user = User.objects.create_user(username='gauthier3', password='azerty1234!')

#     def setUp(self):
#         self.profilepredict = ProfilePrediction.objects.create(
#             user = self.user,
#             age=25,
#             sex='Male',
#             bmi=5,
#             children=2,
#             smoker=1,
#             region='Northeast'
#         )

#     def test_profileprediction_age(self):
#         self.assertIsInstance(self.profilepredict, ProfilePrediction)
#         self.assertEqual(self.profilepredict.age, 25)
#         self.assertGreaterEqual(self.profilepredict.age, 18)

#     def test_profileprediction_bmi(self):
#         self.assertIsInstance(self.profilepredict, ProfilePrediction)
#         self.assertEqual(self.profilepredict.bmi, 5)
#         self.assertGreaterEqual(self.profilepredict.bmi, 4)