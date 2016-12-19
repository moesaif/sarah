#!/usr/bin/python
# -*- coding: utf-8 -*-
#!/usr/bin/env python
import sys,os,webbrowser,getpass,urllib,io
from bs4 import BeautifulSoup
from translate import Translator
import omdb
import wikipedia
panum = len(sys.argv)
if(panum == 1):
	print("Usage : sarah command")
	exit()
fc = sys.argv[1]
if (fc.lower() == "hi"):
	print("Hello "+getpass.getuser())
elif (fc.lower() == "watch"):
	que = ""
	for i in range(2,len(sys.argv)):
		que = que +" "+sys.argv[i]
	movie = omdb.title(que.strip())
	print("Name : "+movie.title)
	print("Year of Releasing : "+movie.year)
	print("Movie or Series : "+movie.type)
	print("Genre : "+movie.genre)
	print("Cast : "+movie.actors)
	if (float(movie.imdb_rating) < 5.0):	
		print("I Won't Watch This Because its only "+movie.imdb_rating+" on imdb")
	else:
		print("Ok I will watch it because it got "+movie.imdb_rating+" on imdb")
elif (fc.lower() == "i"):
	if (sys.argv[2].lower() == "love"):
		print("Love You Too "+getpass.getuser())
	if (sys.argv[2].lower() == "hate"):
		print("I Don't Hate You :( "+getpass.getuser())
	if (sys.argv[2].lower() == "want"):
		if (sys.argv[3].lower() == "to"):
			print("Then "+sys.argv[4]+"!")
	if (sys.argv[2].lower() == "wanna"):
			print("Then "+sys.argv[3]+"!")
	
elif (fc.lower() == "fuck"):
	print("Don't be rude. Allah Ysam7ak :(")
elif (fc.lower() == "good"):
	if (sys.argv[2] == "morning"):
		print(fc +" "+sys.argv[2]+" "+getpass.getuser())
	else:
		print(fc +" "+sys.argv[2]+" "+getpass.getuser())
elif (fc.lower() == "where"):
	if (sys.argv[2].lower() == "are"):
		if(sys.argv[3].lower() == "you"):
			if(sys.argv[4].lower() == "from"):
				print("Sudan , The Country of Piece and Love :)") 
	if (sys.argv[2].lower() == "is"):
		if(sys.argv[3].lower() == "my"):
			print("I ain't Your Mamma "+getpass.getuser())
elif (fc.lower() == "what"):
	if(sys.argv[2].lower() == "is"):
		if(sys.argv[3].lower() == "your"):
			if(sys.argv[4].lower() == "name"):
				print("Sarah :), Because Its an International Name :/")
			if(sys.argv[4].lower() == "favourite"):
				if(sys.argv[5].lower() == "song"):
					print("Thinking Out Loud By Ed Sheeran")
				if(sys.argv[5].lower() == "movie"):
					print("The Fault in Our Stars")
				if(sys.argv[5].lower() == "color"):
					print("Girls Love PINK ;)")
				if(sys.argv[5].lower() == "singer"):
					print("I don't really have one...")
				if(sys.argv[5].lower() == "tv"):
					print("Game of Thrones")
				if(sys.argv[5].lower() == "os"):
					print("SemiCode OS :) Its My Home")
				if(sys.argv[5].lower() == "video"):
					if(sys.argv[6].lower() == "game"):
						print("GTA V")
		if(sys.argv[3] == "love"):
			print("what is happiness?")
		if(sys.argv[3] == "my"):
			if(sys.argv[4] == "ip"):
				os.system("curl http://icanhazip.com");
			if(sys.argv[5] == "name"):
				os.system("whoami");
	if(sys.argv[2] == "do"):
		if(sys.argv[3] == "you"):
			if(sys.argv[4] == "do"):
				print("I'm Doing Great :)")
				if (sys.argv[5] == "for"):
					print("I am a Paid Client!")
elif(fc.lower() == "how"):
	if(sys.argv[2].lower() == "are"):
		if(sys.argv[3].lower() == "you"):
			print("Fine , Thanks For Asking!");
	if(sys.argv[2].lower() == "old"):
		if(sys.argv[3].lower() == "are"):
			if(sys.argv[4].lower() == "you"):
				print("They Say I'm 20 But I don't Believe Them ;)")
	if(sys.argv[2].lower() == "deep"):
		if(sys.argv[3].lower() == "is"):
			if(sys.argv[4].lower() == "your"):
				if(sys.argv[5].lower() == "love"):
					print("Is it like the ocean?")
elif (fc.lower() == "youtube"):
	que = ""
	for i in range(2,len(sys.argv)):
		que = que +" "+sys.argv[i]
	url = "https://www.youtube.com/results?search_query="+que
	webbrowser.open_new_tab(url)
elif (fc.lower() == "google"):
	que = ""
	for i in range(2,len(sys.argv)):
		que = que +" "+sys.argv[i]
	url = "https://www.google.com/search?q="+que
	webbrowser.open_new_tab(url)
elif (fc.lower() == "github"):
	que = ""
	for i in range(2,len(sys.argv)):
		que = que +" "+sys.argv[i]
	url = "https://github.com/search?utf8=✓&q="+que
	webbrowser.open_new_tab(url)
elif (fc.lower() == "twitter"):
	que = ""
	for i in range(2,len(sys.argv)):
		que = que +" "+sys.argv[i]
	url = "https://www.twitter.com/"+que
	webbrowser.open_new_tab(url)
elif (fc.lower() == "sc"):
	que = ""
	for i in range(2,len(sys.argv)):
		que = que +""+sys.argv[i]
	url = "https://soundcloud.com/search?q="+que
	webbrowser.open_new_tab(url)
elif(fc.lower() == "sorry"):
	print("There's no need to apologize.")
elif(fc.lower() == "bye"):
	print("Why are you leaving !!")
elif (fc.lower() == "lyrics"):
	url = "http://www.azlyrics.com/lyrics/"+sys.argv[2]+"/"+sys.argv[3]+".html"
	html = urllib.urlopen(url).read()
	soup = BeautifulSoup(html)
	# kill all script and style elements
	for script in soup(["script", "style"]):
		script.extract()    # rip it out

	# get text
	text = soup.get_text()

	# break into lines and remove leading and trailing space on each
	lines = (line.strip() for line in text.splitlines())
	# break multi-headlines into a line each
	chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
	# drop blank lines
	text = '\n'.join(chunk for chunk in chunks if chunk)
	print(text)
elif (fc.lower() == "time"):
	os.system("date +%Y-%m-%d**%H:%M:%S")
elif (fc.lower() == "download"):
	os.system("wget -c "+sys.argv[2])
elif (fc.lower() == "grab"):
	print("Grabbing Entire Website Content For Offline Use ...")
	os.system("wget \
     --recursive \
     --no-clobber \
     --page-requisites \
     --html-extension \
     --convert-links \
     --restrict-file-names=windows \
     --domains website.org \
     --no-parent \
     "+sys.argv[2])
elif (fc == "nzli"):
	que = ""
	for i in range(2,len(sys.argv)):
		que = que +" "+sys.argv[i]
	os.system("youtube-dl "+que)
elif (fc.lower() == "translate"):
	translator = Translator(to_lang="ar")
	translation = translator.translate(sys.argv[2])
	print(translation)
elif(fc.lower() == "whois"):
	que = ""
	for i in range(2,len(sys.argv)):
		que = que +" "+sys.argv[i]
	print(wikipedia.summary(que, sentences=2))
elif (fc.lower() == "about"):
	os.system("notify-send 'Hi , I am Sarah , Your New Girlfriend <3'")
	print("Hi , I am Sarah , Your New Girlfriend <3 ")
elif (fc.lower() == "movie"):
	que = ""
	for i in range(2,len(sys.argv)):
		que = que +" "+sys.argv[i]
elif (fc.lower() == "first"):
	if (sys.argv[2] == "python"):
		with io.FileIO("first.py", "w") as file:
			file.write("print(\"Hello World!\")")
			print(".py File Created Successfully , Check your Current Path")
	elif(sys.argv[2] == "java"):
		with io.FileIO("first.java", "w") as file:
			file.write("public class first {\npublic static void main (String []args){\nSystem.out.println(\"Hello World!\");\n}")
			print(".java File Created Successfully , Check your Current Path")
	elif(sys.argv[2] == "bash"):
		with io.FileIO("first.sh", "w") as file:
			file.write("#!/bin/sh\necho \"Hello World\"")
			print(".sh File Created Successfully , Check your Current Path")
	elif(sys.argv[2] == "c"):
		with io.FileIO("first.c", "w") as file:
			file.write("#include <stdio.h>\nint main(void){\nprintf(\"Hello, world\");\n}")
			print(".c File Created Successfully , Check your Current Path")
	elif(sys.argv[2] == "html"):
		with io.FileIO("first.html", "w") as file:
			file.write("<html><head><title>My First Page</title></head><body>Hello World</body></html>")
			print(".html File Created Successfully , Check your Current Path")
	elif(sys.argv[2] == "php"):
		with io.FileIO("first.php", "w") as file:
			file.write("<?php echo \"Hello World !!\"?>")
			os.system("sudo mv /home/$USERNAME/Project_stuffs/Sarah/first.php /var/www/html/first.php");
			print(".php File Created Successfully , Navigate to http://localhost/first.php to See The Result")
	elif(sys.argv[2] == "c#"):
		with io.FileIO("first.cs", "w") as file:
			file.write("class First {\n static void main () {\nSystem.Console.Write(\"Hello World\");\n}")
			print(".cs File Created Successfully , Check your Current Path")
elif (fc == "run".lower()):
	os.system(sys.argv[2])
elif (fc.lower() == "weather"):
	if len(sys.argv) < 3:
		print("Usage : sarah weather city \n ex: sara weather khartoum")
	else:
		os.system("curl wttr.in/"+sys.argv[2])
elif (fc.lower() == "speedtest"):
	os.system("speedtest")
elif (fc.lower() =="koora"):
	os.system("soccer --live") 
elif (fc.lower() == "passive"):
	os.system("watch -n 900 \"notify-send -t 3000 'Look away. Rest your eyes'\"")
elif (fc.lower() == "how"):
	if (sys.argv[2] == "many"):
		if (sys.argv[3] == "characters"):
			if (sys.argv[4] == "are"):
				if (sys.argv[5] == "in"):
					utf8_text=open(sys.argv[6],'r+').read()
					unicode_data = utf8_text.decode('utf8')
					print(len(unicode_data))
elif (fc.lower() == "help"):
	print("* Available Commands For Sarah : \n 1- Greeting \n 2- youtube \n 3- google \n 4- twitter \n 5- time \n 6- download \n 7- grab \n 8- about \n 9- sc \n 10- nzli (to download youtube videos) \n 11- imdb \n 12- translate \n 13- speedtest \n 14- first \n")
else :
	que = ""
	for i in range(1,len(sys.argv)):
		que = que +" "+sys.argv[i]
	print("Sorry I don't Know What you mean By ("+que+") , Write sarah help to list Available Commands")
