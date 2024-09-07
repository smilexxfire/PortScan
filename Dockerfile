FROM python:3.9.19
COPY . /app
WORKDIR /app
RUN apt-get update && apt-get install nmap -y && rm -rf /var/lib/apt/lists/* && pip install -r requirements.txt && chmod +x thirdparty/* && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
CMD ["python", "portscan_worker.py", "|| exit 1"]