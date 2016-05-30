#!/usr/bin/env python

import sys
import os
import gi
import pygtk
import pyaudio 
import wave 
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst, Gtk, Gdk
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
GObject.threads_init()
Gdk.threads_init()

Gst.init(None)

class DemoApp(object):
    """Voice Command Recognition System"""
    def __init__(self):
        """Initialize a DemoApp object"""
        self.init_gui()
        self.init_gst()

    def callback(self, widget, data=None):
        print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active])

    def button_toggle(self, widget): 
        if widget.get_active():return Gtk.RadioButton.get_name(widget) 

    def init_gui(self):
        """Initialize the GUI components"""
        self.window = Gtk.Window()
        self.window.set_title("Voice Command Recognizer")
        self.window.set_position(Gtk.WindowPosition.CENTER)

        self.window.connect("destroy", self.quit)
        self.window.set_default_size(400,200)
        self.window.set_border_width(10)
        vbox = Gtk.VBox()

        box1 = Gtk.HBox(False, 10)
        box1.set_border_width(10)
        vbox.pack_start(box1, True, True, 0)
        box1.show()

        self.button_live = Gtk.RadioButton.new_with_label_from_widget(None, label="Live Mode (your microphone)")
        self.button_live.connect("toggled", self.callback, "live")
        self.button_live.set_active(True)
        box1.pack_start(self.button_live, True, True, 0)
        self.button_live.show()
   
        self.button_pre = Gtk.RadioButton.new_with_label_from_widget(self.button_live, label="Experiments (pre-recorded audio)")
        self.button_pre.connect("toggled", self.callback, "pre")
        box1.pack_start(self.button_pre, True, True, 5)
        self.button_pre.show()  
       
        separator = Gtk.HSeparator()
        vbox.pack_start(separator, False, False, 0)
        separator.show() 

        self.label = Gtk.Label("Please choose one model:")
        vbox.pack_start(self.label, True, True, 1)

        box2 = Gtk.HBox(False, 10)
        box2.set_border_width(10)
        vbox.pack_start(box2, True, True, 0)
        box2.show()

        self.button_gmm = Gtk.RadioButton.new_with_label_from_widget(None, label="Mode 1 (GMM)")
        self.button_gmm.connect("toggled", self.callback, "GMM")
        self.button_gmm.set_active(True)
        box2.pack_start(self.button_gmm, True, True, 0)
        self.button_gmm.show()
   
        self.button_dnn = Gtk.RadioButton.new_with_label_from_widget(self.button_gmm, label="Mode 2 (DNN)")
        self.button_dnn.connect("toggled", self.callback, "DNN")
        box2.pack_start(self.button_dnn, True, True, 0)
        self.button_dnn.show()  

        separator = Gtk.HSeparator()
        vbox.pack_start(separator, False, False, 0)
        separator.show()   
        box2 = Gtk.VBox(False, 10)
        box2.set_border_width(10)
        vbox.pack_start(box2, True, True, 0)
        box2.show() 
  
        self.label = Gtk.Label("Your command is displayed below:")
        vbox.pack_start(self.label, True, True, 1)

        self.text = Gtk.TextView()
        self.text.set_size_request(-1, 200)
        self.textbuf = self.text.get_buffer()
        self.text.set_wrap_mode(Gtk.WrapMode.WORD)
        vbox.pack_start(self.text, True, True, 1)

        separator = Gtk.HSeparator()
        vbox.pack_start(separator, False, False, 0)
        separator.show()   
        hbox = Gtk.HBox(spacing=10)
        hbox.show()
        vbox.pack_start(hbox, True, False, 0)

        self.image = Gtk.Image()
        self.image.set_from_file("/home/anastasia/Downloads/speak.jpg")
        self.image.show()
        self.button1 = Gtk.Button()
        self.button1.add(self.image)
        self.button1.set_size_request(100,100) 
        self.button1.show()
        self.button1.connect('clicked', self.button1_clicked,"1")
        hbox.pack_start(self.button1, False, False, 67)

        self.image = Gtk.Image()
        self.image.set_from_file("/home/anastasia/Downloads/stop.png")
        self.image.show()
        self.button2 = Gtk.Button()
        self.button2.add(self.image)
        self.button2.set_size_request(100,100) 
        self.button2.show()
        self.button2.connect('clicked', self.button2_clicked,"2")
        hbox.pack_start(self.button2, False, False, 13)
        vbox.pack_start(hbox, False, False, 5)
        #if self.button_toggle=='pre'
         #   button2.set_enabled(False)
        self.window.add(vbox)
        self.window.show_all()

        def record_audio(self):
            CHUNK = 1024 
            FORMAT = pyaudio.paInt16 
            CHANNELS = 2 
            RATE = 44100 
            RECORD_SECONDS = 4 
            WAVE_OUTPUT_FILENAME = "output.wav" 

            p = pyaudio.PyAudio() 

            stream = p.open(format=FORMAT, 
            channels=CHANNELS, 
            rate=RATE, 
            input=True, 
            frames_per_buffer=CHUNK) 

            frames = [] 

            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)): 
            data = stream.read(CHUNK) 
            frames.append(data)

            stream.stop_stream() 
            stream.close() 
            p.terminate() 

            wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb') 
            wf.setnchannels(CHANNELS) 
            wf.setsampwidth(p.get_sample_size(FORMAT)) 
            wf.setframerate(RATE) 
            wf.writeframes(b''.join(frames)) 
            wf.close()   

    def quit(self, window):
        Gtk.main_quit()

    def init_gst(self):
        #Initialize the speech components
        self.pulsesrc = Gst.ElementFactory.make("pulsesrc", "pulsesrc")
        if self.pulsesrc == None:
            print >> sys.stderr, "Error loading pulsesrc GST plugin. You probably need the gstreamer1.0-pulseaudio package"
            sys.exit()	
        self.audioconvert = Gst.ElementFactory.make("audioconvert", "audioconvert")
        self.audioresample = Gst.ElementFactory.make("audioresample", "audioresample")
        self.asr = Gst.ElementFactory.make("kaldinnet2onlinedecoder", "asr")
        self.fakesink = Gst.ElementFactory.make("fakesink", "fakesink")
        
        if self.asr:
          model_file = "final.mdl"
          if not os.path.isfile(model_file):
              print >> sys.stderr, "Models not downloaded? Run prepare-models.sh first!"
              sys.exit(1)
          self.asr.set_property("fst", "HCLG.fst")
          self.asr.set_property("model", "final.mdl")
          self.asr.set_property("word-syms", "words.txt")
          self.asr.set_property("feature-type", "mfcc")
          self.asr.set_property("mfcc-config", "conf/mfcc.conf")
          self.asr.set_property("ivector-extraction-config", "conf/ivector_extractor.fixed.conf")
          self.asr.set_property("max-active", 7000)
          self.asr.set_property("beam", 10.0)
          self.asr.set_property("lattice-beam", 6.0)
          self.asr.set_property("do-endpointing", True)
          self.asr.set_property("endpoint-silence-phones", "1:2:3:4:5:6:7:8:9:10")
          self.asr.set_property("use-threaded-decoder", False)
          self.asr.set_property("chunk-length-in-secs", 0.1)
        else:
          print >> sys.stderr, "Couldn't create the kaldinnet2onlinedecoder element. "
          if os.environ.has_key("GST_PLUGIN_PATH"):
            print >> sys.stderr, "Have you compiled the Kaldi GStreamer plugin?"
          else:
            print >> sys.stderr, "You probably need to set the GST_PLUGIN_PATH envoronment variable"
            print >> sys.stderr, "Try running: GST_PLUGIN_PATH=../src %s" % sys.argv[0]
          sys.exit();
        
        # initially silence the decoder
        self.asr.set_property("silent", True)
        
        self.pipeline = Gst.Pipeline()
        for element in [self.pulsesrc, self.audioconvert, self.audioresample, self.asr, self.fakesink]:
            self.pipeline.add(element)         
        self.pulsesrc.link(self.audioconvert)
        self.audioconvert.link(self.audioresample)
        self.audioresample.link(self.asr)
        self.asr.link(self.fakesink)    
  
        self.asr.connect('partial-result', self._on_partial_result)
        self.asr.connect('final-result', self._on_final_result)        
        self.pipeline.set_state(Gst.State.PLAYING)


    def _on_partial_result(self, asr, hyp):
        #Delete any previous selection, insert text and select it
        Gdk.threads_enter()
        self.textbuf.begin_user_action()
        self.textbuf.delete_selection(True, self.text.get_editable())
        self.textbuf.insert_at_cursor(hyp)
        ins = self.textbuf.get_insert()
        iter = self.textbuf.get_iter_at_mark(ins)
        iter.backward_chars(len(hyp))
        self.textbuf.move_mark(ins, iter)
        self.textbuf.end_user_action()    
        Gdk.threads_leave()
                
    def _on_final_result(self, asr, hyp):
        Gdk.threads_enter()
        #Insert the final result
        self.textbuf.begin_user_action()
        self.textbuf.delete_selection(True, self.text.get_editable())
        self.textbuf.insert_at_cursor(hyp)
        if (len(hyp) > 0):
            self.textbuf.insert_at_cursor(" ")
        self.textbuf.end_user_action()
        self.get_command
        Gdk.threads_leave()

    def get_command(self):
        driver = webdriver.Firefox()
        if (self.textbuf=="run browser"):
            os.system('/usr/bin/firefox')
        if (self.textbuf=="create new tab"):
            os.system('/usr/bin/firefox -new-tab')
        if (self.textbuf=="create new window"):
            os.system('/usr/bin/firefox -new-window')
        if (self.textbuf=="create private tab"):
            os.system('/usr/bin/firefox -private')
        if (self.textbuf=="create private window"):
            os.system('/usr/bin/firefox -private-window') 
        if (self.textbuf=="close tab"):
            driver.close()
        if (self.textbuf=="close browser"):
            driver.quit()
        if (self.textbuf=="watch movie"):
            os.system('/usr/bin/firefox -url kinogo.co')
        if (self.textbuf=="listen to music"):
            os.system('/usr/bin/firefox -url https://music.yandex.ru')
        if (self.textbuf=="show settings"):
            os.system('/usr/bin/firefox -preferences')
        if not (self.textbuf=="open images"):
            os.system('/usr/bin/eom')
        if not (self.textbuf=="run terminal"):
            os.system('/usr/bin/terminal')
        if not (self.textbuf=="open my documents"):
            os.system('/usr/bin/caja --no-desktop --browser')
        if not (self.textbuf=="run notes"):
            os.system('/usr/bin/pluma')
        if not (self.textbuf=="run calculator"):
            os.system('/usr/bin/gnome-calculator')
        if not (self.textbuf=="run office tables"):
            os.system('/usr/bin/libreoffice --calc')
        if not (self.textbuf=="run office impress"):
            os.system('/usr/bin/libreoffice --impress')
        if not (self.textbuf=="run office draw"):
            os.system('/usr/bin/libreoffice --draw')
        if not (self.textbuf=="run office writer"):
            os.system('/usr/bin/libreoffice --writer')

    def button1_clicked(self, button):
       #Handle button Speak presses
        self.asr.set_property("silent", False)

    def button2_clicked(self, button):
       #Handle button Stop presses
        self.asr.set_property("silent", True)    
            

if __name__ == '__main__':
  app = DemoApp()
  Gdk.threads_enter()
  Gtk.main()
  Gdk.threads_leave()

