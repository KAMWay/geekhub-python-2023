from django.shortcuts import render
from django.utils import timezone
from django.views import generic

from product.models import Product
from .forms import OrderForm
from .models import Order, Item


class IndexView(generic.ListView):
    template_name = "order/index.html"
    context_object_name = "order_list"

    def get_queryset(self):
        return Order.objects.all()


class DetailView(generic.ListView):
    template_name = "order/detail.html"
    context_object_name = "detail_list"

    def get_queryset(self):
        return Item.objects.filter(order_id=self.kwargs['order_id'])


class SaveView(generic.FormView):
    template_name = "order/save.html"
    form_class = OrderForm

    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST)
        context = {'form': OrderForm()}

        if form.is_valid():
            try:
                self.__save(form)
                context.update({"message": "Order was successfully"})
            except Exception:
                context.update({"message": "Order was unsuccessfully"})
        else:
            context.update({"message": "Form data unsuccessfully"})

        return render(request, 'order/save.html', context=context)

    def get(self, request, *args, **kwargs):
        form = OrderForm()
        return render(request, 'order/save.html', context={'form': form})

    def __save(self, form: OrderForm):
        product = Product.objects.get(id=form.cleaned_data['product_id'])
        product_quantity = form.cleaned_data['product_quantity']
        time = timezone.now()
        order = Order(order_date=time, order_amount=product_quantity * product.price)
        order.save()
        order_item = Item(order=order, product=product, product_quantity=product_quantity)
        order_item.save()
