name: CI/CD for Flask App (Without Docker Compose)

on:
  push:
    branches:
      - main  # Trigger pipeline on push to main

jobs:
  build-and-push:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Login to Docker Hub
        run: echo "${{ secrets.DOCKER_PASSWORD }}" | docker login -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin

      - name: Build and Push Docker Image
        run: |
          docker build -t ${{ secrets.DOCKER_USERNAME }}/flask-attendance-app .
          docker push ${{ secrets.DOCKER_USERNAME }}/flask-attendance-app

  deploy:
    runs-on: ubuntu-latest
    needs: build-and-push

    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Deploy to AWS EC2
        run: |
          echo "${{ secrets.AWS_KEY }}" > private_key.pem
          chmod 600 private_key.pem

          ssh -o StrictHostKeyChecking=no -i private_key.pem ${{ secrets.AWS_USER }}@${{ secrets.AWS_HOST }} << 'EOF'

            # Set up Docker network (if needed)
            docker network create app_network || true

            # Stop and remove existing MySQL and Flask containers if they exist
            docker stop mysql-db || true
            docker rm mysql-db || true
            docker stop flask-app || true
            docker rm flask-app || true

            # Run MySQL container
            docker run -d \
              --name mysql-db \
              --network app_network \
              -e MYSQL_ROOT_PASSWORD=root \
              -e MYSQL_DATABASE=attendance_db \
              -p 3306:3306 \
              mysql:latest

            # Wait for MySQL to fully start
            echo "Waiting for MySQL to initialize..."
            sleep 30

            # Create database (this is optional if you want to ensure it exists)
            docker exec mysql-db mysql -uroot -prootpassword -e "CREATE DATABASE IF NOT EXISTS attendance_db;"

            # Pull latest Flask app
            docker login -u ${{ secrets.DOCKER_USERNAME }} -p ${{ secrets.DOCKER_PASSWORD }}
            docker pull ${{ secrets.DOCKER_USERNAME }}/flask-attendance-app

            # Run Flask app container
            docker run -d \
              --name flask-app \
              --network app_network \
              -p 5000:5000 \
              -e DB_HOST=mysql-db \
              -e DB_USER=root \
              -e DB_PASSWORD=root \
              -e DB_NAME=attendance_db \
              ${{ secrets.DOCKER_USERNAME }}/flask-attendance-app

          EOF
