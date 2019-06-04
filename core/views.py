from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.permissions.mixins import AdminPermissionRequiredMixin, PharmacistPermissionRequiredMixin, admin_required_permission, pharmacist_required_permission

from core import forms
from core.models import User, Pharmacy, PharmacyUser


class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = "core/index.html"


class UserProfile(LoginRequiredMixin, generic.TemplateView):
    template_name = 'core/profile.html'
    model = User
    queryset = User.objects.all()

    # def get_context_data(self, **kwargs):
    #     context = super(UserProfile, self).get_context_data(**kwargs)
    #     context['name'] = self.request.user.first_name
    #     return context


# editing user profile
@login_required()
def profile(request):
    if request.method == 'POST':
        u_form = forms.UserProfile(request.POST, instance=request.user)
        p_form = forms.ProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profile was successfully updated')
            return redirect('core:profile', name=request.user.first_name)

    else:
        u_form = forms.UserProfile(instance=request.user)
        p_form = forms.ProfileForm(instance=request.user.profile)

    context = {
        'form1': u_form,
        'form2': p_form
    }

    return render(request, 'core/profile_update.html', context)


class PharmacyRegister(LoginRequiredMixin, AdminPermissionRequiredMixin, generic.CreateView):
    template_name = 'core/pharmacy_create.html'
    model = Pharmacy
    form_class = forms.PharmacyCreateForm

    def form_valid(self, form):
        request = self.request
        form.save(commit=True)
        name = form.cleaned_data['name']
        messages.success(request, f'{name} Pharmacy was successfully created!!!')
        return super(PharmacyRegister, self).form_valid(form)


class PharmacistList(LoginRequiredMixin, AdminPermissionRequiredMixin, generic.ListView):
    template_name = 'core/pharmacist_list.html'
    model = PharmacyUser
    paginate_by = 6
    context_object_name = 'pharmacy_users'

    def get_queryset(self):
        pharmacy = Pharmacy.objects.get(name=self.request.user.pharmacyuser.works_at)
        users = PharmacyUser.objects.filter(works_at=pharmacy)
        return users

    # def get_context_data(self, **kwargs):
    #     context = super(PharmacistList, self).get_context_data(**kwargs)
    #     pharmacy = Pharmacy.objects.get(name=self.request.user.pharmacyuser.works_at)
    #     users = PharmacyUser.objects.filter(works_at=pharmacy)
    #     context['user_email'] = users
    #     new = context.get('pharmacy_users')
    #     print(new)
    #     return context


@login_required(login_url=reversed('account_login'))
@admin_required_permission
def pharmacist_add(request):
    if request.method == 'POST':
        print(request.POST)
        user_id = request.POST.get('pharmacist_id')
        user = get_object_or_404(User, id=user_id)
        pharmacy = Pharmacy.objects.get(name=request.user.pharmacyuser.works_at)
        if user.is_pharmacist:
            user.is_pharmacist = False
            messages.success(request, f'{user.email} was successfully removed as a pharmacist to "{pharmacy}" pharmacy')
        else:
            user.is_pharmacist = True
            messages.success(request, f'{user.email} was successfully added as a pharmacist to "{pharmacy}" pharmacy')
        user.save()
        return redirect('core:pharmacist_list', pharmacy=pharmacy)
    else:
        return Http404("Forbidden request type")

    # try:
    #     product_id = request.POST.get('product_id')
    # except Products.DoesNotExist:
    #     print('product does not exist')
    #     return redirect('cart:home')
    # product_obj = Products.objects.get(id=product_id)
    # cart_obj, new_obj = Cart.objects.new_or_get(request)
    #
    # if product_obj in cart_obj.products.all():
    #     cart_obj.products.remove(product_obj)
    # else:
    #     cart_obj.products.add(product_obj)
    #
    # return redirect('cart:home')
