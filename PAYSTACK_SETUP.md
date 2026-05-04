# Paystack API Setup Guide

## Step 1: Create a Paystack Account

1. Visit [https://paystack.com/signup](https://paystack.com/signup)
2. Fill in your business details:
   - Email address
   - Full name
   - Business name
   - Phone number
3. Create a strong password
4. Verify your email address

## Step 2: Complete Account Verification

1. Log in to your Paystack dashboard
2. Navigate to **Settings → General**
3. Fill in your business information:
   - Legal business name
   - Business type (e.g., "Data/Telecom Services")
   - Website URL (your Render domain, e.g., `https://kdatahub.onrender.com`)
   - Business address
4. Submit verification documents if required
5. Wait for account approval (usually 24-48 hours)

## Step 3: Get Your API Keys

### For Live/Production Keys:
1. Log in to Paystack Dashboard
2. Go to **Settings → API Keys & Webhooks**
3. You'll see two tabs: **Test** and **Live**
4. Click on the **Live** tab (only available after verification)
5. You'll see:
   - **Public Key** (starts with `pk_live_`)
   - **Secret Key** (starts with `sk_live_`)

### For Testing (Development):
1. Stay in the **Test** tab
2. Note the test keys:
   - **Test Public Key** (starts with `pk_test_`)
   - **Test Secret Key** (starts with `sk_test_`)

**⚠️ Important:** Never share your Secret Key publicly!

## Step 4: Configure Webhook

1. In **Settings → API Keys & Webhooks**
2. Scroll to **Webhooks** section
3. Click **Add Webhook**
4. Enter webhook URL: `https://your-domain.com/payments/webhook/paystack/`
5. Select events to listen to:
   - ✅ `charge.success` (important for order confirmation)
   - ✅ `charge.failed` (for tracking failures)
   - ✅ `charge.dispute.created` (optional)
6. Save webhook

## Step 5: Test Payment Integration

### Using Test Credentials:
Use these Paystack test credentials to verify payment flow:

**Test Cards:**
- **Visa Card (Success):** 4111111111111111
  - Expiry: 01/25
  - CVV: 123

- **Visa Card (Failed):** 4000000000000002
  - Expiry: 01/25
  - CVV: 123

- **Mastercard (Success):** 5555555555554444
  - Expiry: 01/25
  - CVV: 123

### Test Payment Flow:
1. Use test public key in frontend
2. Create an order for "Agent Registration Fee"
3. Proceed to payment
4. Use test card details above
5. OTP (if prompted): use any 6 digits
6. Verify payment goes through
7. Check order status updates to "paid"
8. Verify agent gets `is_agent=True`

## Step 6: Environment Variables for K-DATAHUB

### For Development (test keys):
```
PAYSTACK_PUBLIC_KEY=pk_test_XXXXXXXXXXXXXXXXXX
PAYSTACK_SECRET_KEY=sk_test_XXXXXXXXXXXXXXXXXX
```

### For Production (live keys):
```
PAYSTACK_PUBLIC_KEY=pk_live_XXXXXXXXXXXXXXXXXX
PAYSTACK_SECRET_KEY=sk_live_XXXXXXXXXXXXXXXXXX
```

### Add to Render Environment:
1. Go to Render dashboard
2. Select your service
3. Go to **Environment** tab
4. Add new environment variable:
   - Name: `PAYSTACK_PUBLIC_KEY`
   - Value: `pk_live_...` (your live public key)
5. Repeat for `PAYSTACK_SECRET_KEY`

## Step 7: Verify Integration

After deployment, test in production:

1. Navigate to your Render domain
2. Create an order
3. Proceed to payment
4. Use **LIVE card details** (only if live keys are set)
5. Verify:
   - ✅ Payment redirects to Paystack
   - ✅ Payment verification works
   - ✅ Order status updates to "paid"
   - ✅ Agent gets registered (if applicable)
   - ✅ Arkesel SMS is sent

## Troubleshooting

### "Payment initialization failed"
- Check if `PAYSTACK_SECRET_KEY` is set in environment
- Verify SECRET_KEY is not empty or default
- Check if order amount > 0

### Webhook not triggering
- Verify webhook URL is correct in Paystack settings
- Check Paystack webhook logs: Settings → API Keys & Webhooks → Logs
- Ensure `BASE_DOMAIN` is set correctly in settings
- Test webhook manually from Paystack dashboard

### Cards declined in test mode
- Use test cards from Step 5 above
- Ensure you're using test keys (starts with `pk_test_`)
- Try different test card numbers

### Live payments not working
- Verify you're using **live keys** (starts with `pk_live_`)
- Ensure account is verified (Status should be "Approved")
- Use real card details (4111...still works for some tests)
- Check Paystack transaction logs

## Support

- Paystack Documentation: https://paystack.com/docs/
- Paystack Support: https://support.paystack.com/
- K-DATAHUB Support: Contact development team

