class Converter:
    def __init__(self):
        self.conversions = self.load_conversions()
    
    def load_conversions(self):
        return {
            "weight": {
                "mg": 1,
                "g": 1000,
                "mcg": 0.001
            },
            "volume": {
                "ml": 1,
                "l": 1000,
                "oz": 29.5735
#Confirm conversions
            },
            "medications": {
                "insulin_u100": {
                    "type": "insulin",
                    "units_per_ml": 100
                },
                "insulin_u500": {
                    "type": "insulin",
                    "units_per_ml": 500
                },
                "vitamin_d": {
                    "type": "vitamin",
                    "iu_per_mcg": 40
                }
            }  
        }
    def convert(self, num01, measurement01, measurement02, medication=None):
        measurement01 = measurement01.lower()
        measurement02 = measurement02.lower()

        med_result = self.convert_medication(
            num01, measurement01, measurement02, medication
        )
        if med_result is not None:
            return med_result
#Add medications
        for category in ["weight", "volume"]:
            if (measurement01 in self.conversions[category] and
                measurement02 in self.conversions[category]):

                base_value = num01 * self.conversions[category][measurement01]
                converted_value = base_value / self.conversions[category][measurement02]
                return converted_value
            
        return None

    def convert_medication(self, num01, measurement01, measurement02, medication):
        if not medication:
            return None

        med_key = medication.lower()
        meds = self.conversions.get("medications", {})

        if med_key not in meds:
            return None

        med_data = meds[med_key]

        if med_data["type"] == "insulin":
            units_per_ml = med_data["units_per_ml"]

            if measurement01 == "units" and measurement02 == "ml":
                return num01 / units_per_ml
            elif measurement01 == "ml" and measurement02 == "units":
                return num01 * units_per_ml
## THIS IS WHERE YOU LEFT OFF WHEN YOU HAD TO RESTART YOUR COMPUTER
        if med_data["type"] == "vitamin":
            iu_per_mcg = med_data["iu_per_mcg"]
            
            if measurement01 == "mcg" and measurement02 == "iu":
                return num01 * iu_per_mcg
            elif measurement01 == "iu" and measurement02 == "mcg":
                return num01 / iu_per_mcg

class ConversionCalculator:
    def __init__(self):
        self.converter = Converter()

    def validate_input(self, num01, measurement01, measurement02):
        try:
            num01 = float(num01)
            if num01 < 0:
                return False, "Invalid Input: Negative numbers are not allowed."
        except ValueError:
                return False, "Invalid Input: Please enter a valid number."
                
        if not measurement01 or not measurement02:
                return False, "Invalid Input: Measurement fields cannot be blank."
                
        return True, num01
            
    def calculate(self, num01, measurement01, measurement02, medication):
        is_valid, result = self.validate_input(num01, measurement01, measurement02)

        if not is_valid:
            return result
                
        converted_value = self.converter.convert(
            result, measurement01, measurement02, medication)
                
        if converted_value is None:
            return "Invalid Input: Conversion not supported."
                
        return f"Result: {converted_value:.4f} {measurement02}"
            
class User:
    def __init__(self):
        self.calculator = ConversionCalculator()
                
    def display_calcscreen(self):
        print("\n Medication Conversion Calculator")

        while True:
            num01 = input("Enter the number to convert(or 'q' to quit): ")
            if num01.lower() == 'q':
                print("Goodbye!")
                break

            measurement01 = input("Convert FROM (mg, g, mcg, ml, l, oz, units, iu): ")
            measurement02 = input("Convert TO (mg, g, mcg, ml, l, oz, units, iu): ")
        
            medication = self.select_medication()
        
#Should units be changed to insulin units?
            result = self.calculator.calculate(
                num01, measurement01, measurement02, medication
            )

            self.display_result(result)

    def select_medication(self):
        meds = self.calculator.converter.conversions.get("medications", {})

        if not meds:
            return None

        print("\nAvailable Medications:")
        for med in meds:
            display_name = med.replace("_", " ").title()
            print(f"- {display_name}")

        user_input = input(
            "Enter medication name exactly as shown (or press Enter for none): "
        ).strip().lower().replace(" ", "_")

        if user_input == "":
            return None  

        if user_input in meds:
            return user_input
        else:
            print("Invalid medication selected.")
            return None
        
    def display_result(self, result):
        print(result)

if __name__ == "__main__":
    user = User()
    user.display_calcscreen()
