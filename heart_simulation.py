import time
import os

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

class Heart:
    """
    A class to simulate the basic functions of a human heart.
    """
    def __init__(self, heart_rate=75):
        """
        Initializes the Heart.
        
        Args:
            heart_rate (int): The number of beats per minute (BPM).
        """
        if heart_rate <= 0:
            raise ValueError("Heart rate must be positive.")
            
        self.heart_rate = heart_rate
        # The cardiac cycle has two main phases (Diastole and Systole).
        # Time per phase = (60 seconds / BPM) / 2
        self.phase_interval = (60 / self.heart_rate) / 2
        
        # Physiological parameters (average values in mL)
        self.max_volume = 120  # End-diastolic volume (full)
        self.min_volume = 50   # End-systolic volume (after pumping)
        self.stroke_volume = self.max_volume - self.min_volume
        
        # Starting state
        self.current_volume = self.min_volume
        self.state = "Systole (Contracting)" # Start just after a beat
        
    def beat(self):
        """Simulates a single phase of the cardiac cycle (one half of a beat)."""
        if self.state == "Systole (Contracting)":
            # Switch to Diastole: relax and fill with blood
            self.state = "Diastole (Relaxing)"
            self.current_volume = self.max_volume
            print(f"❤️  Diastole: Chambers are filling with blood.")
            
        elif self.state == "Diastole (Relaxing)":
            # Switch to Systole: contract and pump blood
            self.state = "Systole (Contracting)"
            self.current_volume = self.min_volume
            print(f"💥 Systole: Pumping {self.stroke_volume} mL of blood to the body!")

    def get_status(self):
        """Returns a string with the current status of the heart."""
        return (
            f"  └── State: {self.state}\n"
            f"  └── Ventricle Volume: {self.current_volume}/{self.max_volume} mL"
        )

# --- Main Simulation Loop ---
if __name__ == "__main__":
    try:
        my_heart = Heart(heart_rate=75)
        print(f"Starting heart simulation at {my_heart.heart_rate} BPM. Press CTRL+C to stop.")
        time.sleep(2)

        while True:
            clear_screen()
            print(f"--- 🩺 Heart Simulation 🩺 ---")
            print(f"Time: {time.strftime('%H:%M:%S')}")
            print(f"Heart Rate: {my_heart.heart_rate} BPM\n")
            
            # Perform one phase of the beat
            my_heart.beat()
            
            # Print the current status
            print(my_heart.get_status())
            
            # Wait for the calculated interval before the next phase
            time.sleep(my_heart.phase_interval)

    except KeyboardInterrupt:
        print("\nSimulation stopped by user. The heart is at rest.")
    except ValueError as e:
        print(f"Error: {e}")