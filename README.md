# 👕 KidsSwap

**KidsSwap** is a Django-based web application that allows parents and guardians to buy, sell, and swap quality kids’ clothing. The platform offers a simple, user-friendly interface to list items, manage carts, and track orders.

[Live Site](https://herokuapp.com/)

---

## 🚀 Features

- User authentication (Sign Up, Login, Logout)
- Sell and browse second-hand kids' clothing
- Wishlist functionality
- Shopping cart and secure checkout
- Order confirmation and tracking
- Product search with filters (category, size, price)
- Responsive design with Tailwind CSS
- Flash messages for user actions
- Admin management for listings

---

## 🛠 Tech Stack

- **Backend:** Django, Python
- **Frontend:** HTML, Tailwind CSS, JavaScript
- **Database:** SQLite (default for development)
- **Others:** Font Awesome, Swiper.js for carousels, Django Crispy Forms

---

## 📸 Screenshots

Homepage

![KidSwap](documentation\images\homepage_kidswap.png "Navbar")

Categories

![KidSwap](documentation\images\category_options.png "Categories")

Filter

![KidSwap](documentation\images\filter.png "Filter")

Listing page

![KidSwap](documentation\images\sell.png "Listing")

Shopping Cart

![KidSwap](documentation\images\cart.png "Cart")

Confirmation

![KidSwap](documentation\images\confirmed.png "Confirmation")

Wishlist

![KidSwap](documentation\images\wishlist.png "Wishlist")

About Page

![KidSwap](documentation\images\about.png "About")

Footer

![KidSwap](documentation\images\footer.png "Footer")

Login

![KidSwap](documentation\images\login.png "Login")

Mobile Version

![KidSwap](documentation\images\mobile.png "Mobile")

---

## ✨ Usage

- **Buyers** can search and filter for clothing, add items to their cart, checkout, and track their orders.
- **Sellers** can list clothing items with images, descriptions, and other details.
- **Users** can log in to manage their wishlist, view past orders, and update account information.

---

## ✅ To Do / Improvements

- [ ] Add payment gateway integration
- [ ] Implement email notifications for orders and listings
- [ ] Add user profile pages with avatars
- [ ] Enable item reviews and ratings
- [ ] Improve mobile responsiveness and performance

---

## 🤝 Contributing

Pull requests are welcome! Please open an issue first to discuss any major changes you'd like to propose.

---

## 📝 License

This project is licensed under the **MIT License**. See the `LICENSE` file for more details.

---

## 💬 Contact

For questions, suggestions, or feedback, feel free to reach out via [estelle.specht@gmail.com] or open an issue on this repository.


## 🔧 Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/kidsswap.git
cd kidsswap

Create a virtual environment and activate it

python -m venv env
source env/bin/activate  # or env\Scripts\activate on Windows

 - Install dependencies
```bash
pip install -r requirements.txt

- Create a superuser (optional)
```bash
python manage.py createsuperuser

- Start the development server
```bash
python manage.py runserver

- Visit
Open http://127.0.0.1:8000 in your browser.

