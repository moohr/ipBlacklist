# We're just going to use mubeng because it is efficient.
# You should NOT enable this option normally.
import os


def checkproxy(proxylist):
    alive = []

    # get mubeng binaries
    mubeng_url = 'https://github.com/kitabisa/mubeng/releases/download/v0.14.1/mubeng_0.14.1_linux_amd64'
    os.system("wget -O mubeng " + mubeng_url)
    os.system("chmod +x mubeng")
    # check http
    with open('start.txt', 'w') as file:
        for proxy in proxylist:
            file.write("http://"+proxy + "\n")
            file.write("socks4://" + proxy + "\n")
            file.write("socks5://" + proxy + "\n")
    os.system("./mubeng -f start.txt -o live.txt -c -g 1000")
    with open('live.txt', 'r') as file:
        alive.extend(file.readlines())
    return alive


