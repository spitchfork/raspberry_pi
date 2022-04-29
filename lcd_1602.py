##############################################
# Author: Stephen Pitchfork
# Email: s.pitchfork@googlemail.com
# Licence: MIT
##############################################

import RPi.GPIO as GPIO
import time

# LCD to GPIO mapping
LCD_RS = 7 # GPIO 7
LCD_E = 8 # GPIO 8
LCD_D4 = 25 # GPIO 25
LCD_D5 = 24 # GPIO 24
LCD_D6 = 23 # GPIO 23
LCD_D7 = 18 # GPIO 18

# Device constants
INSTR_FUNCTION_SET = 0x28 # 4 bit mode, 2 line display - 0 0 1 0 1 0 0 0
INSTR_DISP_CTRL_DISP_OFF = 0x08
INSTR_DISP_CTRL_DISP_ON_CRSR_OFF_NO_BLK = 0x0C # display on, cursor off, cursor blink off
INSTR_DISP_CTRL_DISP_ON_CRSR_ON_BLK = 0x0F
INSTR_GO_UPPER_LEFT = 0x80 # move cursor to upper left
INSTR_GO_LOWER_LEFT = 0xC0 # move cursor to lower left
INSTR_ENTRY_MODE_SET = 0x06 #cursor position increment
INSTR_CLEAR_DISPLAY = 0x01 # self explanatory
INSTR_CURSOR_HOME = 0x02

class Lcd:

 def display_line_one(self, text):
  self.__write_instruction(INSTR_GO_UPPER_LEFT)
  self.__write_text(text)

 def display_line_two(self, text):
  self.__write_instruction(INSTR_GO_LOWER_LEFT)
  self.__write_text(text)

 def __write_instruction(self, instruction):
  self.__lcd_write(instruction, False)

 def __write_text(self, text):
  for i in range(len(text)):
   self.__lcd_write(ord(text[i]), True)

 def __lcd_write(self, bits, mode):
  # High bits
  GPIO.output(LCD_RS, mode) # RS
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
   GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
   GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
   GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
   GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  self.__lcd_toggle_enable()

  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
   GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
   GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
   GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
   GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  self.__lcd_toggle_enable()

 def __lcd_toggle_enable(self):
  time.sleep(0.01)
  GPIO.output(LCD_E, True)
  time.sleep(0.01)
  GPIO.output(LCD_E, False)
  time.sleep(0.01)

 def run_diagnostics(self):
  print("Running LCD Diagnostics..")
  print("Check the LCD output to observe instruction changes.")
  
  print("Check Function Set..")
  time.sleep(1)
  self.__write_instruction(INSTR_FUNCTION_SET)
  time.sleep(3)

  print("Check Clear Display..")
  time.sleep(1)
  self.__write_instruction(INSTR_CLEAR_DISPLAY)
  time.sleep(3)

  print("Check Cursor Home..")
  time.sleep(1)
  self.__write_instruction(INSTR_CURSOR_HOME)
  time.sleep(3)

  print("Check Cursor Blink..")
  time.sleep(1)
  self.__write_instruction(INSTR_DISP_CTRL_DISP_ON_CRSR_ON_BLK)
  time.sleep(3)

  print("Check Entry Mode Set..")
  time.sleep(1)
  self.__write_instruction(INSTR_ENTRY_MODE_SET)
  time.sleep(3)

  print("Check Hello World write..")
  time.sleep(1)
  self.display_line_one("Hello")
  self.display_line_two("World!")
  time.sleep(3)

 def __init__(self):
  # set up Rpi GPIO
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM) # Use BCM GPIO numbers
  GPIO.setup(LCD_E, GPIO.OUT) # Set GPIO's to output mode
  GPIO.setup(LCD_RS, GPIO.OUT)
  GPIO.setup(LCD_D4, GPIO.OUT)
  GPIO.setup(LCD_D5, GPIO.OUT)
  GPIO.setup(LCD_D6, GPIO.OUT)
  GPIO.setup(LCD_D7, GPIO.OUT)

  # set up LCD
  self.__write_instruction(INSTR_FUNCTION_SET)
  self.__write_instruction(INSTR_CLEAR_DISPLAY)
  self.__write_instruction(INSTR_CURSOR_HOME)
  self.__write_instruction(INSTR_DISP_CTRL_DISP_ON_CRSR_ON_BLK)
  self.__write_instruction(INSTR_ENTRY_MODE_SET)

  time.sleep(0.0005) # Delay to allow commands to process

 def __del__(self):
  GPIO.cleanup()

def test():
 lcd = Lcd()
 lcd.run_diagnostics()
 time.sleep(5)

if __name__ == "__main__":
 test()
 GPIO.cleanup()
