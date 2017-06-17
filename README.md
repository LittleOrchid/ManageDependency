# ManageDependency

## description
You can use this script to list the local dependencies, list the remote dependencies in jcenter, and download the specific dependency you needed
* Currently we only support one remote repository, that is [jcenter](http://jcenter.bintray.com/)
* You have installed python, pip, bash in your PC
* You have installed [BeautifulSoap](https://www.crummy.com/software/BeautifulSoup/#Download/), that is a html parser writing by python

## usage
~~~
Usage: ded [-h] [-l] [-r] jar
       -l : list all jars in local repositoy
       -r : list all jars in remote repository
       -h : manpage
       jar format is group:artifact:version[:classifer:extension]
~~~

## exampleb
### 1.List the archive be dependent on in local repository (~/.m2/repository) 
**cmd:** `ded -l com.squareup.okio:okio`

**result:**
~~~
com.squareup.okio :
	okio  :
		1.0.0
		1.10.0-SNAPSHOT
~~~

### 2. list the archive be dependent on from jcenter
**cmd:** `ded -r com.squareup.okio:okio`

**result:**
~~~
com.squareup.okio
	okio
		0.5.0
		0.6.0
		0.6.1
		0.7.0
		0.8.0
		0.9.0
		1.0.0-atlassian-1
		1.0.0-atlassian-2
		1.0.0
		1.0.1
		1.1.0
		1.10.0
		1.2.0
		1.3.0-atlassian-1
		1.3.0
		1.4.0
		1.5.0
		1.6.0
		1.7.0
		1.8.0
		1.9.0
~~~
