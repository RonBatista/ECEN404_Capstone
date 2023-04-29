import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

pri_key = "/Users/Jose Landivar/.ssh/id_rsa"

ssh.connect('158.101.127.212', port=22, username='ubuntu', pkey=)

stdin, stdout, stderr = ssh.exec_command('ls')

print(stdout.read().decode('utf-8'))
