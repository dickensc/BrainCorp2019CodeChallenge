This project is a submission to the BrainCorp 2019 Code Challenge. The challenge is to parse the UNIX passwd and
group files and combine the data into a single json output.

To install the code, from the top directory, Dickens-Charles/ run the following command in a terminal:

python3 setup.py install

This will install the necessary dependencies, make the PasswordParser script executable, and add the script to PATH.
Then to run the code you can simply type the following command into a terminal.

PasswordParser

This will run the script with the default configuration, that is the paths to the passwd and group files are
/etc/passwd and /etc/group, respectively. This behavior can be changed by passing command line arguments to the script.
Typing the following command:

PasswordParser --help

Will give the available optional arguments for the script and their descriptions.

The default configurations of the program are defined in the top of the PasswordParser script and can be modified to
change the output if it desired.
