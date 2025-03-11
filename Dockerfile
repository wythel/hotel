# 使用 Ubuntu 作為基礎映像
FROM --platform=linux/amd64 ubuntu:latest

# 設定環境變數，避免安裝過程中的交互提示
ENV DEBIAN_FRONTEND=noninteractive

# 更新套件列表並安裝必要的依賴項
RUN apt-get update && \
    apt-get install -y wget gnupg software-properties-common && \

    # 安裝 Python 3.12 和 pip
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.12 python3.12-venv python3.12-dev python3-pip && \

    # 下載 Google Chrome 安裝包
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \

    # 安裝 Google Chrome
    dpkg -i google-chrome-stable_current_amd64.deb || apt-get install -f -y && \

    # 清理不必要的檔案，減少映像大小
    rm -rf /var/lib/apt/lists/* google-chrome-stable_current_amd64.deb
