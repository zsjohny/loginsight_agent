**How to install loginsight agent**
===========


----------



**1. Please make sure you already installed pip is well**
---------------------------------------------------------

 


----------


 - **You can install from official**
   https://pip.pypa.io/en/stable/installing/
 - **Install pip on CentOS / RHEL**
 **Install epel:**
 > **For RHEL 7.x and CentOS 7.x (x86_64)**

		 yum install epel-release

 > **For RHEL 6.x and CentOS 6.x (x86_64)**

		rpm -ivh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm

 > **For RHEL 6.x and CentOS 6.x (i386)**

		rpm -ivh http://dl.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm
                     
	**Installing pip with yum command:**

			yum install -y python-pip

 - **Install pip on ubuntu** 

		sudo apt-get update
		sudo apt-get install pip -y

**2. Installing package with pip command**
----------------------


----------


		pip install jinja2
		pip install requests

**3. Run scripts**
------------------


----------
		cd loginsight_agent
		python loginsight_agent.py
		
**Simple install by shell on wiki**		
