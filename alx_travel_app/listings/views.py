from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
import requests
from django.conf import settings
from .tasks import send_booking_confirmation_email


from .models import Listing, Booking, Payment
from .serializers import ListingSerializer, BookingSerializer, PaymentSerializer

class ListingViewSet(viewsets.ViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    

class BookingViewSet(viewsets.ViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    
    def perform_create(self, serializer):
        booking = serializer.save()
        send_booking_confirmation_email.delay(
            booking.user.email,
            f"Booking ID: {booking.id}, Destination: {booking.destination}"
        )



















class PaymentViewSet(viewsets.ViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    @action(detail=False, methods=['post'])
    def initiate_payment(self, request):
        """
        Initiate payment for a booking using Chapa API
        """
        try:
            booking_id = request.data.get('booking_id')
            customer_email = request.data.get('customer_email')
            customer_phone = request.data.get('customer_phone', '')
            description = request.data.get('description', '')

            if not booking_id or not customer_email:
                return Response(
                    {'error': 'booking_id and customer_email are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                booking = Booking.objects.get(id=booking_id)
            except Booking.DoesNotExist:
                return Response(
                    {'error': 'Booking not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Calculate total amount (listing price for now)
            amount = float(booking.listing.price)

            # Prepare Chapa payment data
            chapa_data = {
                "amount": amount,
                "currency": "ETB",
                "email": customer_email,
                "first_name": booking.guest_name.split()[0] if booking.guest_name else "Customer",
                "last_name": " ".join(booking.guest_name.split()[1:]) if len(booking.guest_name.split()) > 1 else "",
                "phone_number": customer_phone,
                "tx_ref": f"booking_{booking.id}_{booking.guest_name.replace(' ', '_')}",
                "callback_url": request.build_absolute_uri('/api/payments/verify/'),
                "return_url": request.build_absolute_uri('/api/payments/success/'),
                "customization": {
                    "title": "Travel Booking Payment",
                    "description": description or f"Payment for booking: {booking.listing.title}"
                }
            }

            # Make request to Chapa API
            headers = {
                'Authorization': f'Bearer {settings.CHAPA_SECRET_KEY}',
                'Content-Type': 'application/json'
            }

            response = requests.post(
                f"{settings.CHAPA_API_URL}/transaction/initialize",
                json=chapa_data,
                headers=headers
            )

            if response.status_code == 200:
                chapa_response = response.json()

                # Create payment record
                payment = Payment.objects.create(
                    booking=booking,
                    amount=amount,
                    customer_email=customer_email,
                    customer_phone=customer_phone,
                    description=description,
                    transaction_id=chapa_response.get('data', {}).get('tx_ref'),
                    chapa_checkout_url=chapa_response.get('data', {}).get('checkout_url'),
                    status='pending'
                )

                return Response({
                    'message': 'Payment initiated successfully',
                    'payment': PaymentSerializer(payment).data,
                    'checkout_url': chapa_response.get('data', {}).get('checkout_url')
                }, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {'error': 'Failed to initiate payment with Chapa'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    def verify_payment(self, request):
        """
        Verify payment status with Chapa
        """
        try:
            transaction_id = request.data.get('transaction_id')

            if not transaction_id:
                return Response(
                    {'error': 'transaction_id is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Find payment by transaction_id
            try:
                payment = Payment.objects.get(transaction_id=transaction_id)
            except Payment.DoesNotExist:
                return Response(
                    {'error': 'Payment not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Verify with Chapa API
            headers = {
                'Authorization': f'Bearer {settings.CHAPA_SECRET_KEY}',
            }

            response = requests.get(
                f"{settings.CHAPA_API_URL}/transaction/verify/{transaction_id}",
                headers=headers
            )

            if response.status_code == 200:
                chapa_response = response.json()

                # Update payment status based on Chapa response
                status_map = {
                    'success': 'completed',
                    'pending': 'pending',
                    'failed': 'failed'
                }

                chapa_status = chapa_response.get('status', '').lower()
                payment.status = status_map.get(chapa_status, 'failed')
                payment.save()

                return Response({
                    'message': 'Payment verified successfully',
                    'payment': PaymentSerializer(payment).data,
                    'chapa_status': chapa_status
                })
            else:
                return Response(
                    {'error': 'Failed to verify payment with Chapa'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

















@api_view(['GET'])
def payment_success(request):
    """
    Handle successful payment callback
    """
    return Response({'message': 'Payment completed successfully'})


@api_view(['GET'])
def payment_cancel(request):
    """
    Handle cancelled payment callback
    """
    return Response({'message': 'Payment was cancelled'})
