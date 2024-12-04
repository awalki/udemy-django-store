import json
from http import HTTPStatus

import stripe
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from django.views.generic.edit import CreateView

from orders.forms import OrderForm
from django.urls import reverse_lazy, reverse
from django.conf import settings
from common.views import TitleMixin

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Store - Спасибо за заказ!'

class CanceledTemplateView(TemplateView):
    template_name = 'orders/canceled.html'

class OrderCreateView(TitleMixin, CreateView):
    title = 'Store - Оформление заказа'

    template_name = 'orders/order-create.html'
    form_class = OrderForm

    success_url = reverse_lazy('orders:order_create')

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1QRx2XGLIg3yUIZ0BnBB6AgG',
                    'quantity': 1,
                },
            ],
            metadata={'order_id': self.object.id},
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_canceled')),
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)

@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object  # contains a stripe.PaymentIntent

        fulfill_order(payment_intent)

    elif event.type == 'payment_method.attached':
        payment_method = event.data.object  # contains a stripe.PaymentMethod
        # Then define and call a method to handle the successful attachment of a PaymentMethod.
        # handle_payment_method_attached(payment_method)
    # ... handle other event types
    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)

def fulfill_order(session):
    order_id = session.metadata.order_id
    print('fulfilin')
