# CI/CD Setup with GitHub Actions and AWS EC2 (Docker Deployment)

This guide explains how to create a Continuous Integration and Continuous Deployment (CI/CD) pipeline using GitHub Actions, Docker, and an AWS EC2 instance.
The pipeline will automatically build a Docker image, push it to Docker Hub, and deploy it to your EC2 instance whenever code is pushed to GitHub.

---

## Step 1: Create an AWS EC2 Instance

1. Go to the **AWS Management Console** → **EC2** → **Instances** → **Launch Instance**.
2. Choose:

   * **AMI:** Ubuntu Server 22.04 LTS (Free Tier eligible)
   * **Instance Type:** t2.micro (Free Tier)
   * **Key Pair:** Create a new one (download the `.pem` file)
3. In the EC2 Security Group, add the following **Inbound Rules**:

   ```
   22 (SSH)
   80 (HTTP)
   443 (HTTPS)
   5000 (Custom TCP)
   ```
4. Launch the instance and note the **Public IPv4 Address**.

---

## Step 2: Connect to the EC2 Instance

From your terminal, connect to your instance:

```bash
chmod 400 your-key.pem
ssh -i "your-key.pem" ubuntu@<EC2_PUBLIC_IP>
```

---

## Step 3: Install Docker on EC2

Run the following commands to install and configure Docker:

```bash
sudo apt update -y
sudo apt install -y docker.io
sudo usermod -aG docker $USER
sudo systemctl enable docker
sudo systemctl start docker
sudo reboot
```

After the reboot, reconnect to your EC2 instance:

```bash
ssh -i "your-key.pem" ubuntu@<EC2_PUBLIC_IP>
```

Verify that Docker is running:

```bash
sudo systemctl status docker
docker ps
```

If there are no errors, Docker is installed and running correctly.

---

## Step 4: Add GitHub Secrets

In your GitHub repository:

1. Go to **Settings → Secrets and variables → Actions → New repository secret**
2. Add the following secrets:

| Secret Name       | Description                                                |
| ----------------- | ---------------------------------------------------------- |
| `AWS_HOST`        | Your EC2 public IP address                                 |
| `AWS_KEY`         | The content of your `.pem` key file (copy the entire text) |
| `AWS_USER`        | Typically `ubuntu` (default for Ubuntu AMI)                |
| `DOCKER_USERNAME` | Your Docker Hub username                                   |
| `DOCKER_PASSWORD` | Your Docker Hub Personal Access Token (PAT)                |

**Note:**
To create a Docker Hub PAT, go to Docker Hub → Account Settings → Security → New Access Token.

---

## Step 5: Configure GitHub Actions Workflow

Create the following folder structure inside your project:

```
.github/
└── workflows/
    └── deploy.yaml
```
and write your actions in .yaml file.

### Explanation of the Workflow

1. **Trigger:** Executes automatically on every push to the `main` branch.
2. **Checkout:** Pulls the latest code from the repository.
3. **Docker Build:** Builds a Docker image and pushes it to Docker Hub.
4. **SSH Deploy:** Connects to your EC2 instance, stops the old container, pulls the new image, and starts the updated container on port `5000`.

---

## Step 6: Trigger the Deployment

Make any small change to your project (for example, update a file) and push it:

```bash
git add .
git commit -m "trigger CI/CD deployment"
git push origin main
```

Go to your **GitHub repository → Actions tab** to view the workflow running.
Once it completes, the new version of your app will be deployed automatically to your EC2 instance.

---

## Step 7: Verify the Deployment

Open a web browser and visit:

```
http://<EC2_PUBLIC_IP>:5000
```

If everything is configured correctly, your application will appear in the browser.

---

## Summary

| Step | Task                | Description                                     |
| ---- | ------------------- | ----------------------------------------------- |
| 1    | Create EC2 Instance | Launch an Ubuntu server and open required ports |
| 2    | Install Docker      | Set up Docker for container deployment          |
| 3    | Add GitHub Secrets  | Securely store credentials for deployment       |
| 4    | Configure Workflow  | Automate build, push, and deploy                |
| 5    | Push Code           | Trigger the CI/CD process                       |
| 6    | Access App          | View your deployed application on the browser   |

---

## Additional Recommendations

* Map your domain name to the EC2 IP using DNS for easier access.
* For production environments, consider using **Nginx** or **Traefik** as a reverse proxy.
* Tag Docker images with versions (e.g., `myapp:v1.0.0`) to maintain release history.
* Use GitHub environments or branch protection for deployment control.