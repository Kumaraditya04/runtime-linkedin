# Oracle Cloud "Always Free" Deployment Guide

This guide covers deploying LeadRadar AI to an Oracle Cloud ARM A1 Compute Instance using Docker. This is the recommended permanent free hosting solution as it provides 24GB of RAM, which easily handles Playwright's Chromium memory requirements.

---

## 1. Provision the Oracle VM

1. Sign up / Log in to Oracle Cloud.
2. Go to **Compute** -> **Instances** -> **Create Instance**.
3. **Image and Shape**:
   - Image: `Canonical Ubuntu 22.04`
   - Shape: `Ampere ARM (VM.Standard.A1.Flex)`
   - OCPUs: `4`
   - Memory: `24 GB`
4. **Networking**: Ensure you assign a Public IP.
5. **Add SSH Keys**: Generate or upload your public SSH key to access the server.
6. Click **Create**.

---

## 2. Configure VCN Firewall (Oracle Dashboard)

Oracle blocks all inbound ports by default.
1. Click on the attached **Subnet** in the instance details.
2. Click on the **Default Security List**.
3. Add Ingress Rules for:
   - **80** (HTTP)
   - **443** (HTTPS)
   - **3000** (Frontend)
   - **8000** (Backend API)
   - *Source CIDR: `0.0.0.0/0`*

---

## 3. Configure Ubuntu Firewall (iptables)

SSH into your new instance:
```bash
ssh ubuntu@YOUR_INSTANCE_IP
```

Oracle's Ubuntu image also runs a local iptables firewall. Open the ports:
```bash
sudo iptables -I INPUT -p tcp -m tcp --dport 8000 -j ACCEPT
sudo iptables -I INPUT -p tcp -m tcp --dport 3000 -j ACCEPT
sudo netfilter-persistent save
```

---

## 4. Install Docker & Docker Compose

Run the official Docker installation script:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

Add your user to the docker group (so you don't need `sudo`):
```bash
sudo usermod -aG docker $USER
newgrp docker
```

---

## 5. Clone and Deploy LeadRadar AI

Clone your repository:
```bash
git clone https://github.com/YOUR_USERNAME/runtime-linkedin.git
cd runtime-linkedin
```

Create your `.env` file:
```bash
cp .env.example .env
nano .env
```
*(Add your `LINKEDIN_LI_AT`, `SECRET_KEY`, etc. Make sure to set `NEXT_PUBLIC_API_URL=http://YOUR_INSTANCE_IP:8000/api/v1` if you are not setting up a reverse proxy yet).*

Build and start the containers in the background:
```bash
docker compose up -d --build
```

---

## 6. Verification

- **Backend API**: `http://YOUR_INSTANCE_IP:8000/api/v1/internal/health`
- **Frontend Dashboard**: `http://YOUR_INSTANCE_IP:3000`

> **Note**: Since the backend uses the official Playwright Docker image, you will **not** experience any missing browser binary issues. The browser is pre-packaged inside the container!
