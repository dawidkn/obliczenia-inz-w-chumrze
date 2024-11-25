import tkinter as tk
import threading
import time
from datetime import datetime


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Math Race")
        self.root.geometry("830x420")
        
        self.fib_thread = None
        self.prime_thread = None
        self.running = False

        self.fib_numbers = []
        self.prime_numbers = []
        self.timer = 0
        self.calc_time = 10 #standard calculation time in s
        self.temp_time_end = 0
        self.temp_time_start = 0
        self.create_window()

    def fibonacci_calculation(self):
        a, b = 0, 1
        while self.running:
            self.fib_numbers.append(a)
            self.update_fib_position()
            a, b = b, a + b
            # time.sleep(0.01)


    def prime_calculation(self):
        n = 2
        while self.running:
            if all(n % i != 0 for i in range(2, int(n ** 0.5) + 1)):
                self.prime_numbers.append(n)
                self.update_prime_position()
            n += 1
            # time.sleep(0.01)



    def update_fib_position(self):
        self.xSpeed += 10
        if self.xSpeed >= 400:
            self.xSpeed = 0
        self.canvasFib.coords(self.carFib, self.xSpeed, 100)
        self.canvasFib.update()
        self.label_speedFib.config(text=f"Speed: {round(self.xSpeed,1)} [km/h]")
        self.label_CPUFib.config(text=f"CPU usage: {round(self.xSpeed/2,1)} [%]")
        self.label_Fibcount.config(text=f"Fibonacci Counter: {len(self.fib_numbers)}")
        
        # print(len(self.fib_numbers))
        
    def update_prime_position(self):
        self.xSpeed2 += 0.1
        if self.xSpeed2 >= 400:
            self.xSpeed2 = 0
        self.canvasPrime.coords(self.carPrime, self.xSpeed2, 100)
        self.canvasPrime.update()
        self.label_speedPrime.config(text=f"Speed: {round(self.xSpeed2,1)} [km/h]")
        self.label_CPUPrime.config(text=f"CPU usage: {round((self.xSpeed2/2),1)} [%]")
        self.label_PrimeCount.config(text=f"Prime Counter: {len(self.prime_numbers)}")


    def start_calculations(self):
        self.temp_time_start = time.time()

        if not self.running:
            self.running = True
            self.fib_thread = threading.Thread(target=self.fibonacci_calculation, daemon=True)
            self.prime_thread = threading.Thread(target=self.prime_calculation, daemon=True)
            self.fib_thread.start()
            self.prime_thread.start()
    def stop_calculations(self):
        self.running = False
        self.temp_time_end = time.time()

    def reset_calculations(self):
        self.stop_calculations()
        self.fib_numbers = []
        self.prime_numbers = []
        self.xSpeed = 0
        self.xSpeed2 = 0
        self.canvasFib.coords(self.carFib, self.xSpeed, 100)
        self.canvasPrime.coords(self.carPrime, self.xSpeed2, 100)
        self.canvasFib.update()
        self.canvasPrime.update()
        self.label_speedPrime.config(text=f"Speed: {self.xSpeed2} [km/h]")
        self.label_CPUPrime.config(text=f"CPU usage: {self.xSpeed2/2} [%]")
        self.label_speedFib.config(text=f"Speed: {self.xSpeed} [km/h]")
        self.label_CPUFib.config(text=f"CPU usage: {self.xSpeed/2} [%]")
        self.label_PrimeCount.config(text=f"Prime Counter: {len(self.prime_numbers)}")
        self.label_Fibcount.config(text=f"Fibonacci Counter: {len(self.fib_numbers)}")
        self.timer = 0


    def countdown_timer(self, seconds):
        if seconds > 0:
            self.timer_label.config(text=f"Test End in: {seconds}")
            self.root.after(1000, self.countdown_timer, seconds - 1)
        else:

            self.stop_calculations()
            # print("chuj")
            self.timer_label.destroy()
            self.start_button.pack(side="left", padx=5)
            self.stop_button.pack(side="left", padx=5)
            self.reset_button.pack(side="left", padx=5)
            self.standard_test_button.pack(side="left", padx=5)

    def standard_test(self):

        self.reset_calculations()

        self.root.after(0, self.start_calculations)


        self.standard_test_button.pack_forget()#change button to label
        self.reset_button.pack_forget()
        self.start_button.pack_forget()
        self.stop_button.pack_forget()


        self.timer_label = tk.Label(self.button_frame, text="Test End in: 60",width=14)
        self.timer_label.pack(side="left", padx=5)
        self.countdown_timer(self.calc_time)  # Rozpocznij odliczanie od 60 sekund

    def save_score(self):
        self.timer = round(self.temp_time_end-self.temp_time_start,1)
        CPU_NAME = "Inetl"
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        # current_time = 22
        with open('score.txt', 'a') as file:
            file.write(f"\n\n--- Calculation Date: {current_time} ---\
                \n  - Your CPU: {CPU_NAME} \
                \n  - You Found: \
                \n      - Prime Numbers: {len(self.prime_numbers)}\
                \n      - Fibonnaci Numbers: {len(self.fib_numbers)}\
                \n  - Highest Prime Number: {self.prime_numbers[-1]}\
                \n  - Calculation Time: {self.timer} [s]")
        self.reset_calculations()
    def create_window(self):
        self.label = tk.Label(self.root, text="Fibonacci VS Prime")
        self.label.pack(pady=5)

        canvas_frame = tk.Frame(self.root)
        canvas_frame.pack(pady=5)

        # Fibonacci canvas
        labelFib = tk.Label(canvas_frame, text="Fibonacci Calculation")
        labelFib.grid(row=0, column=0, padx=5, pady=2)

        self.canvasFib = tk.Canvas(canvas_frame, width=400, height=200, bg="#a88e32")
        self.canvasFib.grid(row=1, column=0, padx=5, pady=5)
        self.xSpeed = 0
        self.image1 = tk.PhotoImage(file="car1.png")
        self.carFib = self.canvasFib.create_image(self.xSpeed, 100, image=self.image1)

        # Prime canvas
        labelPrime = tk.Label(canvas_frame, text="Prime Numbers Calculation")
        labelPrime.grid(row=0, column=1, padx=5, pady=2)

        self.canvasPrime = tk.Canvas(canvas_frame, width=400, height=200, bg="#e05573")
        self.canvasPrime.grid(row=1, column=1, padx=5, pady=5)
        self.xSpeed2 = 0
        self.image2 = tk.PhotoImage(file="car2.png")
        self.carPrime = self.canvasPrime.create_image(self.xSpeed2, 100, image=self.image2)
        #sub frame speed and cpu monitor--
        #left
        self.canvas_subframe1 = tk.Frame(canvas_frame) #subframe to show speed and cpu monitor
        self.canvas_subframe1.grid(row=2,column=0, padx=5,pady=5)
        #right
        self.canvas_subframe2 = tk.Frame(canvas_frame) #subframe to show speed and cpu monitor
        self.canvas_subframe2.grid(row=2,column=1, padx=5,pady=5)

        #left
        self.label_speedFib = tk.Label(self.canvas_subframe1, text=f"Speed: {self.xSpeed}", width=14, anchor="w")
        self.label_CPUFib = tk.Label(self.canvas_subframe1, text=f"CPU usage: {self.xSpeed}", width=17, anchor="w")
        self.label_Fibcount = tk.Label(self.canvas_subframe1, text=f"Fibonacci Counter: {len(self.fib_numbers)}", width=20, anchor="w")
        self.label_speedFib.grid(row=0,column=0, padx=2,pady=2)
        self.label_CPUFib.grid(row=0,column=1, padx=2,pady=2)
        self.label_Fibcount.grid(row=0,column=2, padx=2,pady=2)

        #right
        self.label_speedPrime = tk.Label(self.canvas_subframe2, text=f"Speed: {self.xSpeed}", width=14, anchor="w")
        self.label_CPUPrime = tk.Label(self.canvas_subframe2, text=f"CPU usage: {self.xSpeed}", width=17, anchor="w")
        self.label_PrimeCount = tk.Label(self.canvas_subframe2, text=f"Prime Counter: {len(self.prime_numbers)}", width=20, anchor="w")
        self.label_speedPrime.grid(row=0,column=0, padx=2,pady=2)       
        self.label_CPUPrime.grid(row=0,column=1, padx=2,pady=2)     
        self.label_PrimeCount.grid(row=0,column=2, padx=2,pady=2)     

        # Buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=5)

        self.start_button = tk.Button(self.button_frame, text="Start", command=self.start_calculations)
        self.start_button.pack(side="left", padx=5)

        self.stop_button = tk.Button(self.button_frame, text="Stop", command=self.stop_calculations)
        self.stop_button.pack(side="left", padx=5)

        self.reset_button = tk.Button(self.button_frame, text="Reset", command=self.reset_calculations)
        self.reset_button.pack(side="left", padx=5)

        self.standard_test_button = tk.Button(self.button_frame, text="Standard Test", command=self.standard_test,width=14)
        self.standard_test_button.pack(side="left", padx=5)


        save_button = tk.Button(self.root, text="Save Score", command=self.save_score)
        save_button.pack(padx=5, pady=5)

        close_button = tk.Button(self.root, text="Close All", command=self.on_close)
        close_button.pack(padx=5, pady=5)


        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def on_close(self):



        self.running = False
        self.root.quit()
        self.root.destroy()


if __name__ == "__main__":
    window1 = MainWindow()
