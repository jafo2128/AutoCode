#!/usr/bin/python3.4
import serial
from tkinter import *
from tkinter import messagebox

# This function creates a serial connection with the Elm 327 chip
# A 03 command is sent to the Elm 327 chip to request codes
def pull_codes():
    try:
        ser = serial.Serial('/dev/ttyUSB0', 38400,timeout = 1)
        ser.write(('03 \r\n').encode('utf-8'))
        line = ser.readline()
        text_line = line.decode("utf-8")
        num = 0
        short = ""
        all_codes = [""] * 6
        tcode = ""
        
        # NO DATA or padded 00's will be returned if there are no codes
        # If there are codes the code line will start with 43.  The codes
        # will begin 3 spaces after code 43
        # The else section will shorten the string to only codes and remove spaces
        # The section will also determine the number of code loops to perform
        if "NO DATA" in text_line or "00 00 00 00 00" in text_line:
            Label(root, text = "                                \n                                    \n                                     ").grid(row = 0,
            column = 1)
            Label(root, text= "No Codes").grid(row = 0, column = 1,pady = 10, padx = 10)
        else:
            index = text_line.index("43")
            index +=3
            while index < len(text_line):
                short = short + str(text_line[index])
                index += 1
            stripped_string = short.replace(" ", "")
            if (len(stripped_string)/4 < 3):
                codes = 2
            elif (len(stripped_string)/4 >= 3 and len(stripped_string)/4 < 4):
                codes = 3
            elif (len(stripped_string)/4 >= 4 and len(stripped_string)/4 < 5):
                codes = 4
            elif (len(stripped_string)/4 >= 5 and len(stripped_string)/4 < 6):
                codes = 5
            else:  
                codes = 6
                
            n = 0      # sets n to 0
            x = 0      # sets x to 0
            while num < codes and n < (len(stripped_string) - 4):
                tcode = ""
                for x in range(4):
                    tcode = tcode + stripped_string[n]
                    n += 1
                    all_codes[num] = tcode
                x = 0   # x must be reset to 0 before the for loop iterates again
                num += 1
            num = 0       # sets num to 0
            y = 0	  # sets y to 0
            display_code = ""

            # These lines add the Powertrain, Chassis, Body, and Network code identifiers to the code.
            while y < codes:
                change_code = all_codes[y]
                if change_code[0] == "3" or change_code[0] == "2" or change_code[0] == "1" or change_code[0] == "0":
                    display_code = "P" + change_code[0] + change_code[1] + change_code[2] + change_code[3]
                if change_code[0] == "4": 
                    display_code = "C" + "0" + change_code[1] + change_code[2] + change_code[3]
                if change_code[0] == "5":
                    display_code = "C" + "1" + change_code[1] + change_code[2] + change_code[3]
                if change_code[0] == "6":
                    display_code = "C" + "2" + change_code[1] + change_code[2] + change_code[3]
                if change_code[0] == "7":
                    display_code = "C" + "3" + change_code[1] + change_code[2] + change_code[3]
                if change_code[0] == "8":
                    display_code = "B" + "0" + change_code[1] + change_code[2] + change_code[3]
                if change_code[0] == "9":
                    display_code = "B" + "1" + change_code[1] + change_code[2] + change_code[3]
                if change_code[0] == "A":
                    display_code = "B" + "2" + change_code[1] + change_code[2] + change_code[3]
                if change_code[0] == "B":
                    display_code = "B" + "3" + change_code[1] + change_code[2] + change_code[3]
                if change_code[0] == "C":
                    display_code = "U" + "0" + change_code[1] + change_code[2] + change_code[3]
                if change_code[0] == "D":
                    display_code = "U" + "1" + change_code[1] + change_code[2] + change_code[3]
                if change_code[0] == "E":
                    display_code = "U" + "2" + change_code[1] + change_code[2] + change_code[3]
                if change_code[0] == "F":
                    display_code = "U" + "3" + change_code[1] + change_code[2] + change_code[3]
                    
                # These lines will block codes with all 0's from displaying    
                if display_code[1] == "0" and display_code[2] == "0" and display_code[3] == "0":
                    display_code = ""
                all_codes[y] = display_code
                y += 1

            # This line displays the codes        
            Label(root, text= all_codes[0] + " " + all_codes[1] + " " + all_codes[2] + "\n" + all_codes[3] + " " + all_codes[4] + " " +	all_codes[5]).grid(row = 0, column = 1,pady = 10, padx = 10)
                    
            ser.close()  # Close the serial connection
    except:
        # Display a check your connections and power statement if a connection is not made
        
        Label(root, text = "                                \n                                    \n                                  ").grid(row = 0,
            column = 1)

        Label(root, text = "Check connections\nTurn ignition on\nOr try a new port").grid(row = 0,
            column = 1)
           


# This function creates a connection with the Elm 327 device and sends the clear codes command (04)
# A check your connections and power statement will be displayed if an exception is thrown
def clear_codes():
    result = messagebox.askquestion(message="Are you sure?", icon="question", title="Clear Codes")
    if result == "yes":
        try:
            ser = serial.Serial('/dev/ttyUSB0', 38400,timeout = 1)
            ser.write(('04 \r\n').encode('utf-8'))
            Label(root, text = "                                \n                                    \n                                  ").grid(row = 1,
                column = 1)
            Label(root, text = "                                \n                                    \n                                  ").grid(row = 0,
                column = 1)
            Label(root, text = "Codes cleared").grid(row = 1,
                column = 1)
            Label(root, text= "No Codes").grid(row = 0, column = 1,pady = 10, padx = 10)
        except:
            Label(root, text = "Check connections\nTurn ignition on\nOr try a new port").grid(row = 1,
                column = 1)
    if result == "no":
        messagebox.showinfo(title="Clear Codes", message = "Canceled")

def about():
    messagebox.showinfo(message="Auto Code\rVersion 1.0\rAuthor: Lauren Rood\r\rUse with ELM327 USB Interface",
        title="Auto Code")
    
# These lines build the graphics window, size it, and title it 
root = Tk()
root.geometry ("300x200")
root.resizable(width=FALSE, height=FALSE)
root.title("Auto Code")

v = StringVar()
connection = ""

# These lines create the buttons that call the pull_codes and clear_codes functions
Button(root, text="Pull Codes", command = pull_codes).grid(row = 0,
    column = 0, padx = 10, pady = 10)
Button(root, text="Clear Codes", command = clear_codes).grid(row = 1,
    column = 0, padx = 10, pady = 10)
Button(root, text="Information", command = about).grid(row = 2, column = 0, padx = 10, pady = 10)
mainloop()
