FROM --platform=linux/amd64 python:3.9.21-slim

RUN apt-get update && \
    apt-get install -y nano htop curl git wget unzip && \
    rm -rf /var/lib/apt/lists/*


RUN pip install black

RUN curl -sL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

RUN wget https://releases.hashicorp.com/terraform/1.9.5/terraform_1.9.5_linux_amd64.zip && \
    unzip terraform_1.9.5_linux_amd64.zip && \
    mv terraform /usr/local/bin/ && \
    rm terraform_1.9.5_linux_amd64.zip

# Instalar NVM
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash

RUN echo 'export NVM_DIR="$HOME/.nvm"' >> ~/.bashrc && \
    echo '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"' >> ~/.bashrc
    RUN apt-get update && \
    apt-get install -y openjdk-17-jdk && \
    rm -rf /var/lib/apt/lists/*
    
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install


RUN bash -c "source ~/.bashrc && nvm install 20.18.1 && nvm use 20.18.1"

WORKDIR /workspace


CMD ["bash"]   