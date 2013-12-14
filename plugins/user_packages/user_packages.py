from base import Task
from common import phases
import os
from common.tasks.packages import ImagePackages
from common.tasks.host import CheckPackages
from common.tasks.apt import AptUpgrade
from common.tasks.locale import GenerateLocale


class AddUserPackages(Task):
	description = 'Adding user defined packages to the image packages'
	phase = phases.system_modification
	predecessors = [AptUpgrade, GenerateLocale]

	def run(self, info):
		if 'repo' not in info.manifest.plugins['user_packages']:
			return
		from common.tools import log_check_call
		cmd = ['/usr/sbin/chroot', info.root,
			'/usr/bin/env','DEBIAN_FRONTEND=noninteractive',
			'/usr/bin/apt-get', 'install',
			'--force-yes', '--assume-yes']
		cmd.extend(info.manifest.plugins['user_packages']['repo'])
		log_check_call(cmd)


class AddLocalUserPackages(Task):
	description = 'Adding user local packages to the image packages'
	phase = phases.system_modification
	predecessors = [AddUserPackages]

	def run(self, info):
		if 'local' not in info.manifest.plugins['user_packages']:
			return

		import stat
		rwxr_xr_x = (stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR |
		             stat.S_IRGRP                | stat.S_IXGRP |
		             stat.S_IROTH                | stat.S_IXOTH)

		from shutil import copy
		from common.tools import log_check_call

		for pkg in info.manifest.plugins['user_packages']['local']:
			script_src = os.path.normpath(pkg)
			script_dst = os.path.join(info.root, 'tmp/'+os.path.basename(script_src))
			copy(script_src, script_dst)
			os.chmod(script_dst, rwxr_xr_x)

			log_check_call(['/usr/sbin/chroot', info.root,
			                '/usr/bin/dpkg', '--install', '/tmp/'+os.path.basename(script_src)])
