from starcluster import clustersetup
from starcluster.logger import log

class RepoFixer(clustersetup.DefaultClusterSetup):

    def __init__(self):
        super(RepoFixer, self).__init__()
        log.info('Initializing Repository Fixer plugin')

        self.commands = [
            "sed -i -e 's/archive.ubuntu.com\|security.ubuntu.com/old-releases.ubuntu.com/g;s/us-east-1.ec2.//g' /etc/apt/sources.list",
            "dpkg --add-architecture i386"
        ]

    def run(self, nodes, master, user, user_shell, volumes):
        log.info('Fixing outdated repos & adding i386 architecture in cluster.')
        for node in nodes:
            self.pool.simple_job(node.ssh.execute, (" && ".join(self.commands)), jobid=node.alias)
        self.pool.wait(len(nodes))

    def on_add_node(self, new_node, nodes, master, user, user_shell, volumes):
        log.info('Fixing outdated repos & adding i386 architecture on node %s.' % new_node.alias)
        new_node.ssh.execute(" && ".join(self.commands))

    def on_remove_node(self, node, nodes, master, user, user_shell, volumes):
        raise NotImplementedError('on_remove_node method not implemented')
