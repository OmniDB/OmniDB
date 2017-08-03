import subprocess

def call(command):
	p = subprocess.run(
		command,
		shell=True,
		stdout=subprocess.PIPE,
		#stderr=subprocess.PIPE
	)
	#if p.stderr:
	#	raise Exception(p.stderr)
	#else:
	#	return p.stdout.decode('utf-8').split('\n')[:-1]
	return p.stdout.decode('utf-8').split('\n')[:-1]

pwd = call('pwd')

print('Copying all external dependencies for omnidb-server, except glibc... ', end='')
serverdeps = {}
servererrors = {}
libs = call('ls -1 {0}/packages/omnidb-server/*.so*'.format(pwd[0]))
for lib in libs:
	ldd = call('ldd {0}'.format(lib))
	for d in ldd:
		dep = d.replace('\t', '')
		tmp = dep.split(' => ')
		if len(tmp) > 1 and pwd[0] not in tmp[1] and 'libc.so' not in tmp[0]:
			if 'not found' in tmp[1]:
				servererrors[lib] = tmp[0]
			else:
				if len(tmp[1].split(' ')[0].strip()) > 0:
					serverdeps[tmp[0]] = tmp[1].split(' ')[0]
for key, value in serverdeps.items():
	call('cp -f {0} {1}/packages/omnidb-server/{2}'.format(value, pwd[0], key))
print('Done')

print('Copying all external dependencies for omnidb-app, except glibc... ', end='')
appdeps = {}
apperrors = {}
libs = call('ls -1 {0}/packages/omnidb-app/*.so*'.format(pwd[0]))
for lib in libs:
	ldd = call('ldd {0}'.format(lib))
	for d in ldd:
		dep = d.replace('\t', '')
		tmp = dep.split(' => ')
		if len(tmp) > 1 and pwd[0] not in tmp[1] and 'libc.so' not in tmp[0]:
			if 'not found' in tmp[1]:
				apperrors[lib] = tmp[0]
			else:
				if len(tmp[1].split(' ')[0].strip()) > 0:
					appdeps[tmp[0]] = tmp[1].split(' ')[0]
for key, value in appdeps.items():
	call('cp -f {0} {1}/packages/omnidb-app/{2}'.format(value, pwd[0], key))
print('Done')
