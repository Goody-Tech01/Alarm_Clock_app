import customtkinter as ctk                            
from datetime import datetime,timedelta
import pygame
import os

pygame.mixer.init()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class AlarmClockApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("My alarm clock⏰")
        self.geometry("500x700")
        self.resizable(True,True)

        self.alarms = []

        self.clock_label=ctk.CTkLabel(self,text="00:00:00",text_color="silver",font=ctk.CTkFont(size=60,weight="bold"),)    #clock display
        self.clock_label.pack(pady=40)

        frame = ctk.CTkFrame(self)
        frame.pack(pady=10)


        self.hour_var = ctk.StringVar(value="00")
        self.hour_menu = ctk.CTkOptionMenu(
            frame, values=[f"{i:02}" for i in range(1,13)], variable=self.hour_var, width=80)
        self.hour_menu.pack(side="left", padx=5)


        self.min_var = ctk.StringVar(value="00")
        self.min_menu = ctk.CTkOptionMenu(
            frame, values=[f"{i:02}" for i in range(60)], variable=self.min_var, width=80)
        self.min_menu.pack(side="left", padx=5)


        self.period_var=ctk.StringVar(value="AM")                    #AM\PM
        self.period_menu=ctk.CTkOptionMenu(frame,
                                           values=["AM","PM"],variable=self.period_var,width=80)
        self.period_menu.pack(side="left",padx=5)

        self.task_entry=ctk.CTkEntry(self,placeholder_text="Enter task:")
        self.task_entry.pack(pady=10)

        self.set=ctk.CTkButton(self,text="Set Alarm",command=self.set_alarm,fg_color="#ff4da6",hover_color="#e60073")                       #Buttons
        self.set.pack(pady=10)

        self.stop=ctk.CTkButton(self,text="Stop Alarm",command=self.stop_alarm,fg_color="#ff4da6",hover_color="#e60073")
        self.stop.pack(pady=10)

        self.snooze=ctk.CTkButton(self,text="Snooze(2 min)",command=self.snooze_alarm,fg_color="#ff4da6",hover_color="#e60073")
        self.snooze.pack(pady=10)

        self.alarm_list=ctk.CTkTextbox(self,width=300,height=100)
        self.alarm_list.pack(pady=10)

        self.status_label=ctk.CTkLabel(self,text="")
        self.status_label.pack(pady=20)

        self.update_clock()



    def update_clock(self):
        now=datetime.now()

        display_time=now.strftime("%I:%M:%S %p")
        self.clock_label.configure(text=display_time)
        current_time=now.strftime("%I:%M")

        for alarm in self.alarms:
            if alarm ["time"]==current_time and not alarm ["triggered"]:
                self.trigger_alarm(alarm["task"])
                alarm["triggered"]=True
        self.after(1000,self.update_clock)

    def set_alarm(self):
            hour = int(self.hour_var.get())
            minute = int(self.min_var.get())
            period = self.period_var.get()


            if period == "PM" and hour != 12:
                hour += 12
            elif period == "AM" and hour == 12:
                hour = 0

            alarm_time = f"{hour:02}:{minute:02}"
            task=self.task_entry.get()

            self.alarms.append({
                "time": alarm_time,
                "task": task if task else "No task",
                "triggered":False
            })

            self.update_alarm_list()
            self.status_label.configure(
                text=f"Alarm set to {alarm_time} "
            )
    def trigger_alarm(self,task):
       try:
           file_path=os.path.join(os.getcwd(),"alarm.mp3")
           pygame.mixer.music.load(file_path)
           pygame.mixer.music.set_volume(1.0)
           pygame.mixer.music.play(-1)
           self.status_label.configure(text=f"Alarm Ringing⏰:{task}")
       except Exception as e:
           print(e)
           self.status_label.configure(text="Error: Add mp3 file")


    def stop_alarm(self):
        pygame.mixer.music.stop()
        self.status_label.configure(text="Alarm Stopped")


    def snooze_alarm(self):
        pygame.mixer.music.stop()
        new_time=datetime.now() + timedelta(minutes=2)

        self.alarms.append({
            "time":new_time.strftime("%I:%M"),
            "task":"Snoozed Alarm",
            "triggered":False
        })

        self.update_alarm_list()
        self.status_label.configure(text="Snoozed for 2 minutes")


    def update_alarm_list(self):
        self.alarm_list.delete("1.0","end")

        count=1

        for alarm in self.alarms:
            if alarm["task"]== "Snoozed Alarm":
                continue

            self.alarm_list.insert(
                "end",f"{count}.{alarm["time"]}-{alarm["task"]}\n"
            )
            count+=1

app=AlarmClockApp()
app.mainloop()