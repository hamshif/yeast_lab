from django.shortcuts import render

# Create your views here.
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from mediums.models import Compound_Model
from mediums.forms import MediumCreatorForm 

def medium_creator(request):
    print('hello')
    print(request)
    print('')
    print('')
    print('')
    
    if request.method == 'POST':
        print('yeepee')
        
        form = MediumCreatorForm(request.POST, request.FILES)
        
        
        if form == None:
            print('form is none')
        else:
            print('form object exists')
        
        if form.is_valid():
            print('form is valid')
            
            return HttpResponseRedirect(reverse('mediums.views.medium_creator'))
            
        else:
            print('form is not valid')
        
        
        
    
    return render_to_response(
        'mediums/medium_creator.html',
        {},
        context_instance=RequestContext(request)
    )

    

