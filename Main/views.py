from distutils.log import error
from multiprocessing import context
from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Busines,Favorite
# import messages
# Create your views here.
import  csv
import pandas as pd
import os

import json
# csv_file= os.path.join(os.path.dirname(__file__), 'results.csv')

# import user authentification django
from django.contrib.auth import authenticate , login,logout
# create a function login and create session
def login_user(request):
    # if session is not created
    if  request.session.has_key('USER'):
        # redirect to login page
        return redirect('home')
    # if get method
    if request.method == 'GET':
        # redirect to login page
        return render(request, 'login.html',{'title': 'Login'})
    # if post method
    if request.method == 'POST':
        # get the username and password from the form
        username = request.POST.get('username')
        password = request.POST.get('password')
        # authenticate the user
        user = authenticate(request, username=username, password=password)
        # if user is not None
        if user is not None:
            # login create session
            login(request, user)
            request.session['USER'] = username
            request.session.modified = True
            # redirect to home page
            return redirect('home')
        else:
            error="Username or Password is incorrect"
            # redirect to login page
            return render(request, 'login.html',{'title': 'Login','error':error})

# create a function logout and delete session
def logout_user(request):
    # delete session
    del request.session['USER']
    request.session.modified = True
    #logout
    logout(request)
    # redirect to login page
    return redirect('login')

def home(request):
    # if session is not created
    if not request.session.has_key('USER'):
        # redirect to login page
        return redirect('login')
    # fill_business()
    # get business
    business = Busines.objects.all()
    # cout the number of business
    nbr_business = business.count()
    # count business by status and stor values in a json 
    new = Busines.objects.filter(status=0).count()
    onhold = Busines.objects.filter(status=1).count()
    inprogress = Busines.objects.filter(status=2).count()
    completed = Busines.objects.filter(status=3).count()
    canceled = Busines.objects.filter(status=4).count()
    rejected = Busines.objects.filter(status=5).count()
    accepted = Busines.objects.filter(status=6).count()
    noresponse = Busines.objects.filter(status=7).count()
    # create a json
    status =""
    if new > 0:
        status += "[ {value:"+str(new)+",name:'New'}"
    if inprogress > 0:
        status += ",{value:"+str(inprogress)+",name:'In Progress'}"
    if onhold > 0:
        status += ",{value:"+str(onhold)+",name:'Onhold'}"
    if canceled > 0:
        status += ",{value:"+str(canceled)+",name:'Canceled'}"
    if accepted > 0:
        status += ",{value:"+str(accepted)+",name:'Accepted'}"
    if completed > 0:
        status += ",{value:"+str(completed)+",name:'Completed'}"
    if rejected > 0:
        status += ",{value:"+str(rejected)+",name:'Rejected'}"
    if noresponse > 0:
        status += ",{value:"+str(noresponse)+",name:'No Response'}]"


    # convert json to string
    status="<script> document.addEventListener('DOMContentLoaded', () => { echarts.init(document.querySelector('#trafficChart')).setOption({ tooltip: {  trigger: 'item' }, legend: {top: '5%',left: 'center'}, series: [{name: 'Statu :', type: 'pie',radius: ['40%', '70%'], avoidLabelOverlap: false,label: {  show: false,   position: 'center' },emphasis: { label: { show: true,fontSize: '18',fontWeight: 'bold'}},labelLine: {show: false}, data: "+status+"}]});}); </script>"
    
    favorites = Favorite.objects.all()

    context = {'title': 'Home','business':business,'status':status,'favorites':favorites,'nbr_business':nbr_business}
    return render(request, 'home.html', context)

def detail(request, id):
    # if session is not created
    if not request.session.has_key('USER'):
        # redirect to login page
        return redirect('login')
    busines = Busines.objects.get(id=id)
    favorite = Favorite.objects.filter(busines_id=id).exists()
    # get the next and the previous business
    next = Busines.objects.filter(id__gt=id).order_by('id').first()
    previous = Busines.objects.filter(id__lt=id).order_by('-id').first()
    pagination={}
    if previous:
        pagination['previous']=previous.id
    if next:
        pagination['next']=next.id

    context = {'title': 'Detail','busines':busines,'favorite':favorite,'pagination':pagination}
    return render(request, 'detail.html', context)

# add to Favorite functions
def favorite(request, id):
    # if session is not created
    if not request.session.has_key('USER'):
        # redirect to login page
        return redirect('login')
    favorite=Favorite()
    # if buisness alredy in Favorite delete it
    if Favorite.objects.filter(busines_id=id).exists():
        Favorite.objects.filter(busines_id=id).delete()
    else:
        # add to Favorite
        favorite.busines_id=id
        favorite.save()
    return redirect('detail', id=id)



def upload_csv(request):
    # if session is not created
    if not request.session.has_key('USER'):
        # redirect to login page
        return redirect('login')
    try:
        if request.method != 'POST':
            context = {'title': 'Add Business'}
            return render(request, 'upload_csv.html',context)
        csv_file = request.FILES["formFile"]
        print(csv_file)
        print(csv_file)
        if not csv_file.name.endswith('.csv'):
            error='File is not CSV type'
            context = {'title': 'Add Business | Error','error':error}
            return render(request, 'upload_csv.html', context)
        # if file is too large, return
        if csv_file.multiple_chunks():
            error='Uploaded file is too big (%.2f MB).' % (csv_file.size/(1000*1000),)
            context = {'title': 'Add Business | Error','error':error}
            return render(request, 'upload_csv.html', context)
            
        #fill Busines class from csv file 
        df = pd.read_csv(csv_file)
        # "Name","Fulladdress",Street,Municipality,Categories,Phone,"Phones",Review Count,Average Rating,"Review URL",Google Maps URL,Latitude,Longitude,Website,Domain,"Opening hours",Featured image
        for index, row in df.iterrows():
            try:
                busines = Busines()
                busines.name = row['Name']
                busines.fulladdress = row['Fulladdress']
                busines.street = row['Street']
                busines.municipality = row['Municipality']
                busines.categories = row['Categories']
                busines.phone = row['Phone']
                busines.phones = row['Phones']
                busines.review_count = row['Review Count']
                busines.average_rating = row['Average Rating']
                busines.review_url = row['Review URL']
                busines.google_maps_url = row['Google Maps URL']
                busines.latitude = row['Latitude']
                busines.longitude = row['Longitude']
                busines.website = row['Website']
                busines.domain = row['Domain']
                busines.opening_hours = row['Opening hours']
                busines.featured_image = row['Featured image']
                busines.save()
            except:
                pass

        # fille_data = csv_file.read().decode('UTF-8')
        # print(fille_data)
        # lines = fille_data.split("\n")
        
        # # loop over the lines and save them in db. If error , store as string and then display  
        # for line in lines:
        #     # scipe the first line
        #     # if line.startswith('Name'):
        #     #     continue
        #     row = line.split(",")
        #     # start from the second line
        #     if 'Name' not in row[0] :
        #         try:
        #                 print(row)
        #                 # create object
        #                 business = Busines()
        #                 # fill object
        #                 # remove " from string if exist
        #                 business.name = row[0].replace('"','')
        #                 business.fulladdress = row[1].replace('"','')
        #                 business.street = row[2].replace('"','')
        #                 business.municipality = row[3].replace('"','')
        #                 business.categories = row[4].replace('"','')
        #                 business.phone = row[5].replace('"','')
        #                 business.phones = row[6].replace('"','')
        #                 business.review_count = row[7].replace('"','')
        #                 business.average_rating = row[8].replace('"','')
        #                 business.review_url = row[9].replace('"','')
        #                 business.google_maps_url = row[10].replace('"','')
        #                 business.latitude = row[11].replace('"','')
        #                 business.longitude = row[12].replace('"','')
        #                 business.website = row[13].replace('"','')
        #                 business.domain = row[14].replace('"','')
        #                 business.opening_hours = row[15].replace('"','')
        #                 business.featured_image = row[16].replace('"','')
        #                 # save object
        #                 business.save()
                
        #         except Exception as e:
        #                 print("Error ", e)
        #                 # pass to the next row
        #                 pass


        success='File uploaded successfully'
        context = {'title': 'Add Business | Success','success':success}
        return render(request, 'upload_csv.html', context)
    except Exception as e:
        error='Unable to upload file. '+repr(e)
        context = {'title': 'Add Business | Error','error':error}
        return render(request, 'upload_csv.html', context)
    
# status function
def status(request, id):
    # if session is not created
    if not request.session.has_key('USER'):
        # redirect to login page
        return redirect('login')
    # if get method
    if request.method == 'GET':
        # redirect to detail page by id
        return redirect('detail', id=id)
    # if post method
    if request.method == 'POST':
        # get the status from the form
        status = request.POST.get('status')
        # get the business by id
        business = Busines.objects.get(id=id)
        # update the status
        business.status = status
        # save the business
        business.save()
        # redirect to detail page by id
        return redirect('detail', id=id)


# # function fill Busines class from csv file
# def fill_business(csv_file):
#     print("fill_business")
#     with open(csv_file, 'r') as f:
#         reader = csv.reader(f)
#         # skip header
#         next(reader)
#         for row in reader:
#             try:
#                 print(row)
#                 # create object
#                 business = Busines()
#                 # fill object
#                 business.name = row[0]
#                 business.fulladdress = row[1]
#                 business.street = row[2]
#                 business.municipality = row[3]
#                 business.categories = row[4]
#                 business.phone = row[5]
#                 business.phones = row[6]
#                 business.review_count = row[7]
#                 business.average_rating = row[8]
#                 business.review_url = row[9]
#                 business.google_maps_url = row[10]
#                 business.latitude = row[11]
#                 business.longitude = row[12]
#                 business.website = row[13]
#                 business.domain = row[14]
#                 business.opening_hours = row[15]
#                 business.featured_image = row[16]
#                 # save object
#                 business.save()
            
#             except Exception as e:
#                 print("Error ", e)
#                 # pass to the next row
#                 pass

