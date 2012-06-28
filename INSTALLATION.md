The first thing you will want to do is follow the instructions on this wiki page: http://reporterslab.wikispaces.com/Setting+Up+Your+Mac. It is all about setting up a mac for development. If you have a PC you won't be able to follow these instructions.

I recommend downloading and installing XCode first. Many of the pieces of software won't compile properly. Once you've downloaded and installed it, open it and go to: XCode > Preferences > Downloads and install the "Command Line Tools." This is a very important step.

Then follow the rest of the wiki instructions, optionally doing the Hello Newsroom tutorial from the Chicago Tribune at the end.

There are a couple of steps you can probably ignore in the Setting Up Your Mac wiki. If you have OSX Lion you will not need to update your Python version. You may not have to add the ARCHFLAGS stuff either. It may be best to try without that first, and if things fail, add that back.

In all cases you should follow the instructions closely so you don't miss anything.

Also, you should install Mercurial (a source repository manager like git) because one of the packages the Video Notebook uses comes from a Mercurial repository (I tried getting it to install via the requirements in the Video Notebook project, but it kept erroring out. Putting it system-wide seemed to work).

from anywhere:

```bash
$ easy_install mercurial
```

(It's possible that you'll encounter an error trying to install mercurial because the installer can't properly locate your C compiler. This happened on my MacBook that I had upgraded to Lion myself. One way to fix that issue is to link the compiler to where the installer expects it to be. This can be done like so:

```bash
$ sudo ln -s /usr/bin/gcc /usr/bin/gcc-4.2
$ sudo ln -s /usr/bin/g++ /usr/bin/g++-4.2 
```
)

---

from here you will either want to create a Fork in github of the Video Notebook repository. The URL to clone from is located on the github page towards the top next to "SSH." To copy straight from the Reporters' Lab account you would do something like this (note that if you want to deploy to a server and not just run locally, you should make a fork first):


```bash
$ git clone git@github.com:ReportersLab/VideoNotebook.git
```

That will copy the code into a directory called VideoNotebook within whatever directory you ran the command (I recommend running that from inside a development folder you have made on your machine).

Your next step will be to create a virtual environment to keep all of the software nicely isolated.

```bash
$ mkvirtualenv VideoNotebook
$ easy_install pip
$ pip install -r requirements.txt
```

The mkvirtualenv command will create and activate the virtual environment. The next line installs pip into the virtual environment (it is used for installing software). And finally you use pip to install all of the requirements for the project (this will take some time). In the future to activate the virtual environment you would do

```bash
$ workon VideoNotebook
```

and to quit you would do

```bash
$ deactivate VideoNotebook
```

pip will install all of the requirements for the project into your virtual environment and you'll be ready to begin.

Now that everything is installed you can initialize the database and start the Django development server (remember that you should be doing all of this inside of your virtual environment, which is indicated by (Virtual_Env_Name) near your command line prompt):

```bash
$ fab bootstrap
$ ./manage migrate tastypie
$ ./manage migrate core
$ ./manage runserver
```

At this point the development server should be up and running on your computer. You'll see this message:

```bash
Django version 1.3.1, using settings 'common.settings'
Development server is running at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

so you can go to http://127.0.0.1:8000/ to view the site. or hit Control+C to quit the server (or close your terminal window).

You cannot log into the site wihtout a user name and password. You can create them in the commandline like so:


```bash
$ ./manage createsuperuser
```

you'll be prompted to put in a username, e-mail address, and password. 

You can now log in and access the site. You can also view the admin site at http://127.0.0.1:8000/admin/ 

You should now have full access to The Video Notebook on a local machine. Note, however, that the Twitter import and the S3 Upload will NOT work until you provide keys for it.

There are placeholders for the information you need in the /videotext/configs/common/settings.py file towards the bottom.

To create your Twitter keys, go here to create a new Twitter application: https://dev.twitter.com/apps/new

Creating the application will provide you with the proper Consumer keys and secrets. From your application's page you can scroll to the bottom to generate the appropriate Access Key and Secret. These can all be put in the appropriate settings. We keep them in a settings_private.py in the config folders and import them into our settings.py

Your EC2 keys will be created if you decide you want to deploy the application to a server.

---

If you want to deploy to a server you should have created a Fork of the repository from above, because you have to make some changes.

The next step should be to follow this wiki entry to set up EC2: http://reporterslab.wikispaces.com/Setting+Up+EC2. It should walk you through setting up an EC2 account, downloading some private keys to launch EC2 instances, and using https://github.com/newsapps/cloud-commander to launch a server. You can pretty much follow these exactly, just change the "hello_world" environment to whatever you named your virtual environment in the previous step (probably VideoNotebook). You will not have to install GRASS.

Once the server is up and running and the Wiki directs you to follow the hello newsroom deployment instructions, come back here.


In the base configuration at the top you will want to change the repository_url if you have made a fork of the VideoNotebook project.

```python
env.repository_url = '' #originally 'https://MrMetlHed@github.com/ReportersLab/VideoNotebook.git'
```


you'll also want to modify the 'staging' information (about line 37) to replace the reporterslab.org domains with the domains cloud commander generated. The bucket you create in S3 and should be something like 'media.yourdomain.com' or something similar.

```python
	env.hosts = ['your-ec2-instance-dns-name.amazonaws.com']   #originally: ['beta.reporterslab.org'] 
    env.s3_bucket = 'your-bucket-name'    #originally: 'media.reporterslab.org/beta'
```


You will next want to change the apache serevr settings to use your EC2 server dns name rather than the reporterslab.org domains. Change the ServerAlias 

```apache
ServerAlias your-ec2-instance-dns-name.amazonaws.com
```

You can also change the other mentions of reporterslab.org to your domains.

You should now be able to commit these changes to your fork to ready them for deployment:

```bash
$ git commit -am "edited the configuration files with our deployment details"
$ git push
```

and finally

```bash
$ fab staging master deploy
```

This will use Fabric to deploy to the 'staging' server using the 'master' branch of the github repository.

At this point you should be able to go to http://your-ec2-instance-dns-name.amazonaws.com and see the video notebook running on the server.

















