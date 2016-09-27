# ManageDependency
You can use this script to list the local dependencies, list the remote dependencies in jcenter, and download the specific dependency you needed

Usage: ded [-h] [-l] [-r] [-d] jar
       -l : list all jars in local repositoy
       -r : list all jars in remote repository
       -d : download jar from remote, and format likes group:artfact:version:classifer:extension
       -h : manpage
       jar format is group:artifact:version[:classifer:extension]
