from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User

class Profile(models.Model):
    user_profile = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = CloudinaryField('profile_photo', blank=True)
    bio = models.CharField(blank=True, max_length=150)
    facebook = models.URLField(blank=True, max_length=150)
    linkedln = models.URLField(blank=True, max_length=150)
    instagram = models.URLField(blank=True, max_length=150)
    twitter = models.URLField(blank=True, max_length=150)
    following = models.ManyToManyField('self', related_name='i_am_following', symmetrical=False, blank=True)
    followers = models.ManyToManyField('self', related_name='my_followers', symmetrical=False, blank=True)
    updated = models.DateTimeField(auto_now=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        ordering = ['updated', 'created']

    def __str__(self):
        return self.user_profile.username

class Project(models.Model):
    title = models.CharField(max_length=100)
    image = CloudinaryField('image')
    description = models.TextField()
    live_link = models.URLField(blank=True)
    user_project = models.ForeignKey(Profile ,on_delete=models.CASCADE)
    ratings = models.ManyToManyField('Rating',related_name='ratings', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['updated', 'created']

    def __str__(self):
        return self.title

class Rating(models.Model):
    creativity = models.IntegerField(default=5, help_text='value 1 to 10', validators=[MaxValueValidator(10),
            MinValueValidator(1)]
        )
    design = models.IntegerField(default=5, help_text='value 1 to 10', validators=[MaxValueValidator(10),
            MinValueValidator(1)]
        )
    usability = models.IntegerField(default=5, help_text='value 1 to 10', validators=[MaxValueValidator(10),
            MinValueValidator(1)]
        )
    content = models.IntegerField(default=5, help_text='value 1 to 10', validators=[MaxValueValidator(10),
            MinValueValidator(1)]
        )
    project = models.ForeignKey(Project ,on_delete=models.CASCADE)
    rated_by = models.ForeignKey(User ,on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['updated', 'created']

    def __str__(self):
        return f'rated by:{self.rated_by.username}'