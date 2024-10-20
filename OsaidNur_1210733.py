# Name       : Osaid Hasan Nur
# ID         : 1210733
# Section    : 5
# Instructor : AbdelSalam Sayyad
# T.A        : Mazen Amria

# import the built in module to create xml manually
import xml.etree.ElementTree as ET

# import some important libraries
import subprocess,sys,os,shutil

# The main class in the project , it contains all operations (generate,verify,search,recommend)
class CommandManualGenerator :
    commands = []
    manuals=[]
    
    # This variable will determine the mode of this class , in other words, it 
    # selects the desired operation (generate,verify,search,recommend)
    option=0

########################################################################################
    # read the commands from the file commands.txt
    @staticmethod
    def readFile () :
        CommandManualGenerator.commands.clear()
        with open("commands.txt", "r") as file:  
            for line in file:
                CommandManualGenerator.commands.append(line.rstrip())

########################################################################################
    # Check if the commands sucessfuly added to the list commands or not
    @staticmethod
    def checkCommands():
        if len(CommandManualGenerator.commands) == 0 :
            print("ERROR when loading the commands, NO commands found !\n")
            sys.exit(1)

########################################################################################
    # Generate the the command manuals into xml file  
    @staticmethod
    def generate (fileName):
        
        #read the file commands.txt and check if the process is successful
        CommandManualGenerator.readFile()
        CommandManualGenerator.checkCommands()
        CommandManualGenerator.manuals.clear()
        
        # Generate a test file that contain 15 lines 
        with open("TEST_.txt", "w") as file:  
            for i in range(1, 16):  
                line = f"Line {i}\n"  
                file.write(line)  
        
        # Iterate over all commands loaded into the list "commands" to generate manuals 
        for command in CommandManualGenerator.commands:
            
            # Extract the description lines from the manual page of the command 
            desc = subprocess.run(["man", command], capture_output=True, text=True).stdout
            
            # Find the start index , when is the next line after DESCRIPTION
            start_index = desc.find("DESCRIPTION") + len("DESCRIPTION")
            
            # Find the end index , it's the first empty line after the description
            end_index = start_index + desc[start_index:].find("\n\n")
            
            # Extract the substring for the desired range
            description_ = desc[start_index:end_index]
            
            # Eliminate consecutive white spaces 
            description_ = description_.replace("  "," ")
            
            # get the version of the command if exists , and the Bash version if not
            if command == "which" or command == "pwd" :
                version_ = subprocess.check_output(['bash', '-c', 'echo $BASH_VERSION']).decode().strip()
            else:
                ver = subprocess.run([command, "--version"], capture_output=True, text=True).stdout.splitlines()[0]
                version_ = ver.split()[-1]
            
            # generate the examples for each command
            if command == "ls" :
                example_ = f">>$ {command}\n"
                # Execute the command and capture its output
                output = subprocess.run([command], capture_output=True, text=True).stdout
                # Append the command output to the example string
                example_ += output
        
            elif command == "touch":
                example_ = ">>$ ls\n"
                example_ += subprocess.run(["ls"], capture_output=True, text=True).stdout
                
                # create a new file for testing 
                example_ += ">>$ touch newfile.txt\n"
                subprocess.run(["touch", "newfile.txt"])  
                example_ += ">>$ ls\n"
                example_ += subprocess.run(["ls"], capture_output=True, text=True).stdout

                # Remove the temporary file
                subprocess.run(["rm", "newfile.txt"])

            elif command == "rm":
                example_ = ">>$ touch test_rm.txt\n"
                subprocess.run(["touch", "test_rm.txt"])
                example_ += ">>$ ls\n"
                example_ += subprocess.run(["ls"], capture_output=True, text=True).stdout
                example_ += ">>$ rm test_rm.txt\n"
                subprocess.run(["rm", "test_rm.txt"])
                example_ += ">>$ ls\n"
                example_ += subprocess.run(["ls"], capture_output=True, text=True).stdout

            elif command== "cat" or command == "head"  or command== "tail"  or \
                command== "more" or command== "less" or command == "wc" or command == "rev" :
                
                #apply these commands on the generated test file 
                example_ = f">>$ {command} TEST_.txt\n"  
                example_ +=subprocess.run([command, "TEST_.txt"], capture_output=True, text=True).stdout

            elif command== "mv":
                example_ = ">>$ touch oldName.txt\n"
                subprocess.run(["touch", "oldName.txt"])
                example_ += ">>$ ls\n"
                example_ += subprocess.run(["ls"], capture_output=True, text=True).stdout

                # give the test file another name, and test the result
                example_ += ">>$ mv oldName.txt newName.txt\n"
                subprocess.run(["mv", "oldName.txt", "newName.txt"])
                example_ += ">>$ ls\n"
                example_ += subprocess.run(["ls"], capture_output=True, text=True).stdout

                # Remove the temporary file
                subprocess.run(["rm", "newName.txt"])

            elif command== "which": 
                example_ = f">>$ which bash\n"  
                example_ += subprocess.run(["which", "bash"], capture_output=True, text=True).stdout

            elif command== "factor":
                example_ = f">>$ factor 250\n" 
                example_ += subprocess.run(["factor", "250"], capture_output=True, text=True).stdout

            elif command== "seq":
                example_ = f">>$ seq 0 5\n"  
                example_ += subprocess.run(["seq", "0", "5"], capture_output=True, text=True).stdout

            elif command== "uniq" :
                example = ">>$ touch before_uniq.txt\n"
                subprocess.run(["touch","before_uniq.txt"])
                
                # Fill the test file with a redundant elements 
                example += ">>$ echo -e \"1\\n2\\n2\\n2\\n3\\n3\\n4\\n5\\n5\\n5\" >> before_uniq.txt\n"
                with open("before_uniq.txt","a") as f:  
                    f.write("1\n2\n2\n2\n3\n3\n4\n5\n5\n5")

                # Display before_uniq.txt contents
                example += ">>$ cat before_uniq.txt\n"
                with open("before_uniq.txt","r") as f:
                    example += f.read()

                # Apply uniq and display after_uniq.txt contents
                example += "\n>>$ uniq before_uniq.txt after_uniq.txt\n"
                subprocess.run(["uniq", "before_uniq.txt", "after_uniq.txt"])
                example += ">>$ cat after_uniq.txt\n"
                with open("after_uniq.txt","r") as f:
                    example += f.read()

                # Remove temporary files
                subprocess.run(["rm", "before_uniq.txt"])
                subprocess.run(["rm", "after_uniq.txt"])

            else:
                example_ = f">>$ {command}\n"  
                example_ += subprocess.run([command], capture_output=True, text=True).stdout
            
            # Generate the related commands using compgen -c
            output = subprocess.check_output('compgen -c', shell=True, executable='/bin/bash')
            allCommands = output.decode() 
            related_ = subprocess.run(["grep", command], input=allCommands, capture_output=True, text=True).stdout  

            # Create an Object from the type CommandManual , and call it's constrctor
            # to assign the values to it
            myCommand = CommandManual(command,description_,version_,example_,related_)
            
            # Add the object to the list of manuals 
            CommandManualGenerator.manuals.append(myCommand)
        
        # Remove the test file     
        subprocess.run(["rm", "TEST_.txt"])
        
        # generate the xml file
        Xmlserializer.serialize(CommandManualGenerator.manuals,fileName)
        if fileName == "Commands" :
            print("  Xml file generated successfully ...")

########################################################################################
    # verify the generated manuals if they changed over time 
    @staticmethod
    def verify (): 
        # if the command manuals are not generated , it will not continue
        if not os.path.exists("Commands.xml"):
            print("The Manuals are not generated to verify them ,generate them and try again ! \n")
        
        # if the command manuals are already generated , we will go ahead
        elif not os.path.exists("Commands_TEST.xml"):
            
            # generate a test version of the command manuals to compare with the current file
            CommandManualGenerator.generate("Commands_TEST")
            
            # deserialize the two files that we want to compare , as a result of that , 
            # we will have two lists that have the pure data for each command manual ,
            # and this make the comparison process easier and more precise 
            list1 = Xmlserializer.deserialize("Commands.xml")
            list2 = Xmlserializer.deserialize("Commands_TEST.xml")
            
            # loop over the two lists , and compare every attribure for each commmand manual
            # and if there is a difference , it will display this difference clearly
            for i in range(0,20):
                if list1[i].getName() != list2[i].getName() :
                    print(f"The name for the command {list2[i].getName()} have been changed...")
                    print ("********** Before **********"+"\n"+list2[i].getName())
                    print ("********** After ***********"+"\n"+list1[i].getName())
                    print ("_______________________________________________________________________________________")

                if list1[i].getDescription() != list2[i].getDescription() :
                    print(f"The Description for the command {list2[i].getName()} have been changed...")
                    print ("********** Before **********"+"\n"+list2[i].getDescription())
                    print ("********** After ***********"+"\n"+list1[i].getDescription())
                    print ("_______________________________________________________________________________________")
                
                if list1[i].getVersion() != list2[i].getVersion() :
                    print(f"The Version for the command {list2[i].getName()} have been changed...")
                    print ("********** Before **********"+"\n"+list2[i].getVersion())
                    print ("********** After ***********"+"\n"+list1[i].getVersion())
                    print ("_______________________________________________________________________________________")
                
                if list1[i].getExample() != list2[i].getExample() :
                    print(f"The Example for the command {list2[i].getName()} have been changed...")
                    print ("********** Before **********"+"\n"+list2[i].getExample())
                    print ("********** After ***********"+"\n"+list1[i].getExample())
                    print ("_______________________________________________________________________________________")
                
                if list1[i].getRelatedCommands() != list2[i].getRelatedCommands() :
                    print(f"The Related Commands for the command {list2[i].getName()} have been changed...")
                    print ("********** Before ********** "+"\n"+list2[i].getRelatedCommands())
                    print ("********** After *********** "+"\n"+list1[i].getRelatedCommands())
                    print ("_______________________________________________________________________________________")
            
            # remove the test command manuals
            subprocess.run(["rm","Commands_TEST.xml"])
            
########################################################################################
    # search for a command or any word in the generated manuals
    @staticmethod
    def search ():
        found=1
        empty=1
        
        # take the command name from the user to search for
        word = input("Enter the command to search for : ")
        
        # if the commands manuals are not generated , it will generate them automatically
        if not os.path.exists("Commands.xml"):
            CommandManualGenerator.generate("Commands")
            found=0
        
        # convert the commands manuals files to a list that contains pure date for commands
        manuals = Xmlserializer.deserialize("Commands.xml")
        
        # loop through all list of manuals and search for the command name , and
        # if found , it will print all info about the command  
      
        for i in range (0,20):
            if word == manuals[i].getName():
                print("//////////////////////////////////////////////////////////////////////")
                print("// Command name     : "+ manuals[i].getName())
                print("// Description      : "+ manuals[i].getDescription())
                print("// Version          : "+ manuals[i].getVersion())
                print("// Example          : \n"+ manuals[i].getExample())
                print("// Related Commands : \n"+ manuals[i].getRelatedCommands())
                print("/////////////////////////////////////////////////////////////////////")
                empty=0
        
        # if the word was not found in any manual , it will print NONE
        if empty: 
            print(" The command was not found !")
       
        
        # if the commands manuals was not generated , it will remove the generated manuals
        # in this function , because maybe the user want to search without generating the 
        # file , this will allow it to perform search at any time 
        if not found :
            subprocess.run(["rm","Commands.xml"])
        
        # get the recommendation of this command name
        CommandManualGenerator.recommend(word)
        
########################################################################################    
    # get some recommendation commands depending on the word given
    @staticmethod
    def recommend (word):
        found=1
        
        #define some related commands depending on the functionality 
        recommendations = {
        "ls": ["dir", "ll", "tree", "find", "du"],
        "touch": ["create", "newfile", "echo", "truncate", "mkfile"],
        "mv": ["move", "rename", "cp", "link", "ln"],
        "rm": ["delete", "erase", "unlink", "purge", "shred"],
        "cat": ["view", "display", "more", "less", "bat"],
        "head": ["top", "peek", "head -n", "tail -n", "sed 1d"],
        "tail": ["end", "bottom", "tail -n", "tac", "more +n"],
        "more": ["less", "pager", "cat", "nl", "bat"],
        "less": ["more", "pager", "cat", "nl", "bat"],
        "wc": ["wordcount", "lines", "grep -c", "awk '{print NR}'"],
        "rev": ["reverse", "flip", "tac", "tr \\0 \\2 \\1"],
        "which": ["where", "locate", "path", "command -v", "type"],
        "factor": ["prime", "decompose", "gfactor", "primenumbers", "factor -h"],
        "seq": ["generate", "range", "for"],
        "uniq": ["unique", "duplicates", "sort -u"],
        "logname": ["username", "whoami", "id", "getent passwd $USER", "echo $LOGNAME"],
        "pwd": ["currentdir", "workingdir", "printwd", "realpath .", "echo $PWD"],
        "who": ["users", "loggedon", "w", "finger", "getent passwd"],
        "date": ["calendar", "time", "cal"],
        "ps": ["processes", "running", "top", "htop", "pgrep"],
        }
        
        # if the word given is one of the 20 supported command , it will display the 
        # related commands depending on functionality 
        if word in recommendations:
            print("Recommended Commands : ")
            for elem in recommendations[word]:
                print(" "+elem)
        
        # if the word given is a command other than our 20 commands, it will print 
        # all related commands depending on the name
        elif shutil.which(word) is not None:
            print("Recommended Commands : ")
            output = subprocess.check_output('compgen -c', shell=True, executable='/bin/bash')
            commands = output.decode()
            result = subprocess.run(["grep",f"{word}"],input=commands,text=True,capture_output=True).stdout
            print(result)
        
        #if the word given is not a command , it will search about the word in the 
        # generated manuals especially in the description part , and it will display 
        # the command name if it found the word in
        else:
            
            # if the commands manuals are not generated , it will generate them automatically
            if not os.path.exists("Commands.xml"):
                CommandManualGenerator.generate("Commands")
                found=0
            
            # convert the commands manuals files to a list that contains pure date for commands
            manuals = Xmlserializer.deserialize("Commands.xml")
            
            # loop through all list of manuals and search for the word in the description
            # for all generated command manuals ,if found , it will print the command name  
            print("Recommended Commands : ")
            for i in range (0,20):
                if word in manuals[i].getDescription():
                    print(" "+manuals[i].getName())
        
        # if the commands manuals was not generated , it will remove the generated manuals
        # in this function , because maybe the user want to get recommendation without 
        # generating the file , this will allow it to get recommendation at any time 
        if not found :
            subprocess.run(["rm","Commands.xml"])        

#****************************************************************************************
#****************************************************************************************
#****************************************************************************************

#this class is the main structure of the command manual
class CommandManual :
    # The main attributes for each command manual
    __Name=""
    __Description=""
    __Version=""
    __Example=""
    __RelatedCommands=""
    
    # the constructor
    def __init__(self,name,description,version,example,relatedCommands):
        self.__Name = name
        self.__Description = description
        self.__Version = version
        self.__Example = example
        self.__RelatedCommands = relatedCommands

    # the Getters
    def getName(self) :
        return self.__Name
    def getDescription(self) :
        return self.__Description
    def getVersion(self):
        return self.__Version
    def getExample(self):
        return self.__Example
    def getRelatedCommands(self):
        return self.__RelatedCommands
    
    #The setters
    def setName(self,name) :
        self.__Name = name
    def setDescription(self,description) :
        self.__Description = description
    def setVersion(self,version):
        self.__Version = version
    def setExample(self,example):
        self.__Example = example
    def setRelatedCommands(self,realtedCommands):
        self.__RelatedCommands = realtedCommands

#****************************************************************************************
#****************************************************************************************
#****************************************************************************************

# this class will convert the CommandManual object to an Xml file and the inverse
class Xmlserializer:
    
    # the following static methond is responsible for converting the commands 
    # manuals of type "CommandManual" class to a single XML file , the principle
    # of serialization is that we have a tree , that have a root and elements 
    # connected to , at the beginning of the function , i define the main root 
    # for all commands manuals , and iterate over every single manual and complete
    # this tree in each round until we have the full tree for the 20 commands 
    @staticmethod
    def serialize(manuals,fileName):
              
        # define the header of the main root for all commands manuals
        root =ET.Element("Manuals")
        
        for man in manuals:
            #define the header for the root of every single command 
            subRoot=ET.SubElement(root,"CommandManual")
            
            #define the sub elements for every command manual , containing 
            # the informations about this command, this elements will act as 
            # the leaves of the tree
            ET.SubElement(subRoot, "CommandName").text = man.getName()
            ET.SubElement(subRoot, "CommandDescription").text = man.getDescription()
            ET.SubElement(subRoot, "VersionHistory").text = man.getVersion()
            ET.SubElement(subRoot, "Example").text = man.getExample()
            ET.SubElement(subRoot, "RelatedCommands").text = man.getRelatedCommands()
 
        #the tree is completed , and we can write it to the xml file
        tree = ET.ElementTree(root)
        tree.write(f"{fileName}.xml")
    
    # the following static methond is the inverse of the previous method , it takes a
    # xml file , and extract data from it , and return the list of manual commands which
    # have the pure data 
    @staticmethod    
    def deserialize(xmlFile):
        manuals = []
        
        tree = ET.parse(xmlFile)
        root = tree.getroot()

        # Store the data of each single manual in a dictionary , then pass the data to 
        # an object of type CommandManual , and push this object to our list 
        for man in root.findall("CommandManual"):
            manual_data = {}
            for element in man:
                manual_data[element.tag] = element.text

            # Create a CommandManual object from the extracted data
            manual = CommandManual(
                name=manual_data["CommandName"],
                description=manual_data["CommandDescription"],
                version=manual_data["VersionHistory"],
                example=manual_data["Example"],
                relatedCommands=manual_data["RelatedCommands"]
            )
            manuals.append(manual)            
        return manuals

#****************************************************************************************
#****************************************************************************************
#****************************************************************************************

# The main class 
while True:
    print("* * * * * * * * * * * * * * *")
    print("*  Choose the option (1-5): *")
    print("*  1- generate              *")
    print("*  2- verify                *")
    print("*  3- search                *")
    print("*  4- recommend             *")
    print("*  5. Exit                  *")
    print("* * * * * * * * * * * * * * *")
    choice = input("||| choice -> " ) 
    choice = int (choice)
    if choice == 1:
        print("... You selected generate ...")
        CommandManualGenerator.generate("Commands")
        
    elif choice == 2:
        print("... You selected verify ...")
        CommandManualGenerator.verify()
   
    elif choice == 3:
        print("... You selected search ...")
        CommandManualGenerator.search()

    elif choice == 4:
        print("... You selected recommend ...")
        com = input("Enter a word or command name: ")
        CommandManualGenerator.recommend(com)

    elif choice == 5:
        print("Exiting...")
        break
    else :
        print("Invalid Input !\n")
        continue
