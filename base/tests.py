from django.test import TestCase
from .models import Project, Profile, Rating
from django.contrib.auth.models import User

class AwwardsClone(TestCase):
    @classmethod
    def setUpTestData(cls):
        '''
        The setup method will run before each test case
        '''
        cls.user = User.objects.create_user(
            username='lemmy',
            email='lemmy@lemmy.com',
            password='lemmy1234'
        )

        cls.profile = Profile.objects.get(id=1)

        cls.project = Project.objects.create(
            title='Project Title',
            image='image/link',
            description='Today is a good day',
            live_link='https://www.lemmy.com',
            user_project=Profile.objects.get(id=1),
        )

        cls.rating = Rating.objects.create(
            creativity = 9,
            design = 7,
            usability = 8,
            content = 9,
            project = Project.objects.get(id=1),
            rated_by = User.objects.get(username='lemmy')
        )

    def tearDown(self):
        '''
        The teardown method does the cleanup after each test has run.
        '''
        User.objects.all().delete()
        Profile.objects.all().delete()
        Project.objects.all().delete()
        Rating.objects.all().delete()

    def test_instance(self):
        '''
        Test the instance of each object
        '''
        self.assertTrue(isinstance(self.user, User))
        self.assertTrue(isinstance(self.profile, Profile))
        self.assertTrue(isinstance(self.project, Project))
        self.assertTrue(isinstance(self.rating, Rating))

    def test_save_objects(self):
        '''
        test_save_image test case to test if the image object is saved into
        the db.
        '''
        self.project_two = Project.objects.create(
            title='Project Title 2',
            image='image/link/2',
            description='Today is a better day',
            live_link='https://www.lemmy2.com',
            user_project=Profile.objects.get(id=1),
        )
        self.project_two.save_project()

        projects = Project.objects.all()
        self.assertEqual(len(projects), 2)

    def test_delete_objects(self):
        '''
        test_delete_image test case to test if the image object is removed from
        the db.
        '''
        self.project.delete_project()
        posts = Project.objects.all()
        self.assertEqual(len(posts), 0)

    def test_get_average_rate(self):
        '''
        test_get_average_rate test case to test if the average rate returned from
        the get_average method is correct
        '''
        rate = self.rating.get_average()
        self.assertEqual(rate, str(8.25))
