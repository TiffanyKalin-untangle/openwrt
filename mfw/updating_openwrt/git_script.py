#!/bin/python
import subprocess 
import sys
import getopt 

#Files to ignore 
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

#Function for determine cherry pick commits for us_only commits and all commits we've committed
#@param print_total_counts - print total commits found
#@param print_all_info_to_file - print commit, author, subject of found commits to a file 
#@param print_commits_to_file - print commit to file 
#@param doing_committers - cherry pick commits from all commits we've committed 
#@param print_files_we_modified - print the files we have modified 
def do_commits(print_total_counts, print_all_info_to_file, print_commits_to_file, doing_committers, print_files_we_modified):
    #file names for us_only
    doing_commits_file='git_log_us_only'
    print_all_info_file='commits_to_cherry_pick_us_only_all'
    print_commits_file='commits_to_cherry_pick_us_only'

    #Change file names for committer situation 
    if doing_committers:
        doing_commits_file='git_log_committers'
        print_all_info_file='commits_to_cherry_pick_committers_all'
        print_commits_file='commits_to_cherry_pick_committers'

    #open git_log file 
    commits=open(doing_commits_file)
    thisset = set()

    print_all_info=''
    print_commits=''

    total_count=0
    for l in commits:
        #determine commit and subject from line 
        commit = l.split(' ')[0]
        subject = l.split(':')[1].strip()

        #get changed files from commit
        cmd=("git", "diff-tree", "--no-commit-id", "--name-only", "-r",  commit)
    
        ps = subprocess.check_output(cmd).strip()

        added_to_set=False
        # if files exist, determine if those files are in the ignore variable 
        if len(ps) > 0:
            for file_name in ps.split('\n'):
                add_to_set=True
                first=file_name.split('/')[0]
                #loop through ignore to determine if this file is added to set 
                for i in ignore:
                    if i in first:
                       add_to_set=False
                       break
                #Add to set 
                if add_to_set:
                        thisset.add(file_name)
                        added_to_set=True
        #if a file was added to the set, then save the commit information 
        if added_to_set:
            total_count=total_count+1
            if print_all_info_to_file:
                print_all_info += l.strip()
                print_all_info += '\n'
            if print_commits_to_file:
                print_commits += commit
                print_commits += '\n'

    commits.close()

    #print out information we desire 
    if print_files_we_modified:
        sortedset=sorted(thisset)
        files_we_modified=open('files_we_modified', 'w')
        files_we_modified_str=''
        for s in sortedset:
            files_we_modified_str+=s
            files_we_modified_str+='\n'
        files_we_modified.write(files_we_modified_str.strip())
        files_we_modified.close()
    if print_total_counts:
        print total_count
    if print_all_info_to_file:
        print_all_info_file_write = open(print_all_info_file, 'w')
        print_all_info_file_write.write(print_all_info.strip())
        print_all_info_file_write.close()
    if print_commits_to_file:
        print_commits_write=open(print_commits_file, 'w')
        print_commits_write.write(print_commits.strip())
        print_commits_write.close()

#print out commits to cherry_pick based on differing_files
#@param print_total_counts - print total commits found 
#@param print_all_info_to_file - print commit, author, subject to file 
#@param print_commits_to_file - print commit to file 
def do_differing_files(print_total_counts, print_all_info_to_file, print_commits_to_file): 
    #Determine files that are different  
    differ_files=open("differing_files")
    differing_files=[]

    #ONly include files that are not in the ignore variable
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
    #determine files to use from differing_files 
    for d_file in differing_files:
        #determine if file is different from 19.07.4 branch 
        cmd=("git", "diff", "master", "upstream-openwrt-19.07.4", "--", d_file.strip())

        ps = subprocess.check_output(cmd).strip()

        #if file is different from 19, then save it in files_to_use
        if len(ps) != 0:
            files_to_use.append(d_file.strip())

    #Print this for debugging purposes
    #for f in files_to_use:
    #    print f
    commits=open("git_log")

    commits_to_use=[]
    #determine commits to cherry pick 
    for l in commits:
        commit = l.split(' ')[0]

        #get files modified by commit
        cmd=("git", "diff-tree", "--no-commit-id", "--name-only", "-r",  commit)
    
        ps = subprocess.check_output(cmd).strip()

        #if files exist, determine if the file seen is a file we want to track commits for
        if len(ps) > 0:
            for file_name in ps.split('\n'):
                if file_name in files_to_use:
                    #make sure don't add same commit more than once to array
                    if l.strip() not in commits_to_use:
                        commits_to_use.append(l.strip())

    #collect and print information we desire
    commits.close()
    print_all_info_str=''
    print_commits_str=''
    for s in commits_to_use:
        print_all_info_str+=s
        print_all_info_str+='\n'
        print_commits_str=s.split(' ')[0]
        print_commits_str+='\n'
    if print_total_counts:
        print len(commits_to_use)
    if print_all_info_to_file:
        print_all_info_file_write = open('commits_to_cherry_pick_all', 'w')
        print_all_info_file_write.write(print_all_info_str.strip())
        print_all_info_file_write.close()
    if print_commits_to_file:
        print_commits_write=open('commits_to_cherry_pick', 'w')
        print_commits_write.write(print_commits_str.strip())
        print_commits_write.close()

#main function
#@param argv - command line arguments
def main(argv):
    #various booleans 
    doing_commits=False
    use_differing_files=False
    doing_committers=False
    print_total_counts=False
    print_all_info_to_file=False
    print_commits=False
    print_files_we_modified=False

    #read args 
    try:
        opts, args = getopt.getopt(argv, "hudaticf")
    except getopt.GetoptError:
        print 'bad arg'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            sys.exit()
        #For is doing_commits function 
        elif opt == '-u':
            doing_commits = True
        #For if doing differing_files function 
        elif opt == '-d':
            use_differing_files = True
        #For if using all committers in doing_commits function 
        elif opt == '-a':
            doing_committers=True
        #For if print total counts in both functions 
        elif opt == '-t':
            print_total_counts=True
        #For if printing commit, author, subject to file in both functions 
        elif opt == '-i':
            print_all_info_to_file=True
        #For if print commit to file for both functions 
        elif opt == '-c':
            print_commits=True
        #For if print files we have modifed in doing_commits function 
        elif opt == '-f':
            print_files_we_modified=True

    #Run functions if we desire 
    if doing_commits:
        do_commits(print_total_counts, print_all_info_to_file, print_commits, doing_committers, print_files_we_modified)
    if use_differing_files:
        do_differing_files(print_total_counts, print_all_info_to_file, print_commits)

#Main
if __name__ == "__main__":
    main(sys.argv[1:])


