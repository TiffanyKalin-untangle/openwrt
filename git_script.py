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
        'subtrees.yaml',
        'LICENSE'
        ]

our_authors = [
        'Brett Mast',
        'John Coffin',
        'Delafond',
        'Sommerville',
        'Dirk Morris',
        'Blaise',
        'Hotz',
        ]

doing_commits=False
use_differing_files=True
if doing_commits:
    commits=open("git_log_all")
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
            #print(l.strip())

    sortedset=sorted(thisset)
    #for s in sortedset:
    #    print s
    print total_count
    commits.close()
elif use_differing_files:
    differ_files=open("differing_files")
    differing_files=[]

    for d_file in differ_files:
        first=d_file.split('/')[0]
        add_to_set=True
        for i in ignore:
            if i in first:
                add_to_set=False
                break
        if add_to_set:
            differing_files.append(d_file.strip())

    count=0
    files_to_use=[]
    for d_file in differing_files:
        cmd=("git", "diff", "master", "upstream-openwrt-19.07.4", "--", d_file.strip())

        ps = subprocess.check_output(cmd).strip()

        if len(ps) != 0:
            files_to_use.append(d_file.strip())

    for f in files_to_use:
        print f
    commits=open("git_log_all_all")

    commits_to_use=[]
    for l in commits:
        commit = l.split(' ')[0]

        cmd=("git", "diff-tree", "--no-commit-id", "--name-only", "-r",  commit)
    
        ps = subprocess.check_output(cmd).strip()

        if len(ps) > 0:
            for file_name in ps.split('\n'):
                if file_name in files_to_use:
                    if l.strip() not in commits_to_use:
                        commits_to_use.append(l.strip())

    #for s in commits_to_use:
        #print s
        #print s.split(' ')[0]
    #print len(commits_to_use)

            


