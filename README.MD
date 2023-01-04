# Pigs Can Fly Labs
A small, e-commerce website built with Python and Django that uses Stripe and their API for payment processing and checkout.

Aside from the regular features like sign up and login, the website has a Shopping Cart and Checkout functionality. Products can be added and managed from the admin panel that Django provides out of the box. Users can also subscribe to receive updates on their email address.

This codebase has placeholder data (lorem ipsum and others) and is meant to just show my skillset and portfolio. The actual website is obviously with my client :).

## Images
![image](https://i.imgur.com/oCG6tvC.png)
![image](https://i.imgur.com/HMRjpx4.png)

## How To Use?
1. Start by cloning this repository.
2. Apply your migrations in Django.
> `python manage.py migrate`
3. Create an admin account in your database.
> `python manage.py createsuperuser`
4. Run the Django development server.
> `python manage.py runserver`

Now, you can use the site in localhost. You can add and manage products in the admin panel. 

## Reusing
Building an E-commerce website in Django? Feel free to use this project as a starting point. Just make sure to replace the templates with your own site to match your look and theme. 

If you're using Stripe, make sure to replace the STRIPE_API_KEY in settings.py before using. The current one is an outdated test key. 

Also the actual logic of checkouts is handled in main/payments.py file. Modify that if you aren't using Stripe.