import os
import requests
from django.http import JsonResponse
from django.views import View
from .models import Payment

CHAPA_SECRET_KEY = os.getenv("CHAPA_SECRET_KEY")
CHAPA_BASE_URL = "https://api.chapa.co/v1/transaction"

class InitiatePaymentView(View):
    def post(self, request):
        booking_ref = request.POST.get("booking_reference")
        amount = request.POST.get("amount")

        headers = {"Authorization": f"Bearer {CHAPA_SECRET_KEY}"}
        data = {
            "amount": amount,
            "currency": "ETB",
            "email": "customer@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "tx_ref": booking_ref,
            "callback_url": "http://localhost:8000/api/verify-payment/"
        }

        response = requests.post(f"{CHAPA_BASE_URL}/initialize", headers=headers, data=data)
        resp_json = response.json()

        if response.status_code == 200 and resp_json.get("status") == "success":
            tx_id = resp_json["data"]["tx_ref"]
            Payment.objects.create(
                booking_reference=booking_ref,
                transaction_id=tx_id,
                amount=amount,
                status="Pending"
            )
            return JsonResponse({"checkout_url": resp_json["data"]["checkout_url"]})
        return JsonResponse({"error": "Payment initiation failed"}, status=400)


class VerifyPaymentView(View):
    def get(self, request):
        tx_ref = request.GET.get("tx_ref")
        headers = {"Authorization": f"Bearer {CHAPA_SECRET_KEY}"}
        response = requests.get(f"{CHAPA_BASE_URL}/verify/{tx_ref}", headers=headers)
        resp_json = response.json()

        try:
            payment = Payment.objects.get(transaction_id=tx_ref)
        except Payment.DoesNotExist:
            return JsonResponse({"error": "Transaction not found"}, status=404)

        if response.status_code == 200 and resp_json.get("status") == "success":
            payment.status = "Completed"
            payment.save()
            return JsonResponse({"status": "Completed"})
        else:
            payment.status = "Failed"
            payment.save()
            return JsonResponse({"status": "Failed"}, status=400)



from .tasks import send_booking_confirmation_email

def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    booking = self.get_object()
    send_booking_confirmation_email.delay(booking.user.email, booking.id)
    return response
