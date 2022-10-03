from telnetlib import STATUS
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import Company
from .models import Employee
from .models import Enrollment
from .models import Mark

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
            datos = {'message': "Companies not found."}
        return JsonResponse(datos, status=404)
    ##ADITIONAL ENDPOINT TO ADD A COMPANY
    def post(self, request):
        try:
            jd = json.loads(request.body)
            Company.objects.create(
            name=jd['name'], website=jd['website'], foundation=int(jd['foundation']))
            datos = {'message': "Success"}
            return JsonResponse(datos)
        except:
            return JsonResponse({'message': "Ah ocurrido un error ingresando la compania."}, status=400)

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
            company_fk_id = self.request.GET.get("company_fk_id")
            id_employee = self.request.GET.get("id_employee")
            employees = list(Employee.objects.values())
            try:
                if company_fk_id is not None:
                    filter_employee = list(Employee.objects.filter(company = int(company_fk_id) ).values())
                    datos = {'message': "Success", 'employees': filter_employee}
                    return JsonResponse(datos)
                else:
                    pass
            except:
                pass
            
            try:
                if id_employee is not None:
                    filter_employee = list(Employee.objects.filter(id = int(id_employee)).values())
                    
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
                data = {'message': "employees not found."}
            return JsonResponse(data, status = 404)



    def post(self, request):
        try:
            jd = json.loads(request.body)
            company = Company.objects.get(id=jd['company_fk_id'])
            Employee.objects.create(name=jd['name'], company=company)
            datos = {'message': "Success"}
            return JsonResponse(datos)
        except:
            return JsonResponse({'message': 'Ha ocurrido un error ingresando al empleado.'}, status= 400)



class EnrollmentView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def post(self, request): 
        try:
            jd = request.POST
            company = Company.objects.get(id= int(jd['compania']))
            employee = Employee.objects.get(name = jd['nombreEmpleado'], company = company)
            Enrollment.objects.create(photo= request.FILES.get('image_upload'), employee = employee).save()
            return JsonResponse({'message': "Success"} )
        except:
            return JsonResponse({'message': 'Ha ocurrido un error, la compania o empleado no existen.'},status= 404)
    def put(self, request):
        pass

    def delete(self, request):
        pass


class MarkView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        mark = list(Mark.objects.values())
        employee = self.request.GET.get("employee")
        company = self.request.GET.get("company")
        initialDate = self.request.GET.get("initialDate")
        lastDate = self.request.GET.get("lastDate")
        try:
            if employee is not None and company is not None and initialDate is not None and  lastDate is not None:
                filter_mark = list(Mark.objects.filter(
                    employee=int(employee), 
                    company = int(company), 
                    mark_date__gte=initialDate, mark_date__lte=lastDate).values())
                    
                
                if len(filter_mark) > 0:
                    data = {'message': "Success", 'Marks': filter_mark}
                    return JsonResponse(data)
                else:
                    data = {'message': "Marks not found."}
                    return JsonResponse(data, status= 404)
                return JsonResponse(data)
            else:
                pass
        except:
            data = {'message': "marks not found."}
            return JsonResponse(data,status= 404)
            


    def post(self, request):
        try:
            jd = json.loads(request.body)
            employee = Employee.objects.get(name = jd['nombreEmpleado'])
            company = Company.objects.get(name = jd['nombreCompania'])
            Mark.objects.create(employee = employee, company = company)
            
            datos = {'message': "Success"}
            return JsonResponse(datos)
        except:
            return JsonResponse({'message': "No se ha podido ingresar la marca"}, status = 400)

    def put(self, request):
        pass

    def delete(self, request):
        pass
