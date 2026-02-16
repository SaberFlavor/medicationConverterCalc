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
                "oz": 28.3495
#Confirm conversions
            }
        }
    def convert(self, num01, measurement01, measurement02, medication=None):
        measurement01 = measurement01.lower()
        measurement02 = measurement02.lower()
#Add medications
        if medication and medication.lower() == "insulin":
            if measurement01 == "units" and measurement02 == "ml":
                return num01 / 100
            elif measurement01 == "ml" and measurement02 == "units":
                return num01 * 100
            
        for category in self.conversions:
            if (measurement01 in self.conversions[category] and
                measurement02 in self.conversions[category]):

                base_value = num01 * self.conversions[category][measurement01]
                converted_value = base_value / self.conversions[category][measurement02]
                return converted_value
            
        return None
        
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
                
        return f"Result: {round(converted_value, 4)} {measurement02}"
            
class User:
    def __init__(self):
        self.calculator = ConversionCalculator()
                
    def display_calcscreen(self):
        print("\n Medication Conversion Calculator")

        num01 = input("Enter the number to convert: ")
        measurement01 = input("Convert FROM (mg, g, mcg, ml, l, oz, units): ")
        measurement02 = input("Convert TO (mg, g, mcg, ml, l, oz, units): ")
        medication = input("Enter medication name (or press Enter if none): ")
#Should units be changed to insulin units?
        result = self.calculator.calculate(
            num01, measurement01, measurement02, medication
        )

        self.display_result(result)

    def display_result(self, result):
                    print(result)

if __name__ == "__main__":
    user = User()
    user.display_calcscreen()