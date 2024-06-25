# Banada Backend(반하다 소개팅 앱)

### 주요 기능
- 하루 4번 랜덤으로 이성을 소개
- 연애 스타일에 관한 질문과 선택지를 제공하고, 결과에 따라 상대방과 연애 스타일이 어느 정도 일치하는지 표시
- 무료 재화와 유료 재화를 나눠서 사용
- 호감 표시 / 유료 재화를 사용해 메시지 전송
- 양방향 호감 표시할 경우 매칭으로 연락처를 주고 받을 수 있음

### CI/CD
- CI: main 브랜치에 push 발생 시 docker image build 및 docker hub에 이미지 push
```yaml
name: CI

on:
  push:
    branches:
      - main

jobs:
  build-and-push-docker-image:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v1

      - name: Login to DockerHub
        uses: docker/login-action@v1
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Build and push Docker image
        uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: ${{ secrets.DOCKER_USERNAME }}/banada_be:latest
```
- CD: CI 과정이 완료된 후 ssh 접속으로 docker-compose 파일을 배포 및 실행
```yaml
name: CD

on:
  workflow_run:
    workflows: ["CI"]
    types:
      - completed

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Copy Docker Compose files via SSH
        uses: appleboy/scp-action@v0.1.3
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SERVER_SSH_KEY }}
          source: "nginx.conf,docker-compose.yml,docker-compose.prod.yml"
          target: "/home/${{ secrets.SERVER_USER }}/banada_backend/"

      - name: Create .env file on server
        uses: appleboy/ssh-action@v0.1.6
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SERVER_SSH_KEY }}
          script: |
            echo "${{ secrets.ENV_VARS }}" > /home/${{ secrets.SERVER_USER }}/banada_backend/.env

      - name: Install Docker and Docker Compose if needed
        uses: appleboy/ssh-action@v0.1.6
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SERVER_SSH_KEY }}
          script: |
            if ! command -v docker &> /dev/null
            then
              echo "Docker not found. Installing Docker..."
              curl -fsSL https://get.docker.com -o get-docker.sh
              sh get-docker.sh
              sudo usermod -aG docker $USER
              newgrp docker
              rm get-docker.sh
            else
              echo "Docker is already installed."
            fi

            if ! command -v docker-compose &> /dev/null
            then
              echo "Docker Compose not found. Installing Docker Compose..."
              sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
              sudo chmod +x /usr/local/bin/docker-compose
            else
              echo "Docker Compose is already installed."
            fi

      - name: Deploy to server via SSH
        uses: appleboy/ssh-action@v0.1.6
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SERVER_SSH_KEY }}
          script: |
            cd /home/${{ secrets.SERVER_USER }}/banada_backend
            docker-compose down --remove-orphans
            docker-compose -f docker-compose.prod.yml pull
            docker-compose -f docker-compose.prod.yml up -d
```

### Oauth2(예정)
