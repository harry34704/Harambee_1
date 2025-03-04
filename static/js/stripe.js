
// Initialize Stripe
document.addEventListener('DOMContentLoaded', function() {
  // Check if Stripe is loaded
  if (typeof Stripe !== 'undefined') {
    // Initialize Stripe with the public key from the server
    // This assumes your server provides STRIPE_PUBLIC_KEY in a meta tag or as a global variable
    try {
      const stripePublicKey = document.querySelector('meta[name="stripe-public-key"]').getAttribute('content');
      if (stripePublicKey) {
        window.stripeInstance = Stripe(stripePublicKey);
      }
    } catch (e) {
      console.error('Error initializing Stripe:', e);
    }
  }
});
