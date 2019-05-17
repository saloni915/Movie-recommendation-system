from .models import *
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
import math
import numpy as np
import pandas as pd
import random
from CFModel import CFModel
from django.core.files.storage import FileSystemStorage
import tensorflow as tf

flag=False

def test(request):
    alert={
        "usernames": request.session.get('username')
    }
    return render(request, 'test.html',alert)

def contactus(request):
    return render(request, 'contactus.html')

def trend(request):
    username=request.session.get('username')
    if(username==None):
        return redirect('../signin')
    b=User.objects.get(user_email=username)
    print(b.user_id)
    tf.reset_default_graph()
    ratings = pd.read_csv('ratings.csv', sep='\t', encoding='latin-1',usecols=['user_id', 'movie_id', 'user_emb_id', 'movie_emb_id', 'rating'])
    users = pd.read_csv('users.csv', sep='\t', encoding='latin-1', usecols=['user_id', 'gender', 'zipcode', 'age_desc', 'occ_desc'])
    movies = pd.read_csv('movies.csv', sep='\t', encoding='latin-1',usecols=['movie_id', 'title', 'genres'])
    max_userid = ratings['user_id'].drop_duplicates().max()
    max_movieid = ratings['movie_id'].drop_duplicates().max()
    K_FACTORS = 100
    trained_model = CFModel(max_userid, max_movieid, K_FACTORS)
    # Load weights
    trained_model.load_weights('weights.h5')
    TEST_USER=b.user_id
    users[users['user_id'] == TEST_USER]
    user_ratings = ratings[ratings['user_id'] == TEST_USER][['user_id', 'movie_id', 'rating']]
    def predict_rating(user_id, movie_id):
        return trained_model.rate(user_id - 1, movie_id - 1)
    user_ratings['prediction'] = user_ratings.apply(lambda x: predict_rating(TEST_USER, x['movie_id']), axis=1)
    print(user_ratings.sort_values(by='rating', ascending=False).merge(movies,on='movie_id',how='inner',suffixes=['_u', '_m']).head(10))
    recommendations = ratings[ratings['movie_id'].isin(user_ratings['movie_id']) == False][['movie_id']].drop_duplicates()
    recommendations['prediction'] = recommendations.apply(lambda x: predict_rating(TEST_USER, x['movie_id']), axis=1)
    r=recommendations.sort_values(by='prediction',
                          ascending=False).merge(movies,
                                                 on='movie_id',
                                                 how='inner',
                                                 suffixes=['_u', '_m']).head(10)
    print(r)
    a=[]
    for i in r.get_values():
        a.extend(list(Movies.objects.filter(movie_id=i[0])))
    return render(request, 'trend.html', {'queryset': a,'recommendation':r.get_values()})

def userlogout(request):
    if request.method == 'POST':
        del request.session['username']
        return redirect('../signin/')
    else:
        return redirect('..a/')

def navigationbar(request):
    return render(request, 'navigationbar.html')

def history(request):
    return render(request, 'history.html')

def aboutchannel(request):
    return render(request, 'aboutchannel.html')

def channelvedio(request):
    return render(request, 'channelvedio.html')

def trending(request):
    alert={
        "username": request.session.get('username')
    }
    print(alert['username'])
    ratings = pd.read_csv('ratings.csv', sep='\t', encoding='latin-1', 
    usecols=['user_id', 'movie_id','rating'])
    movies = pd.read_csv('movies.csv', sep='\t', encoding='latin-1', 
    usecols=['movie_id', 'title', 'genres'])
    trend=ratings[ratings['rating']==5].drop_duplicates(subset=['user_id']).merge(movies,on='movie_id',how='inner',suffixes=['_r','_m']).drop_duplicates(subset=['movie_id']).head(20)
    print(trend)
    a=[]
    for i in trend.get_values():
        a.extend(list(Movies.objects.filter(movie_id=i[1])))
    return render(request, 'trending.html',{'queryset':trend.get_values(),'movi':a})

def genre(request):
    alert={
        "gen":request.GET.get("g")
    }
    a=list(Movies.objects.filter(movie_genre__regex=alert['gen']))
    return render(request,'genrewise.html',{'queryset':a})

def register(request):
    alert = {
        "username": request.GET.get("username"),
        "useremail": request.GET.get("user_email")
    }
    if request.method == 'POST':
        if User.objects.filter(user_id=request.POST['username']):
            alert['username'] = "Username already exists"
        elif User.objects.filter(user_email=request.POST['user_email']):
            alert['useremail'] = "Email already exists"
        else:
            post = User()
            post.user_id = request.POST.get("username")
            post.user_name = request.POST.get("user_name")
            post.user_email = request.POST.get("user_email")
            post.user_password = request.POST.get("password")
            post.save()
            return redirect('../signin')
    return render(request, 'signup.html', alert)

def signin(request):
    alert = {
        "userid": request.GET.get("username"),
    }
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            User.objects.get(user_email=username, user_password=password)
            request.session['username'] = username
            return redirect('../trend')
        except User.DoesNotExist:
            alert['userid'] = "Email/Password are incorrect"
            return render(request, 'signin.html', alert)
    return render(request, 'signin.html', alert)

def mainpage(request):
        a = Videos.objects.all()
        return render(request, 'mainpage.html', {'queryset': a})

def upload(request):
    if request.method == 'POST':
        post = Videos()
        post.video_name = request.POST.get('video_name')
        post.video_upload = request.POST.get('video')
        post.description = request.POST.get('description')
        post.video_thumbnail = request.POST.get('image')
        post.video_duration = request.POST.get('duration')
        post.category = request.POST.get('category')
        post.save()
        return render(request, 'upload.html')

    else:
        return render(request, 'upload.html')

def createchannel(request):
    alert = {
        "channel_name": request.GET.get("Channel_name"),
        "user_email": request.GET.get("user_email"),
        "facebook": request.GET.get("facebook"),
        "instagram": request.GET.get("instagram")
    }
    if request.method == 'POST':
        if Channel.objects.filter(channel_name=request.POST['Channel_name']):
            alert['username'] = "Channel Name already exist"
        elif Channel.objects.filter(email=request.POST['user_email']):
            alert['user_email'] = "Channel already exists"
        elif Channel.objects.filter(facebook_link=request.POST['facebook']):
                alert['facebook'] = "Channel already exist"
        elif Channel.objects.filter(instagram_link=request.POST['instagram']):
                alert['instagram'] = "Channel already exists"
        else:
            post = Channel()
            post.channel_name = request.POST.get('Channel_name')
            post.channel_description = request.POST.get('description')
            post.email = request.POST.get('user_email')
            post.facebook_link = request.POST.get('facebook')
            post.instagram_link = request.POST.get('instagram')
            post.save()
            return render(request, 'createchannel.html', alert)
        return render(request, 'createchannel.html', alert)
    else:
        return render(request,'createchannel.html', alert)


def search(request):
    return render(request, 'searchresults.html')


def createpost(request):
    if request.method == 'POST':
        query = request.POST['search']

        if query:
            match = Videos.objects.filter(video_name__icontains=query)
            if match:
                return render(request, 'searchpage.html', {'sr': match})
            else:
                return render(request, 'searchpage.html')
    return render(request, 'searchpage.html')

def vidpg(request,id):
    result = Videos.objects.filter(id =id)
    print(result[0])
    # return HttpResponse(result)
    return render(request, 'mainpage.html',{ 'vid' : result[0] })

def teraghat(request):
    alert={
    "url":request.GET.get('url')
    }
    print(alert["url"])
    return render(request, 'teraghat.html', {'url':alert['url']})



