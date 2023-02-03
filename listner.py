import socket
import rsa

# Encryption setup
public_key, private_key = rsa.newkeys(1024)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Connection made to get local ip
s.connect(("192.168.1.1", 80))
host = s.getsockname()[0]
s.close()

#host = "192.168.1.11"
print(f"Host is {host}")
port = 8787

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((host, port))

s.listen(5)

print("listening...")
c, addr = s.accept()

# Connection made
print(f"Got connection from {addr}")

c.send(b"Connected to the listener")

# Send encryption public keyc.send(public_key.save_pkcs1())
#print(f"Sent: {public_key.save_pkcs1()}")
c.send(public_key.save_pkcs1())
other_pub_key = c.recv(1024)
other_pub_key = rsa.PublicKey.load_pkcs1(other_pub_key)

while True:
    message = c.recv(1024)
    plaintext = rsa.decrypt(message, private_key)
    if not message:
        break

    #print(f"Received message: {message.decode()}")
    print(f"\u001b[34mReceived message: {plaintext.decode()}")
    if plaintext.decode() == "exit": break

    message = input("\u001b[0mEnter message to send: ")
    if message == "exit": break
    ciphertext = rsa.encrypt(message.encode(), other_pub_key)
    c.send(ciphertext)

c.close()
