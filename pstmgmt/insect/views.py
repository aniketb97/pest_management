from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import get_list_or_404, get_object_or_404
from .models import InsectInformation, Insect
from django.contrib.auth.models import User
from api.models import Transactions, TransactionMedia
from django.contrib import messages


# Create your views here.
def dashboard(request):
    data = Insect.objects.all()
    total_insect = len(data)
    insect_info = Insect.objects.all()
    total_insect_info = len(insect_info)
    total_trans = Transactions.objects.all()
    total_trans = len(total_trans)
    trans_data = TransactionMedia.objects.all().order_by('-id')
    if request.session.has_key('is_logged'):
        return render(request, 'index.html', {"information": data, "total_insect": total_insect, "total_insect_info": total_insect_info, "data": trans_data, "total_trans": total_trans})
    else:
        return render(request, 'login.html')


def transaction_report(request):
    if request.method == "GET":
        total_trans = Transactions.objects.all()
        results = Insect.objects.all()
        total_trans = len(total_trans)
        data = TransactionMedia.objects.all().order_by('-id')

        if request.session.has_key('is_logged'):
            return render(request, 'report.html', {"data": data, "total_trans": total_trans,"label": results,})
        else:
            return render(request,'login.html')


# Create your views here.
@login_required
def add(request):
    data = Insect.objects.all
    return render(request, 'add_insect_info.html', {"insect": data})


def insert(request):
    return render(request, 'insert.html')


@login_required
def insert(request):
    return render(request, 'insert.html')

@login_required
def viewDetails(request):
    return render(request, 'allProducts.html')

@login_required
def insert_insect(request):
    data = Insect.objects.all()
    userdata = User.objects.filter(username=request.user.username)
    if request.method == 'POST':
        insect_name = request.POST["insect_name"]
        status = request.POST["status"]

        if Insect.objects.filter(insect_name=insect_name).exists():
            messages.info(request, 'Insect name already inserted.')
            return render(request, 'insert.html')

        else:

            insects = Insect(insect_name=insect_name, status=status, created_by=userdata[0])
            insects.save()
            messages.info(request, 'Data saved successfully')
            return render(request, 'insert.html')
            return render(request, 'show.html', {"insect": data})


@login_required
def view_insect(request):
    data = InsectInformation.objects.all()
    return render(request, 'views.html', {'information': data})

@login_required
def view_info(request, id):
    data = InsectInformation.objects.get(id=id)
    #data = InsectInformation.objects.all()

    #return redirect('insect:view_info' , {"information": data})
    return render(request, 'view_info.html', {"information": data})

@login_required
def edit_insect(request, id):
    data = Insect.objects.get(id=id)
    if request.method == 'POST':
        #userdata = User.objects.filter(username='PestManagement')
        insect_name = request.POST["insect_name"]
        status = request.POST["status"]

    #     if Insect.objects.filter(insect_name=insect_name).exists():
    #         messages.info(request, 'Insect name already taken')
    #         return render(request,'edit.html',{"information": data})
    #
    #
    #     else:

        data.insect_name = insect_name
        data.status = status
        #created_by = request.POST["created_by"]
        #insects = Insect(insect_name=insect_name, status=status, created_by=userdata[0])
        data.save()
        messages.info(request, 'Data saved Successfully')
        #return reverse('insect:edit_insect', args=[insects.id])
    return render(request, 'edit.html', {"information": data})



@login_required
def delete_insect(request, id):
    data = get_object_or_404(Insect, pk=id)
    data.delete()
    return redirect('insect:show_insect')


@login_required
def show_insect(request):
    data = Insect.objects.all()
    return render(request, 'show.html', {"information": data})


@login_required
def update(request,id):
    data = InsectInformation.objects.get(id=id)
    if request.method=="POST":
        insect_name = request.POST['insect_id']
        host_plant = request.POST['host_plant']
        host_plant_type = request.POST['host_plant_type']
        lifecycle = request.POST['lifecycle']
        bionomics = request.POST['bionomics']
        shape = request.POST['shape']
        growth_rate = request.POST['growth_rate']
        damage = request.POST['damage']
        symptoms = request.POST['symptoms']
        natural_enemies = request.POST['natural_enemies']
        etl = request.POST['etl']
        size = request.POST['size']
        colour = request.POST['colour']
        species = request.POST['species']
        species_example = request.POST['species_example']
        favourable_condition = request.POST['favourable_condition']
        soil_type = request.POST['soil_type']
        peak_occurance = request.POST['peak_occurance']
        region = request.POST['region']
        reproduction = request.POST['reproduction']
        preventive_measures = request.POST['preventive_measures']
        insectiside = request.POST['insectiside']
        ipm_techniques = request.POST['ipm_techniques']
        speciality = request.POST['speciality']


        data1 = InsectInformation.objects.filter(id=id , insect_name_id = insect_name).update(host_plant=host_plant, host_plant_type=host_plant_type,
                                 lifecycle=lifecycle, bionomics=bionomics, shape=shape, growth_rate=growth_rate,
                                 damage=damage, symptoms=symptoms, natural_enemies=natural_enemies, etl=etl, size=size,
                                 colour=colour, species=species, species_example=species_example,
                                 favourable_condition=favourable_condition, soil_type=soil_type,
                                 peak_occurance=peak_occurance, region=region, reproduction=reproduction,
                                 preventive_measures=preventive_measures, insectiside=insectiside,
                                 ipm_techniques=ipm_techniques, speciality=speciality)

        return redirect(reverse('insect:update', args=(id,)))
    return render(request, 'update.html',{"information":data})


@login_required
def add_new_insect(request):
    data = Insect.objects.all
    if request.method=="POST":
        insect_name = request.POST['insect_name']
        host_plant = request.POST['host_plant']
        host_plant_type = request.POST['host_plant_type']
        lifecycle = request.POST['lifecycle']
        bionomics = request.POST['bionomics']
        shape = request.POST['shape']
        growth_rate = request.POST['growth_rate']
        damage = request.POST['damage']
        symptoms = request.POST['symptoms']
        natural_enemies = request.POST['natural_enemies']
        etl = request.POST['etl']
        size = request.POST['size']
        colour = request.POST['colour']
        species = request.POST['species']
        species_example = request.POST['species_example']
        favourable_condition = request.POST['favourable_condition']
        soil_type = request.POST['soil_type']
        peak_occurance = request.POST['peak_occurance']
        region = request.POST['region']
        reproduction = request.POST['reproduction']
        preventive_measures = request.POST['preventive_measures']
        insectiside = request.POST['insectiside']
        ipm_techniques = request.POST['ipm_techniques']
        speciality = request.POST['speciality']


        if InsectInformation.objects.filter(insect_name_id=insect_name).exists():
            messages.info(request, 'Insect already registered')
            return render(request, 'add_insect_info.html', {"insect": data})
        else:
            data1 = InsectInformation(insect_name_id=insect_name,host_plant=host_plant, host_plant_type=host_plant_type, lifecycle=lifecycle, bionomics=bionomics, shape=shape, growth_rate=growth_rate, damage=damage, symptoms=symptoms, natural_enemies=natural_enemies, etl=etl, size=size, colour=colour, species=species, species_example=species_example, favourable_condition=favourable_condition, soil_type=soil_type, peak_occurance=peak_occurance, region=region, reproduction=reproduction,  preventive_measures=preventive_measures, insectiside=insectiside, ipm_techniques=ipm_techniques, speciality=speciality  )
            data1.save()
            print("Data submitted!!")
            return render(request, 'add_insect_info.html', {"insect": data})
    return render(request, 'add_insect_info.html', {"insect": data})



@login_required
def delete(request, id):
    data = get_object_or_404(InsectInformation, pk=id)
    data.delete()
    return redirect('insect:view_insect')


@login_required
def show_info_insect(request, id):
    data = get_object_or_404(Insect, pk=id)
    return render(request, 'show_info.html', {"information": data})

