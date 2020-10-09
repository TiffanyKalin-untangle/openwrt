#!/bin/python
import subprocess 

ignore = [
        '.dockerignore',
        '.gitignore',
        '.travis',
        'Dockerfile.build',
        'Dockerfile.test',
        'Jenkinsfile',
        'admin',
        'build.sh',
        'build',
        'caswell-rssi-leds',
        'caswell-wifi-led',
        'classd',
        'configs',
        'container',
        'crash-collector',
        'docker-compose',
        'docs',
        'feeds.conf.mfw',
        'feeds.conf.untangle',
        'geoip-database',
        'create-branch.sh',
        'get-binaries.sh',
        'git-remote-describe.sh',
        'git-remote-find-tag.sh',
        'golang',
        'jsonschema',
        'kmod-gpio-nuvoton',
        'libnavl',
        'libnftnl',
        'license-scripts',
        'mfw-schema-v1.json',
        'mfw',
        'nftables',
        'kmod-nft-dict',
        'openvpn-proto',
        'packetd',
        'patches',
        'pyconnector',
        'python3-vcversioner',
        'sdwan-vbox-helper',
        'sync-settings',
        'test-agent.sh',
        'untangle-python-sync-setting',
        'upgrade-scripts',
        'version-images.sh',
        'version.mk',
        'wan-manager',
        'README',
        'update-subtrees.py',
        'subtrees.yaml'
        ]

#subprocess.call(("git", "log", "--author=Brett", "--author=Delafond", "--author='John Coffin'", "--author=Sommerville", "--author='Dirk Morris'", "--author=Hadarau", "--format=%H %an", "--reverse"))

commits=open("git_log_committer_all")
thisset = set()

total_count=0
for l in commits:
    commit = l.split(' ')[0]

    cmd=("git", "diff-tree", "--no-commit-id", "--name-only", "-r",  commit)

    ps = subprocess.check_output(cmd).strip()

    added_to_set=False
    if len(ps) > 0:
        for file_name in ps.split('\n'):
            add_to_set=True
            first=file_name.split('/')[0]
            for i in ignore:
                if i in first:
                   add_to_set=False
                   break
            if add_to_set:
                thisset.add(file_name)
                added_to_set=True
    if added_to_set:
        total_count=total_count+1
        print(l.strip())

sortedset=sorted(thisset)
for s in sortedset:
    print s
print len(sortedset)
commits.close()


