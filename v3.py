#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[1]:


import tkinter as tk
from tkinter import simpledialog, messagebox
import os
import json
from datetime import datetime
import psutil
import paramiko
from PIL import Image, ImageDraw
import cv2
import pywhatkit
import pyautogui
import time
import random
from pynput.keyboard import Key
from twilio.rest import Client
import boto3
from geopy.geocoders import Nominatim
import ssl
import smtplib
from email.message import EmailMessage
from functools import partial
from googlesearch import search



# Add other necessary imports based on your requirements

# Define the function to open software
def open_software(software_name, status_label):
    software_path = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe",
        "chrome": "chrome.exe",
        "command prompt": "cmd.exe",
        "explorer": "explorer.exe",
        "vlc": "vlc.exe",
        "task manager": "taskmgr",
    }

    if software_name in software_path:
        try:
            os.startfile(software_path[software_name])
        except Exception as e:
            status_label.config(text=f"Error: {e}")
    else:
        status_label.config(text=f"Software '{software_name}' not found.")
        

        
    
class TaskManager:
    def __init__(self, root):
        self.root = root
        self.to_do_window = None  # Store reference to the Toplevel window
        self.tasks = []
        self.load_tasks()

    def create_to_do_window(self):
        if self.to_do_window is None or not self.to_do_window.winfo_exists():
            # Create a new window only if it doesn't exist or has been closed
            self.to_do_window = tk.Toplevel(self.root)
            self.to_do_window.title("To-Do List")

            # Rest of your code for creating the to-do window...
            
            self.task_listbox = tk.Listbox(self.to_do_window, selectmode=tk.SINGLE, width=40, height=10)
            self.task_listbox.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

            self.task_entry = tk.Entry(self.to_do_window, width=30)
            self.task_entry.grid(row=1, column=0, padx=10, pady=10)

            add_button = tk.Button(self.to_do_window, text="Add Task", command=self.add_task)
            add_button.grid(row=1, column=1, padx=10, pady=10)

            remove_button = tk.Button(self.to_do_window, text="Remove Selected", command=self.remove_selected_task)
            remove_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

            self.update_task_listbox()
        else:
            # Bring the existing window to the front
            self.to_do_window.lift()

    def load_tasks(self):
        try:
            with open('tasks.json', 'r') as file:
                self.tasks = json.load(file)
        except FileNotFoundError:
            self.tasks = []

    def save_tasks(self):
        with open('tasks.json', 'w') as file:
            json.dump(self.tasks, file)

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.tasks.append({'title': task, 'created_at': str(datetime.now()), 'completed': False})
            self.save_tasks()
            self.update_task_listbox()
            self.task_entry.delete(0, tk.END)

    def remove_selected_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            self.tasks.pop(selected_task_index[0])
            self.save_tasks()
            self.update_task_listbox()

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for index, task in enumerate(self.tasks, start=1):
            status = "Completed" if task['completed'] else "Pending"
            self.task_listbox.insert(tk.END, f"{index}. {task['title']} - {status}")

def create_task_manager(root):
    return TaskManager(root)

def tasks():
    task_manager.create_to_do_window()


# Define the function to get coordinates
def get_coordinates():
    location_name = simpledialog.askstring("User Input", "Enter place:")
    
    if location_name:
        geolocator = Nominatim(user_agent="location_finder")
        location = geolocator.geocode(location_name)
        
        if location is None:
            show_error(f"Coordinates not found for '{location_name}'.")
        else:
            latitude, longitude = location.latitude, location.longitude
            result_str = f"Coordinates for '{location_name}': Latitude = {latitude}, Longitude = {longitude}."
            messagebox.showinfo("Coordinates", result_str)
    else:
        return "No location provided."    

# Define encryption and decryption functions
def encrypt_word(word):
    if len(word) >= 3:
        # Remove the first letter and place it at the end
        encrypted_word = word[1:] + word[0]
        # Add three random characters to the front
        encrypted_word = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(3)) + encrypted_word
        # Add three random characters to the end
        encrypted_word += ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(3))
        return encrypted_word
    else:
        # Reverse the string
        return word[::-1]

def decrypt_word(word):
    if len(word) >= 9:  # Adjust the condition to reflect the new encryption process
        # Remove three random characters from the front and the end
        decrypted_word = word[3:-3]
        # Remove the last letter and place it at the beginning
        decrypted_word = decrypted_word[-1] + decrypted_word[:-1]
        return decrypted_word
    else:
        # Reverse the string
        return word[::-1]

# Define the encryption tool window
class EncryptionWindow(tk.Toplevel):
    def __init__(self, master=None, args=None):
        super().__init__(master)
        self.title("Encryption Tool")

        self.choice_var = tk.IntVar()
        self.choice_var.set(1)

        tk.Label(self, text="Encryption or Decryption?").pack(pady=10)

        tk.Radiobutton(self, text="Encrypt", variable=self.choice_var, value=1).pack()
        tk.Radiobutton(self, text="Decrypt", variable=self.choice_var, value=2).pack()

        tk.Label(self, text="Enter something to process:").pack(pady=10)
        self.input_entry = tk.Entry(self)
        self.input_entry.pack()

        tk.Button(self, text="Process", command=self.process).pack(pady=10)

    def process(self):
        choice = self.choice_var.get()
        inp = self.input_entry.get()

        if choice == 1:  # Encryption
            encrypted_text = ' '.join(encrypt_word(word) for word in inp.split())
            messagebox.showinfo("Encrypted", f"Encrypted: {encrypted_text}")

        elif choice == 2:  # Decryption
            decrypted_text = ' '.join(decrypt_word(word) for word in inp.split())
            messagebox.showinfo("Decrypted", f"Decrypted: {decrypted_text}")

        else:
            messagebox.showerror("Error", "Invalid choice. Please choose 1 or 2.")


# Define the personal assistant window
class AssistantWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Personal Assistant")

        tk.Label(self, text="Personal Assistant Bot is ready. Type 'exit' to end.").pack(pady=10)

        tk.Button(self, text="Set Reminder", command=self.set_reminder).pack(pady=10)
        tk.Button(self, text="Get Time", command=self.get_time).pack(pady=10)
        tk.Button(self, text="Answer Query", command=self.answer_query).pack(pady=10)

    def set_reminder(self):
        task = simpledialog.askstring("Set Reminder", "What task would you like to set a reminder for?")
        due_date = simpledialog.askstring("Set Reminder", "When is it due? (Format: YYYY-MM-DD HH:MM)")
        assistant.set_reminder(task, due_date)

    def get_time(self):
        assistant.get_time()

    def answer_query(self):
        query = simpledialog.askstring("Answer Query", "What would you like to ask?")
        assistant.answer_query(query)

class PersonalAssistant:
    def __init__(self):
        self.reminders = []

    def set_reminder(self, task, due_date):
        self.reminders.append({'task': task, 'due_date': due_date})
        print(f"Reminder set: {task} on {due_date}")

    def get_time(self):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"The current time is {current_time}")

    def check_reminders(self):
        current_time = datetime.datetime.now()
        for reminder in self.reminders:
            due_date = datetime.datetime.strptime(reminder['due_date'], "%Y-%m-%d %H:%M")
            if current_time >= due_date:
                print(f"Reminder: {reminder['task']} is due!")

    def answer_query(self, query):
        if 'your name' in query:
            print("I am your personal assistant bot.")
        elif 'how are you' in query:
            print("I'm just a computer program, but thanks for asking!")
        else:
            print("Sorry, I don't understand that query.")

    def start_assistant(self):
        print("Personal Assistant Bot is ready. Type 'exit' to end.")
        while True:
            self.check_reminders()  # Check for due reminders in each iteration
            user_input = input("How can I assist you? ")

            if user_input.lower() == 'exit':
                print("Exiting Personal Assistant Bot. Goodbye!")
                break

            elif 'reminder' in user_input.lower():
                task = input("What task would you like to set a reminder for? ")
                due_date = input("When is it due? (Format: YYYY-MM-DD HH:MM) ")
                self.set_reminder(task, due_date)

            elif 'time' in user_input.lower():
                self.get_time()

            elif 'query' in user_input.lower():
                query = input("What would you like to ask? ")
                self.answer_query(query)

            else:
                print("Sorry, I didn't understand that command.")


                
                
def whatsapp():
    phone_number = simpledialog.askstring("WhatsApp", "Enter phone number:")
    if phone_number:
        try:
            pywhatkit.sendwhatmsg(phone_number, "Hello Linux World", time.localtime().tm_hour, time.localtime().tm_min + 1)
            time.sleep(20)
            pyautogui.click()
            time.sleep(5)
            pyautogui.press('enter')
            show_result("Message sent!")
        except Exception as e:
            show_error(str(e))

def message():

        client = Client("AC39df9b5371dgfgfgfg", "b3gdaghsjdmhd")
        client.messages.create(to="+955522122", 
                               from_="+1412355555", 
                               body="Hello Linux World!")
        print("message sent")
        
        
def Email():
    email_sender = 'your_email@gmail.com'  # Replace with your email
    email_password = 'your_password'  # Replace with your email password
    email_receiver = simpledialog.askstring("Email", "Enter your email:")

    if email_receiver:
        subject = 'Check out my email code'
        body = "Your email body here"

        try:
            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_receiver
            em['Subject'] = subject
            em.set_content(body)

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())

            show_result("Email Sent")
        except Exception as e:
            show_error(f"Email error: {str(e)}")


def instagram_upload():
    username = "  xxxx "
    password = "  xxxx"

    bot = Bot()

    bot.login(username=username, password=password, use_cookie=False, ask_for_code=True)

    image_path = "captain.jpg"
    image = Image.open(image_path)
    width, height = image.size
    min_dimension = min(width, height)
    resized_image = image.crop((0, 0, min_dimension, min_dimension))

    temp_image_path = "temp.jpg"
    resized_image.save(temp_image_path)

    caption = "Check out this cool picture!"

    try:
        bot.upload_photo(temp_image_path, caption=caption)
        show_result("Image uploaded to Instagram successfully!")
    except Exception as e:
        show_error(f"Instagram upload error: {str(e)}")
        


        
def click_photo():

   cap=cv2.VideoCapture(0)
   cap
   status ,photo =cap.read()
   cv2.imwrite("pic.jpg",photo)
   cv2.imshow("My photo",photo)
   cv2.waitKey(5000)
   cv2.destroyAllWindows()
   cap.release()

def crop_pic():
   cap=cv2.VideoCapture(0)
   cap
   status ,photo =cap.read()
   cv2.imwrite("pic.jpg",photo)
   cv2.imshow("My photo",photo[200:540,200:430])
   cv2.waitKey(5000)
   cv2.destroyAllWindows()
   cap.release()
    

def capture_video():
    cap=cv2.VideoCapture(0)
    while True:
        status ,photo=cap.read()
        cv2.imshow("My photo",photo)
        if cv2.waitKey(5)==13:
            break
    cv2.destroyAllWindows()

def capture_crop_video():
    cap=cv2.VideoCapture(0)
    while True:
        status ,photo=cap.read()
        photo[0:200,0:200]=photo[200:400,200:400]
        cv2.imshow("My photo",photo)
        if cv2.waitKey(5)==13:
            break
    cv2.destroyAllWindows()

    
def image_100_100():
    width, height = 800, 600
    image = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    stripe_height = height // 3
    draw.rectangle([(0, 0), (width, stripe_height)], fill=(255, 153, 51))
    draw.rectangle([(0, stripe_height), (width, 2 * stripe_height)], fill=(255, 255, 255))
    draw.rectangle([(0, 2 * stripe_height), (width, height)], fill=(0, 128, 0))
    chakra_radius = min(width, height) // 8
    chakra_center = (width // 2, stripe_height + (stripe_height // 2))
    draw.ellipse(
    [
        (chakra_center[0] - chakra_radius, chakra_center[1] - chakra_radius),
        (chakra_center[0] + chakra_radius, chakra_center[1] + chakra_radius),
    ],
    fill=(0, 56, 168),
    )

    image.save("indian_flag.png")
    image.show()



def animated():    
    import cv2
    import numpy as np

    def cartoonize_image(image, gray_mode=False):
    # Convert image to grayscale
        if gray_mode:
            gray = image
        else:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply median blur to reduce noise and smooth the image
        gray = cv2.medianBlur(gray, 5)
    
    # Detect edges in the image using adaptive thresholding
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    
    # Create a color version of the image
        color = cv2.bilateralFilter(image, 9, 300, 300)
    
    # Combine the edges with the color image using a bitwise AND operation
        cartoon = cv2.bitwise_and(color, color, mask=edges)
    
        return cartoon

    def cartoonize_video():
    # Start video capture
        cap = cv2.VideoCapture(0)
    
        while True:
            ret, frame = cap.read()
            if not ret:
                break
        
        # Flip the frame horizontally for a more intuitive selfie view
            frame = cv2.flip(frame, 1)
        
        # Apply cartoonize effect to the frame
            cartoon_frame = cartoonize_image(frame)
        
        # Show the original and cartoonized frames side by side
            stacked_frames = np.hstack((frame, cartoon_frame))
            cv2.imshow("Cartoonizer", stacked_frames)
        
        # Press 'q' to exit the loop
            if cv2.waitKey(1) == 13:
                break
    
    # Release video capture and destroy windows
        cap.release()
        cv2.destroyAllWindows()

    if __name__ == "__main__":
        cartoonize_video()    
        
        
        
        
        
    
def launch_instance():
    region = 'ap-south-1'
    
    instance_name = simpledialog.askstring("Instance Name", "Enter instance name:")
    
    if instance_name:
        ec2_client = boto3.client('ec2', region_name=region)
        response = ec2_client.run_instances(
            ImageId='ami-0da59f1af71ea4ad2',
            InstanceType='t2.micro',
            MaxCount=1,
            MinCount=1,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': instance_name
                        },
                    ]
                },
            ]
        )
        
        instance_id = response['Instances'][0]['InstanceId']
        messagebox.showinfo("Instance Launched", f"Instance '{instance_id}' launched successfully!")
    else:
        messagebox.showwarning("Instance Launch", "No instance name provided.")

    
    

    
def create_bucket():
    bucket_name = simpledialog.askstring("Bucket Name", "Enter bucket name:")
    if bucket_name:
        s3_client = boto3.client('s3', region_name='ap-south-1')
        s3_client.create_bucket(
            Bucket=bucket_name,
            ACL='private',
            CreateBucketConfiguration={
                'LocationConstraint': 'ap-south-1'
            }
        )
        messagebox.showinfo("Bucket Created", f"Bucket '{bucket_name}' created successfully!")
    else:
        messagebox.showwarning("Bucket Creation", "No bucket name provided.")
        
        
        
def upload_file():
    object = boto3.client('s3')
    object.upload_file(r"C:\Users\asus\Pictures\captain america\captain.jpg",'ka12','pics')
    download_object = boto3.client('s3')
    download_object.download_file('ka12','pics', 'captain.jpeg')

    
    
def use_sns_service():
    sns = boto3.client('sns',region_name='ap-south-1')
    sns.publish(
    Message='Dont take it serious.',
    Subject='this is automatd sns service.',
    TopicArn='arn:aws:sns:ap-south-1:299592517672:python_menu'
    )
    print("email sent")
    
            
def establish_ssh_connection_with_key(host, port, username, private_key_path):
    try:
        ssh_client = paramiko.SSHClient()

        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        private_key = paramiko.RSAKey(filename=private_key_path)

        ssh_client.connect(host, port=port, username=username, pkey=private_key)

        print("SSH Connection Established Successfully!")

        ssh_client.close()

    except Exception as e:
        print(f"Error: {e}")

establish_ssh_connection_with_key("your_ssh_host", 22, "your_ssh_username", "path/to/private_key.pem")



def top_10_google_searches(query):
    try:
        search_results = list(search(query, num_results=10))
        result_text = f"Top Google searches for '{query}':\n"
        for index, result in enumerate(search_results, start=1):
            result_text += f"{index}. {result}\n"

        # Create a new window to display the search results
        result_window = tk.Toplevel(root)
        result_window.title("Google Search Results")

        result_label = tk.Label(result_window, text=result_text, font=("Arial", 12))
        result_label.pack(padx=10, pady=10)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")



# Function to show an error message in a new window
def show_error(message):
    error_window = tk.Toplevel(root)
    error_window.title("Error")
    error_label = tk.Label(error_window, text=message, font=("Arial", 12))
    error_label.pack(padx=10, pady=10)

# Function to show a result message in a new window
def show_result(result):
    result_window = tk.Toplevel(root)
    result_window.title("Result")
    result_label = tk.Label(result_window, text=result, font=("Arial", 12))
    result_label.pack(padx=10, pady=10)

# Function to create a button
def create_window(command):
    window = tk.Toplevel(root)
    command(window)

def create_button(parent, label, command, icon=None):
    button = tk.Button(parent, text=label, font=("Arial", 10, "bold"), width=20, height=2, command=command)
    button.default_text = label  # Set default text for the button
    if icon:
        button.config(image=icon, compound="top")
    return button




# Function to clear the status label
def clear_status(status_label):
    status_label.config(text="Status")


# Main window class
class MainWindow:
    def __init__(self, master):
        self.master = master
        master.title("Main Window")
        master.geometry("1200x900")
        master.configure(bg="#434184")

        
        
        title_label = tk.Label(root, text="Welcome to GUI Based Menu",width=30,height=2, font="title_font", fg="blue")
        title_label.pack(pady=15)
        
        
        open_button = tk.Button(root, text="Open Software", fg="red", font=("Arial", 20, "bold"), width=25, command=lambda: open_software(software_entry.get().lower(), status_label))
        open_button.pack()
        
        software_entry = tk.Entry(root, width=64)
        software_entry.pack(pady=20)


        buttons_frame = tk.Frame(root)
        buttons_frame.pack(side=tk.TOP, pady=10)

        # Function to create stylish headers
        def create_header_frame(parent, text):
            header_frame = tk.Frame(parent, bg="#434184")
            header_label = tk.Label(header_frame, text=text, font=("Arial", 16, "bold"), fg="white", bg="#434184", pady=5)
            header_label.pack()
            return header_frame

        # Stylish headers and buttons in frames
        header1_frame = create_header_frame(buttons_frame, "Tools")
        header1_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        header2_frame = create_header_frame(buttons_frame, "Messaging")
        header2_frame.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")

        header3_frame = create_header_frame(buttons_frame, "Camera")
        header3_frame.grid(row=0, column=2, padx=20, pady=10, sticky="nsew")

        header4_frame = create_header_frame(buttons_frame, "AWS")
        header4_frame.grid(row=0, column=3, padx=20, pady=10, sticky="nsew")

        # ... (your existing code for creating buttons)

        # Additional buttons for the menu
        button_encrypt = create_button(buttons_frame, "Encrypt/Decrypt", EncryptionWindow)

        button_assistant = create_button(buttons_frame, "Your Assistant", AssistantWindow)
        button_coordinates = create_button(buttons_frame,"GEO COORDINATES" ,lambda:get_coordinates())
        button_task_tracker = create_button(buttons_frame, "Task Tracker", lambda: task_manager.create_to_do_window())
        button_ram = create_button(buttons_frame, "Find RAM Usage", command=lambda: show_result(f"RAM memory % used: {psutil.virtual_memory().percent}\nRAM Used (GB): {psutil.virtual_memory().used / 1000000000}"))
        
        button_ssh_connection = create_button(buttons_frame, "SSH Connection", lambda: establish_ssh_connection_with_key("your_ssh_host", 22, "your_ssh_username", "path/to/private_key.pem"))
        button_launch_instance = create_button(buttons_frame, "Launch Instance", launch_instance)
        button_create_bucket = create_button(buttons_frame, "Create Bucket", create_bucket)
        button_upload_file = create_button(buttons_frame, "Upload File to S3", upload_file)
        button_use_sns_service = create_button(buttons_frame, "Use SNS Service", use_sns_service)
        
        button_whatsapp = create_button(buttons_frame, "SEND WHATSAPP", whatsapp)
        button_message = create_button(buttons_frame, "SEND MESSAGE", message)
        button_instagramupload = create_button(buttons_frame,"INSTAGRAM POST",instagram_upload)
        button_email = create_button(buttons_frame,"SEND EMAIL",Email)
        button_twitterupload = create_button(buttons_frame,"Twitter POST",instagram_upload)
        
        
        button_photo = create_button(buttons_frame, "CLICK PHOTO",click_photo)
        button_croppic = create_button(buttons_frame, "FACE CAPTURE",crop_pic)
        button_video = create_button(buttons_frame, "CAPTURE VIDEO",capture_video)
        button_animated = create_button(buttons_frame, "ANIMATED Live VIDEO",animated)
        button_cropvideo = create_button(buttons_frame,"CROP LIVE VIDEO",capture_crop_video)
        button_image= create_button(buttons_frame,"IMAGE 100*100",image_100_100)
        

        # Create and pack the buttons
        button_ram.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        button_coordinates.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        button_task_tracker.grid(row=3, column=0, padx=20, pady=20, sticky="nsew")
        button_encrypt.grid(row=4, column=0, padx=20, pady=20, sticky="nsew")
        button_assistant.grid(row=5, column=0, padx=20, pady=20, sticky="nsew")

        button_whatsapp.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")
        button_message.grid(row=2, column=1, padx=20, pady=20, sticky="nsew")
        button_email.grid(row=3, column=1, padx=20, pady=20, sticky="nsew")
        button_instagramupload.grid(row=4, column=1, padx=20, pady=20, sticky="nsew")
        button_twitterupload.grid(row=5, column=1, padx=20, pady=20, sticky="nsew")

        button_croppic.grid(row=1, column=2, padx=20, pady=20, sticky="nsew")
        button_cropvideo.grid(row=2, column=2, padx=20, pady=20, sticky="nsew")
        button_photo.grid(row=3, column=2, padx=20, pady=20, sticky="nsew")
        button_animated.grid(row=4, column=2, padx=20, pady=20, sticky="nsew")
        button_image.grid(row=5, column=2, padx=20, pady=20, sticky="nsew")

        button_launch_instance.grid(row=1, column=3, padx=20, pady=20, sticky="nsew")
        button_create_bucket.grid(row=2, column=3, padx=20, pady=20, sticky="nsew")
        button_upload_file.grid(row=3, column=3, padx=20, pady=20, sticky="nsew")
        button_use_sns_service.grid(row=4, column=3, padx=20, pady=20, sticky="nsew")
        button_ssh_connection.grid(row=5, column=3, padx=20, pady=20, sticky="nsew")
        
        
        # Google Search Bar
        search_frame = tk.Frame(root, bg="#8e8db5")
        search_frame.pack(pady=20)

        search_label = tk.Label(search_frame, text="Google Search:", font=("Arial", 12, "bold"), fg="#FFFFFF", bg="#8e8db5")
        search_label.grid(row=0, column=0, padx=10)

        search_entry = tk.Entry(search_frame, width=40, font=("Arial", 12))
        search_entry.grid(row=0, column=1, padx=10)

        def search_button_click():
            top_10_google_searches(search_entry.get())

        search_button = tk.Button(search_frame, text="Search", font=("Arial", 12, "bold"), fg="#FFFFFF", bg="#4CAF50",
                                  command=search_button_click)
        search_button.grid(row=0, column=2, padx=10)


        status_label = tk.Label(root, text="Status", fg="red")
        status_label.pack(pady=10)

        clear_button = tk.Button(root, text="Clear Status", fg="blue", font=("Arial", 14, "bold"), width=25, command=lambda: clear_status(status_label))
        clear_button.pack(pady=10)

# Main part of the script
    
if __name__ == "__main__":
    root = tk.Tk()
    task_manager = create_task_manager(root)
    app = MainWindow(root)
    root.mainloop()


