# Harambee Student Accommodation System

A Flask-based student accommodation management system with document verification and payment processing.

## Features

- Student registration and authentication
- Document upload and verification
- Room booking and management
- Payment processing
- Admin dashboard for application approval
- Maintenance request system

## Prerequisites

- Python 3.11
- PostgreSQL database
- Stripe account for payments
- Twilio account for SMS notifications

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/harambee
SESSION_SECRET=your_secret_key
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_PUBLIC_KEY=your_stripe_public_key
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE_NUMBER=your_twilio_phone
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/harambee-accommodation.git
cd harambee-accommodation
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize the database:
```bash
flask db upgrade
```

4. Run the application:
```bash
python main.py
```

The application will be available at `http://localhost:5000`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
