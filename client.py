from ftplib import FTP
import os

# Create FTP connection and login as anonymous user
ftp = FTP('')
ftp.connect('127.0.0.1', 2121)
ftp.login()

# Create a text file and upload to FTP server
def uploadFile(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = directory + '\\client.txt'
    f = open(filename, 'w')
    f.write('File to be uploaded to FTP.')
    f.close()
    
    # The file is uploaded to the "server" directory of the server
    ftp.mkd('server')
    ftp.cwd('server')
    ftp.storbinary('STOR ' + 'server.txt', open(filename, 'rb'))
    ftp.quit()

if __name__ == '__main__':
    uploadFile(os.getcwd() + '\\client')
 