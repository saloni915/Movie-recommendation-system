from django.db import models
# Create your models here.


class User(models.Model):
    user_id = models.IntegerField(default=0, unique=True)
    user_name = models.CharField(max_length=50, blank=True, null=True, default="")
    user_email = models.EmailField(default="", max_length=50, unique=True)
    no_of_channels = models.IntegerField(default=0)
    user_password = models.CharField(default="",max_length=40)

    def __str__(self):
        return self.user_name


class Channel(models.Model):
    channel_videos = models.IntegerField(default=0)
    channel_name = models.CharField(max_length=40, unique=True)
    channel_subscribers = models.IntegerField(default=0)
    channel_description = models.TextField(default="")
    email = models.EmailField(default="", max_length=50, unique=True)
    facebook_link = models.CharField(max_length=100, default="", unique=True)
    instagram_link = models.CharField(max_length=100, default="", unique=True)

    def __str__(self):
        return self.channel_name


class History(models.Model):
    user_history = models.TextField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Videos(models.Model):
    video_name = models.CharField(max_length=100, default="")
    video_thumbnail = models.FileField(upload_to='vimages', null='true', blank='true', default="")
    video_description = models.TextField(null='true', blank='true', default="")
    video_upload = models.FileField(upload_to='videos', null='true', blank='true', default="")
    video_category = models.CharField(default="",max_length=40)
    video_date = models.DateTimeField(auto_now_add=True)
    video_views = models.IntegerField(default=0)
    video_duration = models.TimeField()
    video_likes = models.IntegerField(default=0)
    video_dislikes = models.IntegerField(default=0)
    list = [('E','Education'),
        ('p','politics'),
        ('E1','entertainment'),
        ('S','sports'),
        ('O', 'other'),
        ]
    category = models.CharField(max_length=2, choices=list, default="")


    def __str__(self):
        return self.video_name


class Comments(models.Model):
    video_comments = models.TextField()
    video_id = models.ForeignKey(Videos,on_delete=models.CASCADE)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.video_comments
    
class Movies(models.Model):
    movie_id=models.IntegerField(default=0,unique=True)
    movie_name=models.CharField(max_length=100, default="")
    movie_genre=models.CharField(max_length=100, default="")
    movie_img=models.FileField(upload_to='vimages', null='true', blank='true', default="")
    movie_link=models.URLField(max_length=128,db_index=True,unique=True,blank=True)
    
    def __str__(self):
        return self.movie_name