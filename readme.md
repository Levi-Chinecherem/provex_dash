# Provex Investment Platform

Provex is an investment platform that allows users to fund their accounts, choose investment plans, and withdraw funds. The platform supports various investment options such as USDT TRC20, USDT ERC20, and BTC.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- User registration and authentication
- Funding accounts with various cryptocurrencies
- Investment plans with different durations and returns
- Withdrawal requests and approvals
- Real-time account summaries

## Installation

1. Clone the repository:

   ```bash
   git clonehttps://github.com/Levi-Chinecherem/provex_dash.git
   ```
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Apply migrations:

   ```bash
   python manage.py migrate
   ```
4. Create a superuser for admin access:

   ```bash
   python manage.py createsuperuser
   ```
5. Run the development server:

   ```bash
   python manage.py runserver
   ```
6. Access the application at http://localhost:8000/ and the admin panel at http://localhost:8000/admin/

## Usage

1. Create a user account.
2. Fund your account using the available cryptocurrencies.
3. Choose an investment plan based on your preferences.
4. Monitor your account summary and investment returns in real-time.
5. Request withdrawals and await approval.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Create a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
