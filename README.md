# Secure Password Manager - Cloud-Based Solution

## 🔐 About the Project
This project is a fully secured password manager designed with robust cryptographic mechanisms, built on a cloud infrastructure using Oracle Cloud Free Tier. The architecture ensures high availability, security, and scalability, leveraging Flask, Docker, and Oracle Autonomous Database (ATP). It offers:

- Strong password encryption
- Auto-generated secure passwords
- Master-password-based encryption/decryption for user credentials

Additionally, setting up this project requires:
- Configuring Oracle Cloud security policies
- Ensuring correct permissions
- Handling certificates and vaults for secure authentication
- Setting up the Oracle ATP database with proper access controls
- Defining networking configurations
- Managing authorization inside the Virtual Private Server (VPS) to maintain the highest security standards

## 🌍 Project Architecture
The password manager operates through a multi-layered cloud infrastructure, ensuring that all sensitive data is encrypted before being stored in the database. The master password itself is never stored, enhancing security and preventing unauthorized access.

- **Oracle Cloud Load Balancer** (Layer 4 & 7) for traffic distribution and security. Any hack attempt would include Oracle in the scope, acting as a strong deterrent.
- **Backend Virtual Machine (VM)** running Dockerized Flask application.
- **Oracle Autonomous Database (ATP)** for secure credential storage.
- **Secure API Communication** with encrypted transactions, strong authentication, and strict access control.

## 🛠️ Tech Stack

### **Backend:**
- Python (Flask) - Web framework
- cx_Oracle - Oracle DB integration
- Cryptography - Secure encryption and decryption
- Werkzeug Security - Secure password hashing
- Gunicorn - Production WSGI server
- Docker - Containerization for easy deployment

### **Frontend:**
- HTML5 & CSS3 - Responsive and mobile-friendly design

### **Database:**
- Oracle Autonomous Database (ATP) - Scalable and secure storage
- UUIDs for unique user identification
- Fernet & PBKDF2 encryption for storing credentials securely

### **Security Features:**
- Full OWASP Top 10 protection
- **Master Password Encryption:** User passwords are encrypted using a derived key from their master password.
- **AES-GCM Encryption:** Protects salt storage with strong cryptography.
- **Base64 Encoding:** Ensures database-storable format while keeping security intact.
- **Session Management:** Secure authentication & CSRF protection.
- **Multi-Layered Firewall Protection:** Oracle Cloud Security policies.
- **Strict Role-Based Access Control:** Users have predefined roles and permissions within the application.

## 🔑 Key Features

✅ Secure password storage with encrypted vault  
✅ Automatic password generation for secure credentials  
✅ Mobile-responsive UI  
✅ Master password protection for added security  
✅ Database-backed storage using Oracle ATP  
✅ Fully containerized with Docker for easy deployment  
✅ Gunicorn integration for production-grade performance  
✅ Flask-based API with secure endpoints  
✅ Modular Code Structure for ease of maintenance and customization  

## 🏗️ Setup & Deployment

### **Prerequisites:**
- Oracle Cloud Free Tier Account
- Oracle ATP configured with Wallet access
- Oracle Cloud Vault for securing keys and credentials
- Load Balancer properly configured with security policies
- Docker & Docker-Compose installed on VM
- Proper role-based authorization configured within the VPS
- SSL/TLS Certificates managed for secure HTTPS access

### **Installation:**
```bash
# Clone the repository
git clone https://github.com/WhassuppussahW/password-manager.git
cd password-manager

# Set up environment variables (.env file)
echo "FLASK_SECRET_KEY=your_flask_secret" >> .env
echo "DB_USERNAME=your_db_user" >> .env
echo "DB_PASSWORD=your_db_password" >> .env
echo "DB_URL=your_db_url" >> .env
echo "ENCRYPTION_KEY=your_encryption_key" >> .env

# Build and run the Docker container
docker-compose up --build
```

### **Access the application:**
```bash
http://load_balancer_public_ip
```

## 📝 API Endpoints

### **Authentication:**
```http
POST /sign-in         # Register a new user
POST /login           # Authenticate a user
GET /logout           # Log out user
```

### **Password Management:**
```http
GET /main-page         # Choose the desired password management option
POST /add-password     # Store an encrypted password
GET /view-passwords    # Retrieve stored passwords
DELETE /delete-password # Remove a stored password
```

### **Health Check:**
```http
GET /health           # Load balancer health check (or any other system status endpoint)
```

## 📜 License

MIT License. Feel free to modify and contribute! 🎉

## 🤝 Contributing
Pull requests are welcome! For significant changes, open an issue to discuss improvements.

---
Developed for study purposes to understand web application security, cloud infrastructure, and Python development. 📚💻

