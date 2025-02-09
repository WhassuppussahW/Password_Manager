# Password_Manager

Secure Password Manager - Cloud-Based Solution
🔐 About the Project
This project is a fully secured password manager designed with robust cryptographic mechanisms, built on a cloud infrastructure using Oracle Cloud Free Tier. The architecture ensures high availability, security, and scalability, leveraging Flask, Docker, and Oracle Autonomous Database (ATP). It offers strong password encryption, auto-generated secure passwords, and master-password-based encryption/decryption for user credentials.
Additionally, setting up this project requires configuring Oracle Cloud security policies, ensuring correct permissions, and handling certificates and vaults for secure authentication. Users must set up the Oracle ATP database with proper access controls, define networking configurations, and manage authorization inside the Virtual Private Server (VPS) to maintain the highest security standards.
🌍 Project Architecture
The password manager operates through a multi-layered cloud infrastructure, ensuring that all sensitive data is encrypted before being stored in the database. The master password itself is never stored, enhancing security and preventing unauthorized access.
•	Oracle Cloud Load Balancer (Layer 4 & 7) for traffic distribution and security. Thanks to the load balancer being used on the client side, any hack attempt on the password manager would include Oracle in the scope, which acts as a strong deterrent. Additionally, Oracle handles maintenance, reducing the need for manual server management and minimizing configuration errors.
•	Backend Virtual Machine (VM) running Dockerized Flask application.
•	Oracle Autonomous Database (ATP) for secure credential storage.
•	Secure API Communication with encrypted transactions, strong authentication, and strict access control.
🛠️ Tech Stack
Backend:
•	Python (Flask) - Web framework
•	cx_Oracle - Oracle DB integration
•	Cryptography - Secure encryption and decryption
•	Werkzeug Security - Secure password hashing
•	Gunicorn - Production WSGI server
•	Docker - Containerization for easy deployment
Frontend:
•	HTML5 & CSS3 - Responsive and mobile-friendly design
Database:
•	Oracle Autonomous Database (ATP) - Scalable and secure storage
•	UUIDs for unique user identification
•	Fernet & PBKDF2 encryption for storing credentials securely
Security Features:
•	Full OWASP Top 10 protection
•	Master Password Encryption: User passwords are encrypted using a derived key from their master password.
•	AES-GCM Encryption: Protects salt storage with strong cryptography.
•	Base64 Encoding: Ensures database-storable format while keeping security intact.
•	Session Management: Secure authentication & CSRF protection.
•	Multi-Layered Firewall Protection: Oracle Cloud Security policies.
•	Strict Role-Based Access Control: Users have predefined roles and permissions within the application.
🔑 Key Features
✅ Secure password storage with encrypted vault
✅ Automatic password generation for secure credentials
✅ Mobile-responsive UI
✅ Master password protection for added security
✅ Database-backed storage using Oracle ATP
✅ Fully containerized with Docker for easy deployment
✅ Gunicorn integration for production-grade performance
✅ Flask-based API with secure endpoints
✅ Modular Code Structure for ease of maintenance and customization
🏗️ Setup & Deployment
Prerequisites:
•	Oracle Cloud Free Tier Account
•	Oracle ATP configured with Wallet access
•	Oracle Cloud Vault for securing keys and credentials
•	Load Balancer properly configured with security policies
•	Docker & Docker-Compose installed on VM
•	Proper role-based authorization configured within the VPS
•	SSL/TLS Certificates managed for secure HTTPS access
Installation:
1.	Clone the repository:
2.	git clone https://github.com/yourusername/password-manager.git
3.	cd password-manager
4.	Set up environment variables (.env file):
5.	FLASK_SECRET_KEY=your_flask_secret
6.	DB_USERNAME=your_db_user
7.	DB_PASSWORD=your_db_password
8.	DB_URL=your_db_url
9.	ENCRYPTION_KEY=your_encryption_key
10.	Build and run the Docker container:
11.	docker-compose up --build
12.	Access the application:
13.	http://load_balancer_public_ip
📝 API Endpoints
Authentication:
•	POST /sign-in → Register a new user
•	POST /login → Authenticate a user
•	GET /logout → Log out user
Password Management:
•	GET /main-page → Choose the desired password management option
•	POST /add-password → Store an encrypted password
•	GET /view-passwords → Retrieve stored passwords
•	DELETE /delete-password → Remove a stored password
Health Check:
•	GET /health → Load balancer health check (or any other system status endpoint)
📜 License
MIT License. Feel free to modify and contribute! 🎉
🤝 Contributing
Pull requests are welcome! For significant changes, open an issue to discuss improvements.
________________________________________
Developed for study purposes to understand web application security, cloud infrastructure, and Python development. 📚💻
