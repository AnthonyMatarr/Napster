from django.shortcuts import render
import googlemaps
from django.conf import settings
from .forms import *
from datetime import datetime
from .models import *
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.shortcuts import get_object_or_404
from django.contrib import messages

from django.contrib.auth import logout
from .forms import ProfileForm

#/***************************************************************************************
#*  REFERENCES
#*
#*  Title: Django-Google-Maps-API-Tutorial
#*  URL:https://github.com/NickMol/Django-Google-Maps-API-Tutorial
#*
#*  Title:Working with AJAX in Django
#*  URL:https://testdriven.io/blog/django-ajax-xhr/
#***************************************************************************************/

def home(request):
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    return render(request, "home.html")

def logout_view(request):
    logout(request)
    return redirect("/")

def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('home')
    
    return render(request, "admin_dashboard.html")

class MapView(View): #class inspired by GitHub: https://github.com/NickMol/Django-Google-Maps-API-Tutorial.git
    template_name = "map.html"

    def get(self,request): 
        key = settings.API_KEY
        eligable_locations = Locations.objects.filter(approved=True)
        locations = []
        for a in eligable_locations: 
            data = {
                'lat': float(a.lat), 
                'lng': float(a.lng), 
                'name': a.name,
                'rating_average': a.rating_average,
                'id':a.id
            }
            locations.append(data)
        context = {
            "key": key, 
            "locations": locations,
            "form": DistanceForm
        }

        return render(request, self.template_name, context)

class DistanceView(View): ##class inspired by GitHub: https://github.com/NickMol/Django-Google-Maps-API-Tutorial.git
    template_name = "distance.html"

    def get(self, request): 
        form = DistanceForm
        distances = Distances.objects.all()
        context = {
            'form':form,
            'distances':distances
        }

        return render(request, self.template_name, context)

    def post(self, request): 
        form = DistanceForm(request.POST)
        if form.is_valid(): 
            from_location = form.cleaned_data['from_location']
            from_location_info = Locations.objects.get(name=from_location)
            from_address_string = str(from_location_info.address)+", "+str(from_location_info.zipcode)+", "+str(from_location_info.city)+", "+str(from_location_info.country)

            to_location = form.cleaned_data['to_location']
            to_location_info = Locations.objects.get(name=to_location)
            to_address_string = str(to_location_info.address)+", "+str(to_location_info.zipcode)+", "+str(to_location_info.city)+", "+str(to_location_info.country)

            mode = form.cleaned_data['mode']
            now = datetime.now()

            gmaps = googlemaps.Client(key= settings.API_KEY)
            calculate = gmaps.distance_matrix(
                    from_address_string,
                    to_address_string,
                    mode = mode,
                    departure_time = now
            )


            duration_seconds = calculate['rows'][0]['elements'][0]['duration']['value']
            duration_minutes = duration_seconds/60

            distance_meters = calculate['rows'][0]['elements'][0]['distance']['value']
            distance_kilometers = distance_meters/1000

            
            obj = Distances(
                from_location = Locations.objects.get(name=from_location),
                to_location = Locations.objects.get(name=to_location),
                mode = mode,
                distance_km = distance_kilometers,
                duration_mins = duration_minutes,
            )

            obj.save()

        else: 
            print(form.errors)
        
        return redirect('my_distance_view')


def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect("home")

    if request.method == "POST":
        action = request.POST.get('action')

        if action in ['approve', 'delete']:
            location_id = request.POST.get('location_id')
            try:
                location = Locations.objects.get(id=location_id)
                if action == "approve":
                    location.approved = True
                    location.save()
                elif action == "delete":
                    location.delete()
            except Locations.DoesNotExist:
                messages.error(request, "Location not found.")

        elif action == "delete_review":
            rating_id = request.POST.get('rating_id')
            try:
                rating = Rating.objects.get(id=rating_id)
                rating.delete()
            except Rating.DoesNotExist:
                messages.error(request, "Review not found.")

        return redirect("admin_dashboard")

    all_locations = Locations.objects.all()
    ratings = Rating.objects.all()
    return render(request, "admin_dashboard.html", {'locations': all_locations, 'ratings': ratings})


# https://testdriven.io/blog/django-ajax-xhr/ used this to help me write this function
def add_location(request):
    try:
        if request.method == 'POST':
            name = request.POST.get('name')
            rating = request.POST.get('rating')
            description = request.POST.get('description')
            lat = request.POST.get('lat')
            lng = request.POST.get('lng')

            cur_user, created = User.objects.get_or_create(username=request.user.username)

            new_location = Locations(name=name, lat=lat, lng=lng, approved=False, user=cur_user)
            new_location.save()

            new_rating = Rating(location=new_location, rating=rating, description=description)
            new_rating.save()

            UserRating.objects.create(user=cur_user, rating=new_rating)
            new_location.update_rating_fields()

            return JsonResponse({"success": True, "message": "Location sent to admin."})
    except Exception as e:
        return JsonResponse({"success": False, "message": "Please enter field correctly"})

@login_required
def add_rating(request):
    try:
        if request.method == 'POST':
            ID = request.POST.get('ID')
            rating_value = request.POST.get('rating')
            description = request.POST.get('description')

            location = Locations.objects.get(pk=ID)
            user = request.user

            if UserRating.objects.filter(user=user, rating__location=location).exists():
                return JsonResponse({"success": False, "message": "You have already rated this location."})

            new_rating = Rating(location=location, rating=rating_value, description=description)
            new_rating.save()

            UserRating.objects.create(user=user, rating=new_rating)

            location.update_rating_fields()

            return JsonResponse({"success": True, "message": "Rating added successfully."})
    except Exception as e:
        print(f"Exception in add_rating: {e}")
        return JsonResponse({"success": False, "message": "Please enter valid review."})

def detail(request, spot_id):
    spot = get_object_or_404(Locations, pk=spot_id)
    if request.method == 'POST':
        form = LocationImageForm(request.POST, request.FILES)
        if form.is_valid():
            new_image = form.save(commit=False)
            new_image.location = spot
            new_image.save()
            return redirect('detail', spot_id=spot_id)
    else:
        form = LocationImageForm()
    images = spot.images.all()
    return render(request, "detail.html", {"spot": spot, "form": form, "images": images})

def feedback(request, location_id):
    cur_location = Locations.objects.get(pk=location_id)

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback_instance = form.save(commit=False)
            feedback_instance.user = cur_location.user  # Associate the feedback with the user associated with the location
            feedback_instance.location = cur_location
            feedback_instance.save()
            print(feedback_instance.pk)
            return redirect('admin_dashboard')  
    else:
        form = FeedbackForm()

    return render(request, 'feedback.html', {'form': form, 'location': cur_location})

def user_feedback(request):
    user_feedback_list = Feedback.objects.filter(user=request.user)

    return render(request, 'user_feedback.html', {'user_feedback_list': user_feedback_list})