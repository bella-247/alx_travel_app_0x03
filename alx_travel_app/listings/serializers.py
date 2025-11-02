from rest_framework import serializers
from .models import Listing, Booking, Review, Payment

class ListingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Listing
		fields = ['id', 'title', 'description', 'price', 'location']

class BookingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Booking
		fields = ['id', 'listing', 'guest_name', 'start_date', 'end_date']

class ReviewSerializer(serializers.ModelSerializer):
	class Meta:
		model = Review
		fields = ['id', 'listing', 'reviewer_name', 'rating', 'comment']

class PaymentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Payment
		fields = ['id', 'booking', 'amount', 'currency', 'status', 'transaction_id',
		         'chapa_checkout_url', 'customer_email', 'customer_phone', 'description',
		         'created_at', 'updated_at']
		read_only_fields = ['transaction_id', 'chapa_checkout_url', 'created_at', 'updated_at']
