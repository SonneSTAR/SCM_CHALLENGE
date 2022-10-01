from telnetlib import STATUS
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import Company
from .models import Employee
from .models import Enrollment
from django.core.files import File
import urllib
import os
#from .models import Upload

import json
# Create your views here.


class CompanyView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        companies = list(Company.objects.values())
        if len(companies) > 0:
            datos = {'message': "Success", 'companies': companies}
        else:
            datos = {'message': "Companies not found.."}
        return JsonResponse(datos)

    def post(self, request):
        # print(request.body)
        jd = json.loads(request.body)
        # print(jd)
        Company.objects.create(
            name=jd['name'], website=jd['website'], foundation=int(jd['foundation']))
        datos = {'message': "Success"}
        return JsonResponse(datos)

    def put(self, request):
        pass

    def delete(self, request):
        pass


class EmployeeView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def get(self, request):
        try:
            employees = list(Employee.objects.values())
            jd = json.loads(request.body)
            try:
                if jd['company_fk_id'] is not None:
                    filter_employee = list(Employee.objects.filter(company_fk = int(jd['company_fk_id']) ).values())
                    datos = {'message': "Success", 'employees': filter_employee}
                    return JsonResponse(datos)
                else:
                    pass
            except:
                pass
            
            try:
                if jd['id'] is not None:
                    print("PASO employee_id")
                    filter_employee = list(Employee.objects.filter(id = int(jd['id']) ).values())
                    
                    datos = {'message': "Success", 'employees': filter_employee}
                    
                    return JsonResponse(datos)
                else: 
                    pass

            except:
                pass
        except:
            if len(employees) > 0:
                data = {'message': "Success", 'employees': employees}
            else:
                data = {'message': "employees not found.."}
            return JsonResponse(data)



    def post(self, request):
        try:
            # print(request.body)
            jd = json.loads(request.body)
            # print(jd)
            company = Company.objects.get(id=jd['company_fk_id'])
            Employee.objects.create(name=jd['name'], company=company)
            datos = {'message': "Success"}
            return JsonResponse(datos)
        except:
            return JsonResponse({'message': 'Ha ocurrido un error'}, status= 404)



class EnrollmentView(View):
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    #Enrollamiento
    def post(self, request): 
        
        print(request.FILES.get('image_upload'))
        jd = request.POST
        print(request.POST)
        datos = {'message': "Success"} 
        #la clave foranea que se esta instanciando, el registro tiene que existir en la otra tabla 
        #para vincularse.
        #si esta este registro, se le pasa eta instancia como parametro al get en la posicion
        #donde iria la fk
        company = Company.objects.get(name= jd['compania'])
        employee = Employee.objects.get(name = jd['nombreEmpleado'], company = company)
        Enrollment.objects.create(photo= request.FILES.get('image_upload'), employee = employee).save()
        return JsonResponse(datos)

    def put(self, request):
        pass

    def delete(self, request):
        pass