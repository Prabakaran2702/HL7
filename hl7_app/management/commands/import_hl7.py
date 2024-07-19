# hl7_app/management/commands/import_hl7.py

from datetime import datetime
import os
import sys
from django.core.management.base import BaseCommand
from hl7_app.models import Patient, ErrorCharges

class Command(BaseCommand):
    help = 'Import HL7 files and store data in the database'

    def handle(self, *args, **kwargs):
        try:
            # file_path = r'C:\Users\91824\Downloads\HL7 (1) (1)\HL7\charges_0.hl7'
            # filename = charges_0.hl7

            hl7_dir = r'C:\Users\91824\Downloads\HL7 (1) (1)\HL7' # Path to HL7 file
            for filename in os.listdir(hl7_dir):
                if filename.endswith('.hl7'):
                    file_path = os.path.join(hl7_dir, filename)

                    # Read HL7 data
                    hl7_data = self.read_hl7_file(file_path)

                    # Extract patient data
                    patient_data = self.extract_patient_data(hl7_data)
                    
                    # Store patient data
                    self.store_patient_data(patient_data)
                    self.stdout.write(self.style.SUCCESS(f'{filename} Processing complete.'))
                    sys.stdout.write('Patients data successfully stored\n')
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error: {str(e)}'))            

    def read_hl7_file(self,file_path):
        with open(file_path, 'r') as file:
            hl7_data = file.read()
        return hl7_data

    # Function to extract patient data from HL7 text
    def extract_patient_data(self,hl7_data):
        patients = []

        # Split the HL7 data into segments
        segments = hl7_data.split('\n')

        for segment in segments:
            if segment.startswith('PID'):
                # Extract fields from PID segment
                print('segment-->',segment)
                fields = segment.split('|')
                print('fields-->',fields)
                try:
                    patient_data = {
                        'mrn': fields[3].split('^')[0],  # Medical Record Number
                        'last_name': fields[5].split('^')[0],  # Last Name
                        'first_name': fields[5].split('^')[1] if len(fields[5].split('^')) > 1 else 'N/A',  # First Name
                        'date_of_birth': fields[7],  # Date of Birth
                        'physician_name':fields[24].split('^')[0],
                        'phone': fields[11].split('^')[14]  # Phone
                    }
                    patients.append(patient_data)
                except IndexError:
                    # Handle unexpected format
                    print("Error processing PID segment:", segment)
        
        return patients


    def store_patient_data(self,patient_data):
        print(patient_data)
        for entry in patient_data:
            first_name = entry.get('first_name')
            last_name = entry.get('last_name')
            date_of_birth_str = entry.get('date_of_birth')
            mrn = entry.get('mrn')
            phone = entry.get('phone')
            print(first_name,last_name, mrn, type(mrn))
            errors = []
            if not date_of_birth_str:
                errors.append('DOB not found')
            if not mrn:
                errors.append('MRN not found')
            if not first_name or not last_name:
                errors.append('Patient name not found')
        
            try:
                date_of_birth = datetime.strptime(date_of_birth_str, '%Y%m%d').date()
            except ValueError:
                date_of_birth = None
                errors.append('Invalid DOB format')
        
            if not errors:
                existing_patients = Patient.objects.filter(mrn=mrn)
                if existing_patients.exists():
                    # Handle duplicates - choose one or merge
                    for patient in existing_patients:
                        # For demonstration, we'll just print duplicates
                        print(f"Duplicate MRN found: {patient.mrn}")
                else:
                    Patient.objects.create(
                        mrn=mrn,
                        first_name=first_name,
                        last_name=last_name,
                        date_of_birth=date_of_birth,
                        phone=phone
                    )
            else:
                for error in errors:
                    ErrorCharges.objects.create(
                        error_type=error,
                        error_message=f"Missing data for patient: {first_name}{last_name}" if 'MRN not found'== error else f"Missing data for MRN: {mrn}",
                    
                    )