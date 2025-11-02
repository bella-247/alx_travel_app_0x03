# ALX Travel App with Chapa Payment Integration

A comprehensive Django REST API application for travel bookings with integrated Chapa payment gateway. This project demonstrates real-world payment processing implementation in a travel booking system.

## 🚀 Project Overview

This Django application provides a complete travel booking system with the following core features:

- **Property Listings**: Manage available accommodations and properties
- **Booking System**: Handle customer reservations with date management
- **Review System**: Allow customers to rate and review properties
- **Payment Processing**: Integrated Chapa payment gateway for secure transactions
- **API-First Design**: RESTful API architecture for frontend integration

## 💳 Chapa Payment Integration

The application features a complete payment processing system using **Chapa** - Ethiopia's leading payment gateway. This integration provides:

### ✅ Payment Features
- **Secure Payment Initiation**: Create payments and redirect to Chapa's secure checkout
- **Payment Verification**: Real-time payment status verification with Chapa API
- **Transaction Tracking**: Complete payment lifecycle management
- **Status Management**: Automatic status updates (pending → completed/failed)
- **Customer Management**: Store customer details and payment history

### 🔄 Payment Workflow
1. **Initiation**: Customer selects booking and initiates payment
2. **Redirection**: System redirects to Chapa's secure payment page
3. **Processing**: Chapa processes the payment securely
4. **Verification**: System verifies payment status via Chapa API
5. **Confirmation**: Payment status updated and confirmation sent

## 🛠️ Technology Stack

- **Backend**: Django 5.2.7 (Python web framework)
- **API**: Django REST Framework
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Payment Gateway**: Chapa API
- **Task Queue**: Celery with RabbitMQ
- **Environment Management**: Django-environ
- **CORS Support**: Django-cors-headers

## 📦 Installation & Setup

### Prerequisites
- Python 3.11+
- Django 5.2+
- Virtual environment (recommended)
- Chapa account and API credentials

### 1. Clone and Setup
```bash
git clone <repository-url>
cd alx_travel_app_0x02
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
cd alx_travel_app
pip install -r requirement.txt
```

### 3. Environment Configuration
Update the `.env` file with your credentials:
```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database
DATABASE_URL=sqlite:///db.sqlite3

# Celery
CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672//

# Chapa Payment Gateway (Get these from https://dashboard.chapa.co/)
CHAPA_SECRET_KEY=CHAPA_your_actual_secret_key_here
CHAPA_PUBLIC_KEY=CHAPA_your_actual_public_key_here
```

### 4. Database Setup
```bash
cd alx_travel_app
python manage.py makemigrations
python manage.py migrate
```

### 5. Run Development Server
```bash
cd alx_travel_app
python manage.py runserver
```

The API will be available at `http://localhost:8000`

## 🔑 API Endpoints

### Core Resources
- `GET /api/listings/` - List all properties
- `GET /api/bookings/` - List all bookings
- `GET /api/reviews/` - List all reviews

### Payment Endpoints
- `GET /api/payments/` - List all payments
- `POST /api/payments/initiate/` - Initiate new payment
- `POST /api/payments/verify/` - Verify payment status
- `GET /api/payments/success/` - Payment success callback
- `GET /api/payments/cancel/` - Payment cancellation callback

## 💰 Payment Integration Usage

### 1. Initiate Payment
```bash
curl -X POST http://localhost:8000/api/payments/initiate/ \
  -H "Content-Type: application/json" \
  -d '{
    "booking_id": 1,
    "customer_email": "customer@example.com",
    "customer_phone": "+251911123456",
    "description": "Payment for hotel booking"
  }'
```

**Response:**
```json
{
  "message": "Payment initiated successfully",
  "payment": {
    "id": 1,
    "booking": 1,
    "amount": "100.00",
    "currency": "ETB",
    "status": "pending",
    "transaction_id": "booking_1_customer_name",
    "chapa_checkout_url": "https://checkout.chapa.co/payment/..."
  },
  "checkout_url": "https://checkout.chapa.co/payment/..."
}
```

### 2. Verify Payment
```bash
curl -X POST http://localhost:8000/api/payments/verify/ \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "booking_1_customer_name"
  }'
```

**Response:**
```json
{
  "message": "Payment verified successfully",
  "payment": {
    "id": 1,
    "status": "completed",
    "amount": "100.00"
  },
  "chapa_status": "success"
}
```

## 🗄️ Database Models

### Payment Model
```python
class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='ETB')
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES)
    transaction_id = models.CharField(max_length=255, unique=True)
    chapa_checkout_url = models.URLField()
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Status Values
- `pending` - Payment initiated but not completed
- `processing` - Payment is being processed
- `completed` - Payment successful
- `failed` - Payment failed or was declined
- `cancelled` - Payment was cancelled by user

## 🔒 Security Features

- **Environment Variables**: Sensitive API keys stored securely
- **Input Validation**: All payment data validated before processing
- **Error Handling**: Comprehensive error handling for failed payments
- **Transaction Tracking**: Unique transaction IDs for audit trails

## 🧪 Testing

### 1. Create Test Data
```bash
cd alx_travel_app
python manage.py shell
```

```python
# Create a test listing
from listings.models import Listing, Booking

listing = Listing.objects.create(
    title="Test Hotel",
    description="A beautiful test hotel",
    price=100.00,
    location="Addis Ababa"
)

booking = Booking.objects.create(
    listing=listing,
    guest_name="Test Customer",
    start_date="2024-01-01",
    end_date="2024-01-03"
)
```

### 2. Test Payment Flow
1. Use the API endpoints above to test payment initiation
2. Use Chapa's test environment for sandbox testing
3. Verify payment status updates correctly

## 🚀 Deployment Considerations

### Production Setup
1. **Database**: Switch to PostgreSQL for production
2. **Environment Variables**: Use proper secret management
3. **HTTPS**: Ensure SSL/TLS encryption for payment security
4. **CORS**: Configure appropriate CORS policies
5. **Celery**: Set up proper message broker (RabbitMQ/Redis)

### Environment Variables for Production
```env
DEBUG=False
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://user:password@host:port/dbname
CHAPA_SECRET_KEY=your_production_chapa_secret
CHAPA_PUBLIC_KEY=your_production_chapa_public
```

## 📚 API Documentation

The application includes Swagger/OpenAPI documentation available at:
`http://localhost:8000/docs/` (when using drf-yasg)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues related to:
- **Chapa Integration**: Check Chapa documentation at https://developer.chapa.co/
- **Django Issues**: Refer to Django documentation
- **Payment Problems**: Contact Chapa support with transaction IDs

## 🎯 Key Features Summary

✅ **Complete Payment Lifecycle Management**
✅ **Secure API Integration with Chapa**
✅ **Real-time Payment Verification**
✅ **Comprehensive Error Handling**
✅ **Production-Ready Architecture**
✅ **Detailed API Documentation**
✅ **Environment-Based Configuration**

This integration provides a solid foundation for payment processing in travel booking systems and can be extended for other e-commerce applications requiring secure payment processing.
