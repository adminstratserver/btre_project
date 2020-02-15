from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from listings.choices import price_choices, mktbias_choices
from django.contrib.auth.decorators import login_required
from listings.models import Listing
from members.models import MemberProfile
from demoapp.tasks import addtwonumbers

#from partners.models import Partner
from developers.models import Developer

def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)[:3]
    alldevelopers = Developer.objects.order_by('published_date')

    context = {
        'listings': listings,
        'mktbias_choices': mktbias_choices,
        'alldevelopers': alldevelopers,
        'price_choices': price_choices
    }
    return render(request, 'pages/index.html', context)


def about(request):

    alldevelopers = Developer.objects.order_by('published_date')
    mvd_developers = Developer.objects.all().filter(is_mvd=True)

    context = {
        'alldevelopers': alldevelopers,
        'mvd_developers': mvd_developers,
    }
    return render(request, 'pages/about.html', context)

def memberProfile(request):

    if request.method == 'POST':

        b4 = MemberProfile.objects.get(id=request.user.id)
        if request.POST['first_name']: b4.first_name = request.POST['first_name']
        if request.POST['last_name']: b4.last_name = request.POST['last_name']
        if request.POST['email']: b4.email = request.POST['email']
        if request.POST['ibHostname']: b4.ibHostname = request.POST['ibHostname']
        #b4.photo = request.POST['inputGroupFile01']
        b4.save()
        messages.success(request, 'Changes are completed!')
        return redirect('dashboard')

    else:
        ##user_contacts = User.objects.filter(id=request.user.id)
        profile1 = MemberProfile.objects.filter(id=request.user.id)
        print('1. profile1 = ', profile1)
        context = {'profile1': profile1}
        return render(request, 'pages/profile.html', context)


@login_required(redirect_field_name='login')
def ibgatewayconfig(request):
    return render(request, 'pages/ibgatewayconfig.html')

@login_required(redirect_field_name='login')
def hostnameconfig(request):
    return render(request, 'pages/hostnameconfig.html')


@login_required(redirect_field_name='login')
def testIBconnect(request):

    profile1 = MemberProfile.objects.filter(id=request.user.id)
    context = {
        'profile1': profile1
    }

    if request.method == 'POST':
        b5 = MemberProfile.objects.get(id=request.user.id)
        print ("123. Hostname=",b5.ibHostname)
        addtwonumbers.delay(10, 10)
        tt = Test_Stratserver()
        tt.test_Stratserver_fn(b5.ibHostname)
        return redirect('dashboard')
    #return render(request, 'stratserver/contact.html')
    return render(request, 'pages/testconnect.html', context)

def faq(request):

    return render(request, 'pages/faq.html')

def services(request):

    return render(request, 'pages/services.html')
