import os
import time

alternate1 = """
      __        __      _______        __      
     /""\      |" \    /"      \      /""\     
    /    \     ||  |  |:        |    /    \    
   /' /\  \    |:  |  |_____/   )   /' /\  \   
  //  __'  \   |.  |   //      /   //  __'  \  
 /   /  \\  \  /\  |\ |:  __   \  /   /  \\  \ 
(___/    \___)(__\_|_)|__|  \___)(___/    \___)
                                               
                                               """

a = """

 █████╗ 
██╔══██╗
███████║
██╔══██║
██║  ██║
╚═╝  ╚═╝
        
"""
ai = """

 █████╗ ██╗
██╔══██╗██║
███████║██║
██╔══██║██║
██║  ██║██║
╚═╝  ╚═╝╚═╝
           
"""
air = """

 █████╗ ██╗██████╗ 
██╔══██╗██║██╔══██╗
███████║██║██████╔╝
██╔══██║██║██╔══██╗
██║  ██║██║██║  ██║
╚═╝  ╚═╝╚═╝╚═╝  ╚═╝
                   
"""
aira = """

 █████╗ ██╗██████╗  █████╗ 
██╔══██╗██║██╔══██╗██╔══██╗
███████║██║██████╔╝███████║
██╔══██║██║██╔══██╗██╔══██║
██║  ██║██║██║  ██║██║  ██║
╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
                           
"""


def bootup():
    os.system("cls")
    print(a)
    time.sleep(0.5)
    os.system("cls")
    print(ai)
    time.sleep(0.5)
    os.system("cls")
    print(air)
    time.sleep(0.5)
    os.system("cls")
    print(aira)
