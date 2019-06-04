from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from pms_new import settings
from django.urls import reverse
from core.models import Pharmacy, City
from django.db.models.signals import pre_save, post_save

from drug.utils import unique_slug_generator

User = settings.AUTH_USER_MODEL
# Create your models here.


class Category(models.Model):
    name = models.CharField(help_text='category of drug', max_length=100)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class DrugQueryset(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def good_drugs(self):
        drugs = self.all()
        present_date = timezone.now().date()

        for drug in drugs:
            expiry_date = drug.expiry_date
            difference = int(str(expiry_date - present_date).split()[0])  # gets the number of days difference

            if difference > 0:
                return self.filter(expiry_date=expiry_date)

    def bad_drugs(self):
        drugs = self.all()
        present_date = timezone.now().date()

        for drug in drugs:
            expiry_date = drug.expiry_date
            difference = int(str(expiry_date - present_date).split()[0])  # gets the number of days difference

            if difference < 0:
                return self.filter(expiry_date=expiry_date)

    def search(self, query):
        lookups = Q(name__icontains=query) | Q(des__icontains=query) | Q(price__icontains=query)
        return self.filter(lookups).distinct()


class DrugManager(models.Manager):
    def get_queryset(self):
        return DrugQueryset(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active().good_drugs()

    def expired_drugs(self):
        return self.get_queryset().active().bad_drugs()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)


class Drugs(models.Model):
    name = models.CharField(max_length=100, help_text='name of drug')
    des = models.TextField(max_length=200, help_text='drug description', verbose_name='Description')
    slug = models.SlugField(blank=True, unique=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True, help_text='please upload drug image here')
    price = models.DecimalField(decimal_places=2, max_digits=20, default=0.00)
    discount_price = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
    batch_no = models.IntegerField(verbose_name='Batch Number')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, default=None)
    city = models.ForeignKey(City, on_delete=models.CASCADE, default=None)
    active = models.BooleanField(default=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    entry_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateField()

    created_on = models.DateTimeField(_('registration date'), auto_now_add=True)
    updated_on = models.DateTimeField(_('last updated'), auto_now=True)

    objects = DrugManager()

    def get_absolute_url(self):
        return reverse('drug:list')

    def get_add_to_cart_url(self):
        return reverse('drug:add_to_cart', kwargs={'slug': self.slug})

    def remove_from_cart_url(self):
        return reverse('drug:remove_from_cart', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['-created_on']
        verbose_name_plural = 'Drugs'

    def __str__(self):
        return self.name


class OrderDrugs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    drug = models.ForeignKey(Drugs, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.drug.name}'

    class Meta:
        verbose_name_plural = 'Ordered Drugs'

    def get_total_drug_price(self):
        return self.quantity * self.drug.price

    def get_total_discount_drug_price(self):
        return self.quantity * self.drug.discount_price

    def get_amount_saved(self):
        return self.get_total_drug_price() - self.get_total_discount_drug_price()

    def get_final_price(self):
        if self.drug.discount_price:
            return self.get_total_discount_drug_price()
        else:
            return self.get_total_drug_price()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    drugs = models.ManyToManyField(OrderDrugs)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email

    # def get_total(self):
    #     total = 0
    #
    #     for drug in self.drugs.all():
    #         total += drug.get_final_price()
    #
    #     return total


class ExpiredDrugs(models.Model):
    drugs = models.ForeignKey(Drugs, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Expired Drugs'
