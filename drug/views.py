from django.http.response import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from drug.forms import DrugRegistration
from drug.models import Drugs, Category, OrderDrugs, Order, ExpiredDrugs
from core.models import Pharmacy, PharmacyUser, Profile, City
from core.permissions.mixins import AdminPermissionRequiredMixin, PharmacistPermissionRequiredMixin, admin_required_permission, pharmacist_required_permission


class DrugRegister(LoginRequiredMixin, generic.CreateView):
    template_name = 'drug/register.html'
    model = Drugs
    form_class = DrugRegistration
    # initial =

    # # overridding form field input
    # def get_initial(self):
    #     initial = super(DrugRegister, self).get_initial()
    #     print(self.initial)
    #     initial['pharmacy'] = self.kwargs.get("pk")
    #     return initial

    # def get_form_kwargs(self):
    #     kwargs = super(IdentitySocieteFormView, self).get_form_kwargs()
    #     query_Responsable = self.request.GET.get('Responsable')
    #     Responsable = Individu.objects.filter(NumeroIdentification=query_Responsable)
    #     kwargs['responsable_qs'] = Responsable
    #     u = request.user
    #     kwargs['user_initial'] = '{lname} {fname}'.format(lname=u.last_name, fname=u.first_name)
    #     return kwargs
    #
    # class SocieteFormulaire(forms.ModelForm):
    #     def __init__(self, *args, **kwargs):
    #         user_initial = kwargs.pop('user_initial', None)
    #         responsable_qs = kwargs.pop('responsable_qs', None)
    #         super(SocieteFormulaire, self).__init__(*args, **kwargs)
    #         self.fields['Responsable'].queryset = responsable_qs
    #         self.fields['InformationsInstitution'].initial = user_initial

    def form_valid(self, form):
        request = self.request
        form.instance.added_by = self.request.user
        form.instance.pharmacy = Pharmacy.objects.filter(name=request.user.pharmacyuser.works_at)[0]
        form.instance.city = City.objects.filter(name=self.request.user.pharmacyuser.city)[0]
        form.save(commit=True)
        name = form.cleaned_data['name']
        messages.success(request, f'{name} was successfully registered!!!')
        return super(DrugRegister, self).form_valid(form)


class DrugList(LoginRequiredMixin, generic.ListView):
    template_name = 'drug/list.html'
    model = Drugs
    paginate_by = 5
    context_object_name = 'drugs'
    queryset = Drugs.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pharmacy'] = Pharmacy.objects.filter(name=self.request.user.pharmacyuser.works_at)[0]
        context['pharmacy_drugs'] = Drugs.objects.filter(pharmacy=self.request.user.pharmacyuser.works_at)
        # print(context.get('pharmacy'))
        return context


class DrugDetail(LoginRequiredMixin, generic.DetailView):
    queryset = Drugs.objects.all()
    template_name = 'drug/detail.html'
    context_object_name = 'drug'

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')

        try:
            instance = Drugs.objects.get(slug=slug)
        except Drugs.DoesNotExist:
            raise Http404("Drug doesn't exist")
        except Drugs.MultipleObjectsReturned:
            qs = Drugs.objects.filter(slug=slug)
            instance = qs.first()
        except:
            raise Http404('What error is this one')
        return instance

    # def get_context_data(self, **kwargs):
    #     contex = super(DrugDetail, self).get_context_data(**kwargs)
    #     contex['pharmacy'] = Drug.objects.get(pharmacy__name__startswith='m')


class DrugEdit(LoginRequiredMixin, AdminPermissionRequiredMixin, generic.UpdateView):
    template_name = 'drug/edit.html'
    form_class = DrugRegistration
    context_object_name = 'drug'

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')

        try:
            instance = Drugs.objects.get(slug=slug)
        except Drugs.DoesNotExist:
            raise Http404("Drug doesn't exist")
        except Drugs.MultipleObjectsReturned:
            qs = Drugs.objects.filter(slug=slug)
            instance = qs.first()
        except:
            raise Http404('What error is this one')
        return instance

    # def form_valid(self):
    #     request = self.request
    #     messages.success(request, 'Drug was successfully Edited!!!')
    #     return super().form_valid(self)


class DrugDelete(LoginRequiredMixin, AdminPermissionRequiredMixin, generic.DeleteView):
    model = Drugs
    template_name = 'drug/confirm_delete.html'
    context_object_name = 'drug'
    success_url = reverse_lazy('drug:list')


# adding drug to cart
@login_required(login_url=reversed('account_login'))
@pharmacist_required_permission
def add_to_cart(request, slug):
    drug = get_object_or_404(Drugs, slug=slug)
    order_drug, created = OrderDrugs.objects.get_or_create(drug=drug, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.drugs.filter(drug__slug=drug.slug).exists():
            order_drug.quantity += 1
            order_drug.save()
            messages.info(request, f'{drug.name} quantity was updated')
        else:
            order.drugs.add(order_drug)
            messages.info(request, f'{drug.name} was added to your cart')
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.drugs.add(order_drug)
        messages.info(request, f'{drug.name} was added to your cart')

    return redirect('drug:order_summary')


# removing drug from cart
@login_required(login_url=reversed('account_login'))
@pharmacist_required_permission
def remove_from_cart(request, slug):
    drug = get_object_or_404(Drugs, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.drugs.filter(drug__slug=drug.slug).exists():
            order_drug = OrderDrugs.objects.filter(drug=drug, user=request.user, ordered=False)[0]
            order.drugs.remove(order_drug)
            messages.info(request, f'{drug.name} was removed from your cart')
            return redirect('drug:order_summary')
        else:
            messages.info(request, f'{drug.name} was not in your cart')
            return redirect('drug:order_summary')
    else:
        messages.info(request, "You don't have an active order")
        return redirect('drug:order_summary')


# removing single drug from cart
@login_required(login_url=reversed('account_login'))
@pharmacist_required_permission
def remove_single_drug_from_cart(request, slug):
    drug = get_object_or_404(Drugs, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.drugs.filter(drug__slug=drug.slug).exists():
            order_drug = OrderDrugs.objects.filter(drug=drug, user=request.user, ordered=False)[0]

            if order_drug.quantity > 1:
                order_drug.quantity -= 1
                order_drug.save()
            else:
                order.drugs.remove(order_drug)

            messages.info(request, f'{drug.name} quantity was updated')
            return redirect('drug:order_summary')
        else:
            messages.info(request, f'{drug.name} was not in your cart')
            return redirect('drug:detail', slug=slug)
    else:
        messages.info(request, "You don't have an active order")
        return redirect('drug:detail', slug=slug)


# order summary
class OrderSummary(LoginRequiredMixin, PharmacistPermissionRequiredMixin, generic.View):

    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)

            # calculating the total price of the drugs in the cart
            total = 0

            for drug in order.drugs.all():
                total += drug.get_final_price()

            context = {'drug': order, 'total': total}
            return render(self.request, 'drug/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You don not have an active order")
            return redirect('/')


# view drugs present in my pharmacy
class DrugsPharmacy(LoginRequiredMixin, AdminPermissionRequiredMixin, generic.ListView):
    template_name = 'drug/drug_pharmacy.html'
    model = Drugs
    paginate_by = 5
    context_object_name = 'drugs'

    def get_queryset(self):
        request = self.request
        pharmacy = Pharmacy.objects.get(name=self.request.user.pharmacyuser.works_at)
        drugs = Drugs.objects.filter(added_by=request.user, pharmacy=pharmacy)
        return drugs


# get the list of expired drugs for a given pharmacy
class DrugsExpired(LoginRequiredMixin, AdminPermissionRequiredMixin, generic.ListView):
    template_name = 'drug/expired_drugs.html'
    model = Drugs
    paginate_by = 5
    context_object_name = 'drugs'

    def get_queryset(self):
        request = self.request
        pharmacy = Pharmacy.objects.get(name=self.request.user.pharmacyuser.works_at)
        drugs = Drugs.objects.filter(added_by=request.user, pharmacy=pharmacy)

        present_date = timezone.now().date()

        for drug in drugs:
            expiry_date = drug.expiry_date
            difference = int(str(expiry_date - present_date).split()[0])  # gets the number of days difference

            if difference < 0:
                return Drugs.objects.filter(expiry_date=expiry_date)
