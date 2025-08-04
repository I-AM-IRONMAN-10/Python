from itertools import combinations
from datetime import datetime

def extract_date_digits(date):
   
    return list(date.replace("-", ""))

def generate_date_pins(dates, pin_length):

    all_combinations_2part = {}
    all_combinations_1part = {}

    for date in dates:
        digits = extract_date_digits(date)

        for r in range(2, len(digits) + 1):
            for combo in combinations(digits, r):
                pin = "".join(combo)
                if len(pin) == pin_length:
                    all_combinations_2part[pin] = combo

        for r in range(1, len(digits) + 1):
            for combo in combinations(digits, r):
                pin = "".join(combo)
                if len(pin) == pin_length and pin not in all_combinations_2part:
                    all_combinations_1part[pin] = combo

    return all_combinations_2part, all_combinations_1part

def generate_phone_pins(phone_numbers, pin_length):
    
    phone_pins = set()

    for phone in phone_numbers:
        if len(phone) >= pin_length:
            phone_pins.add(phone[:pin_length])
            phone_pins.add(phone[-pin_length:])

        if pin_length == 3 and len(phone) >= 6:
            phone_pins.add(phone[3:6])

        elif pin_length == 4 and len(phone) >= 8:
            phone_pins.add(phone[:2] + phone[-2:])

        elif pin_length == 6 and len(phone) >= 10:
            phone_pins.add(phone[:3] + phone[-3:])

    if pin_length % 2 == 0:
        half_len = pin_length // 2
        for phone in phone_numbers:
            if len(phone) >= pin_length:
                phone_pins.add(phone[:half_len] + phone[-half_len:])

    if len(phone_numbers) > 1 and pin_length % 2 == 0:
        half_len = pin_length // 2
        for phone1, phone2 in combinations(phone_numbers, 2):
            if len(phone1) >= half_len and len(phone2) >= half_len:
                phone_pins.add(phone1[:half_len] + phone2[:half_len])
                phone_pins.add(phone1[:half_len] + phone2[-half_len:])
                phone_pins.add(phone1[-half_len:] + phone2[:half_len])
                phone_pins.add(phone1[-half_len:] + phone2[-half_len:])

    return {pin for pin in phone_pins if len(pin) == pin_length}

def generate_repeating_pins(pin_length):
   
    return {str(digit) * pin_length for digit in range(10)}

def generate_sequential_pins(pin_length):
    
    sequential_pins = set()
    digits = "0123456789"

    for i in range(10 - pin_length + 1):
        sequential_pins.add(digits[i:i + pin_length])

    for i in range(10 - pin_length + 1):
        sequential_pins.add(digits[::-1][i:i + pin_length])

    return sequential_pins

def generate_all_pins(pin_length, date_pins_2part, date_pins_1part, phone_pins):
   
    limit = 10**pin_length
    all_pins = {str(i).zfill(pin_length) for i in range(limit)}

    date_pins = set(date_pins_2part.keys()) | set(date_pins_1part.keys())
    phone_pins_set = set(phone_pins)

    unique_pins = sorted(all_pins - date_pins - phone_pins_set)
    repeating_pins = generate_repeating_pins(pin_length)
    sequential_pins = generate_sequential_pins(pin_length)

    priority_pins = sorted((repeating_pins | sequential_pins) - date_pins - phone_pins_set)
    final_pins = sorted(set(unique_pins) - repeating_pins - sequential_pins)

    return priority_pins, final_pins

def validate_date(date):
   
    try:
        datetime.strptime(date, "%d-%m-%Y")
        return True
    except ValueError:
        return False

def validate_phone_number(phone):
    
    return phone.isdigit() and len(phone) >= 6

def validate_pin(pin, pin_length):
   
    return pin.isdigit() and len(pin) == pin_length

# input for PIN length
while True:
    try:
        pin_length = int(input("Enter the PIN length (e.g., 4): "))
        if pin_length <= 0:
            print("PIN length must be a positive integer. Try again.")
        else:
            break
    except ValueError:
        print("Invalid input. Please enter a valid integer.")

#  custom guesses from user
while True:
    try:
        num_custom_guesses = int(input(f"How many custom {pin_length}-digit guesses would you like to provide? "))
        if num_custom_guesses < 0:
            print("Number of guesses cannot be negative. Try again.")
        else:
            break
    except ValueError:
        print("Invalid input. Please enter a valid integer.")

#  guesses from user
custom_guesses = []
for i in range(num_custom_guesses):
    while True:
        guess = input(f"Enter guess #{i+1} ({pin_length}-digit number): ")
        if validate_pin(guess, pin_length):
            if guess in custom_guesses:
                print("You already entered this guess. Try a different one.")
            else:
                custom_guesses.append(guess)
                break
        else:
            print(f"Invalid PIN. Please enter a {pin_length}-digit number.")

#  dates
while True:
    try:
        n = int(input("Enter the number of dates: "))
        if n <= 0:
            print("Number of dates must be a positive integer. Try again.")
        else:
            break
    except ValueError:
        print("Invalid input. Please enter a valid integer.")

dates = []
for i in range(n):
    while True:
        date = input(f"Enter date {i+1} (DD-MM-YYYY): ")
        if validate_date(date):
            dates.append(date)
            break
        else:
            print("Invalid date format. Please enter a date in DD-MM-YYYY format.")

#phonenum
while True:
    try:
        m = int(input("Enter the number of phone numbers: "))
        if m <= 0:
            print("Number of phone numbers must be a positive integer. Try again.")
        else:
            break
    except ValueError:
        print("Invalid input. Please enter a valid integer.")

phone_numbers = []
for i in range(m):
    while True:
        phone = input(f"Enter phone number {i+1}: ")
        if validate_phone_number(phone):
            phone_numbers.append(phone)
            break
        else:
            print("Invalid phone number. Please enter a valid phone number (at least 6 digits).")

# G date-based PINs
date_pins_2part, date_pins_1part = generate_date_pins(dates, pin_length)

#  repeating  sequential PINs
priority_pins = generate_repeating_pins(pin_length) | generate_sequential_pins(pin_length)

# phone-based PINs
phone_pins = generate_phone_pins(phone_numbers, pin_length)

# all remaining PINs
_, all_remaining_pins = generate_all_pins(pin_length, date_pins_2part, date_pins_1part, phone_pins)

#  Save and print output
filename = input("Enter the filename to save the output (e.g., output.ino): ")

with open(filename, "w") as file:
    
    file.write("#include <Arduino.h>\n")
    file.write("#include <MD5.h>\n\n")
    file.write("// Target hash for comparison (MD5)\n")
    file.write("const char TARGET_HASH[] = \"5f4dcc3b5aa765d61d8327deb882cf99\"; // Example: MD5 of 'password'\n\n")
    file.write("// Custom list of numbers/passwords to try\n")
    file.write("const char* PASSWORDS[] = {\n")
    
    # custom guesses first 
    for guess in custom_guesses:
        file.write(f'    "{guess}",\n')
    
    #  date-based PINs (2part)
    for pin in date_pins_2part:
        file.write(f'    "{pin}",\n')
    
    # date-based PINs (1part)
    for pin in date_pins_1part:
        file.write(f'    "{pin}",\n')
    
    # priority PINs 
    for pin in priority_pins:
        file.write(f'    "{pin}",\n')
    
    # phone-based PINs
    for pin in phone_pins:
        file.write(f'    "{pin}",\n')
    
    #  all remaining PINs
    for pin in all_remaining_pins:
        file.write(f'    "{pin}",\n')
    
    file.write("};\n")
    file.write(f"const int NUM_PASSWORDS = sizeof(PASSWORDS) / sizeof(PASSWORDS[0]);\n\n")
    
    
    file.write("bool checkHashCollision(const char* password) {\n")
    file.write("  MD5 md5;\n")
    file.write("  md5.reset();\n")
    file.write("  md5.update(password, strlen(password));\n")
    file.write("  md5.finalize();\n")
    file.write("  char computedHash[33];\n")
    file.write("  md5.print(computedHash);\n")
    file.write("  return (strcmp(computedHash, TARGET_HASH) == 0);\n")
    file.write("}\n\n")
    
    
    file.write("void enterPassword(const char* password) {\n")
    file.write("  int length = 0;\n")
    file.write("  while (password[length] != '\\0') {\n")
    file.write("    length++;\n")
    file.write("  }\n")
    file.write("  for (int j = 0; j < length; j++) {\n")
    file.write("    char digit = password[j];\n")
    file.write("    pressKeypadButton(digit);\n")
    file.write("    delay(100); // Simulate human typing speed\n")
    file.write("  }\n")
    file.write("  pressKeypadButton('#'); // Submit the password\n")
    file.write("}\n\n")
    
    file.write("void pressKeypadButton(char button) {\n")
    file.write("  // Simulate pressing a keypad button\n")
    file.write("  Serial.print(\"Pressing button: \");\n")
    file.write("  Serial.println(button);\n")
    file.write("}\n\n")
    
    
    file.write("void setup() {\n")
    file.write("  Serial.begin(9600);\n")
    file.write("  Serial.println(\"Starting security testing...\");\n")
    file.write("  Serial.print(\"Total passwords to try: \");\n")
    file.write("  Serial.println(NUM_PASSWORDS);\n")
    file.write("}\n\n")
    
    file.write("void loop() {\n")
    file.write("  // PHASE 1: Hash collision detection\n")
    file.write("  Serial.println(\"\\n=== Starting hash collision detection ===\");\n")
    file.write("  for (int i = 0; i < NUM_PASSWORDS; i++) {\n")
    file.write('    Serial.print("Hash Check [");\n')
    file.write('    Serial.print(i+1);\n')
    file.write('    Serial.print("/");\n')
    file.write('    Serial.print(NUM_PASSWORDS);\n')
    file.write('    Serial.print("]: ");\n')
    file.write('    Serial.println(PASSWORDS[i]);\n')
    file.write("    if(checkHashCollision(PASSWORDS[i])) {\n")
    file.write('      Serial.println("!!! HASH COLLISION FOUND !!!");\n')
    file.write('      Serial.print("Password: ");\n')
    file.write('      Serial.println(PASSWORDS[i]);\n')
    file.write("      while(1); // Halt on success\n")
    file.write("    }\n")
    file.write("    delay(100); // Short delay between hash checks\n")
    file.write("  }\n")
    file.write('  Serial.println("=== No hash collisions found ===\\n");\n\n')
    
    file.write("  // PHASE 2: Physical password attempts\n")
    file.write("  Serial.println(\"=== Starting physical password attempts ===\");\n")
    file.write("  for (int i = 0; i < NUM_PASSWORDS; i++) {\n")
    file.write('    Serial.print("Attempt [");\n')
    file.write('    Serial.print(i+1);\n')
    file.write('    Serial.print("/");\n')
    file.write('    Serial.print(NUM_PASSWORDS);\n')
    file.write('    Serial.print("]: ");\n')
    file.write('    Serial.println(PASSWORDS[i]);\n')
    file.write("    enterPassword(PASSWORDS[i]);\n")
    file.write("    delay(5000); // Wait 5 seconds between attempts\n")
    file.write("  }\n")
    file.write('  Serial.println("=== All attempts completed ===\\n");\n')
    file.write("  while(1); // Stop after completion\n")
    file.write("}\n")


print(f"\nOutput saved in {filename}")
print(f"Total passwords generated: {len(custom_guesses) + len(date_pins_2part) + len(date_pins_1part) + len(priority_pins) + len(phone_pins) + len(all_remaining_pins)}")
print(f" - Custom guesses: {len(custom_guesses)}")
print(f" - Date-based PINs: {len(date_pins_2part) + len(date_pins_1part)}")
print(f" - Repeating/sequential PINs: {len(priority_pins)}")
print(f" - Phone-based PINs: {len(phone_pins)}")
print(f" - All remaining PINs: {len(all_remaining_pins)}")