from defs import config

def print_debug(message, newline = True):
     # If "end" = "" it does not create a newline

     if(config["dev"]["debug"]):
          end = "\n"
          if newline != True:
               end = ""

          print(message, end)