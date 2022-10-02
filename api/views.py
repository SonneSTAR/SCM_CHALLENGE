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
            company_fk_id = self.request.GET.get("company_fk_id")
            id_employee = self.request.GET.get("id_employee")
            employees = list(Employee.objects.values())
            print(id_employee)
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
                    print("PASO employee_id")
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
                data = {'message': "employees not found.."}
            return JsonResponse(data)



    def post(self, request):
        try:
            jd = json.loads(request.body)
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


class MarkView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        mark = list(Mark.objects.values())
        print("ENTRO AL GET")
        employee = self.request.GET.get("employee")
        company = self.request.GET.get("company")
        initialDate = self.request.GET.get("initialDate")
        lastDate = self.request.GET.get("lastDate")
        #jd = json.loads(request.body) 
        try:
            print("entro al try")
            if employee is not None and company is not None and initialDate is not None and  lastDate is not None:
                print("PASO EL IF")
                print(initialDate)
                filter_mark = list(Mark.objects.filter(
                    employee=int(employee), 
                    company = int(company), 
                    mark_date__gte=initialDate, mark_date__lte=lastDate).values())
                    
                data = {'message': "Success", 'Marks': filter_mark}
                return JsonResponse(data)
            else:
                pass
        except:
            print("paso")
            data = {'message': "mark not found.."}
            return JsonResponse(data)
            


    def post(self, request):
        try:
            print("asd")
            jd = json.loads(request.body)
            print(jd)
            employee = Employee.objects.get(name = jd['nombreEmpleado'])
            
            company = Company.objects.get(name = jd['nombreCompania'])
            print("se cae?")
            Mark.objects.create(employee = employee, company = company)
            
            datos = {'message': "Success"}
            return JsonResponse(datos)
        except:
            return JsonResponse(f"error")

    def put(self, request):
        pass

    def delete(self, request):
        pass
