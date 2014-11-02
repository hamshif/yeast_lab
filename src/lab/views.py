from django.shortcuts import render

# Create your views here.
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from mediums.models import Compound_Model
from mediums.forms import MediumCreatorForm 

def home(request):
    
    print(request)
    
    for variable in request.GET:
        print(variable + ' = ' +request.GET.get(variable))
    
    return render_to_response(
            'lab/home.html',
            {},
            context_instance=RequestContext(request)
        )
    
