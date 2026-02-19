# Medication Conversion Calculator
from medications import MEDICATIONS


class Converter:
    def __init__(self):
        self.conversions = self.load_conversions()
        self.medications = MEDICATIONS

    def load_conversions(self):
        # This returns the standard weight and volume conversions.
        return {
            "weight": {"mg": 1, "g": 1000, "mcg": 0.001},
            "volume": {"ml": 1, "l": 1000, "oz": 29.5735},
        }

    def convert(self, dose_amount, from_unit, to_unit, medication=None):
        # Converts the dose_amount from one unit to another.
        from_unit = from_unit.lower()
        to_unit = to_unit.lower()

        med_result = self.convert_medication(
            dose_amount, from_unit, to_unit, medication
        )
        if med_result is not None:
            return med_result

        for category in ["weight", "volume"]:
            if (
                from_unit in self.conversions[category]
                and to_unit in self.conversions[category]
            ):

                base_amount = dose_amount * self.conversions[category][from_unit]
                converted_amount = base_amount / self.conversions[category][to_unit]
                return converted_amount

        return None

    def convert_medication(self, dose_amount, from_unit, to_unit, medication):
        # Converts a dose for a specific medication.
        if not medication:
            return None

        medication_key = medication.lower()

        if medication_key not in self.medications:
            return None

        medication_data = self.medications[medication_key]

        if medication_data["type"] == "insulin":
            units_per_ml = medication_data["units_per_ml"]

            if from_unit == "units" and to_unit == "ml":
                return dose_amount / units_per_ml
            elif from_unit == "ml" and to_unit == "units":
                return dose_amount * units_per_ml

        if medication_data["type"] == "vitamin":
            iu_per_mcg = medication_data["iu_per_mcg"]

            if from_unit == "mcg" and to_unit == "iu":
                return dose_amount * iu_per_mcg
            elif from_unit == "iu" and to_unit == "mcg":
                return dose_amount / iu_per_mcg

        return None


class ConversionCalculator:
    def __init__(self):
        self.converter = Converter()

    def validate_input(self, dose_amount, from_unit, to_unit):
        dose_amount = dose_amount.strip()
        from_unit = from_unit.strip()
        to_unit = to_unit.strip()
        # Makes sure that the dose_amount is valid.
        
        if not dose_amount:
            return False, "Invalid Input: Dose amount cannot be blank."
        if not from_unit or not to_unit:
            return False, "Invalid Input: Measurement fields cannot be blank."
        
        try:
            dose_amount = float(dose_amount)
            if dose_amount < 0:
                return False, "Invalid Input: Negative numbers are not allowed."
        except ValueError:
            return False, "Invalid Input: Please enter a valid number."

        return True, dose_amount

    def calculate(self, dose_amount, from_unit, to_unit, medication):
        # Makes sure the input is valid and performs the conversion.
        is_valid, result = self.validate_input(dose_amount, from_unit, to_unit)

        if not is_valid:
            return result

        converted_value = self.converter.convert(result, from_unit, to_unit, medication)

        if converted_value is None:
            return "Invalid Input: Conversion not supported or impossible."

        return f"Result: {converted_value:.4f} {to_unit}"


class User:
    def __init__(self):
        self.calculator = ConversionCalculator()

    def display_calcscreen(self):
        # Promts user for dose_amount, from_unit, to_unit, and medication. Continues unless the user quits.
        print("\nMedication Conversion Calculator")

        while True:
            dose_amount = input("Enter the number to convert(or 'q' to quit): ")
            if dose_amount.lower() == "q":
                print("Goodbye!")
                break

            from_unit = input("Convert FROM (mg, g, mcg, ml, l, oz, units, iu): ")
            to_unit = input("Convert TO (mg, g, mcg, ml, l, oz, units, iu): ")

            medication = self.select_medication()

            result = self.calculator.calculate(
                dose_amount, from_unit, to_unit, medication
            )

            self.display_result(result)

    def select_medication(self):
        # Lists available medications and prompts the user to select one. Returns selected medication or None if the user only pushes enter.
        meds = self.calculator.converter.medications

        if not meds:
            return None

        print("\nAvailable Medications:")
        for med in meds:
            display_name = med.replace("_", " ").title()
            print(f"- {display_name}")

        user_input = (
            input("Enter medication name exactly as shown (or press Enter for none): ")
            .strip()
            .lower()
            .replace(" ", "_")
        )

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
