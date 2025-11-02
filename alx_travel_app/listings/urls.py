from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r"listings", views.ListingViewSet, basename="listing")
router.register(r"bookings", views.BookingViewSet, basename="booking")
router.register(r"payments", views.PaymentViewSet, basename="payment")

urlpatterns = [
    path("", include(router.urls)),
    path("payments/initiate/", views.PaymentViewSet.as_view({'post': 'initiate_payment'}), name="initiate-payment"),
    path("payments/verify/", views.PaymentViewSet.as_view({'post': 'verify_payment'}), name="verify-payment"),
    path("payments/success/", views.payment_success, name="payment-success"),
    path("payments/cancel/", views.payment_cancel, name="payment-cancel"),
]
