import heapq
from itertools import count


class EmergencyRoom:

    def __init__(self):
        self.in_patients = []
        self.in_treatment = []
        self._out_patients = []
        self._patient_list = {}
        self.updated_condition = "--changed--"
        self.counter = count()

    def __len__(self):
        return len(self.in_patients)

    def numbers_of_patients(self):
        return len(self.in_patients)

    def register_patient(self, patient, priority=0):
        """register or update patient with priority """
        if patient in self._patient_list:
            self.update_patient_condition(patient)
        count = next(self.counter)
        entry = [priority, count, patient]
        self._patient_list[patient] = entry
        heapq.heappush(self.in_patients, entry)

    def update_patient_condition(self, patient):
        """update patient priority condition"""
        entry = self._patient_list.pop(patient)
        entry[-1] = self.updated_condition

    def _next_patient(self):
        """return patient with minimum priority"""
        while self.in_patients:
            priority, count, patient = heapq.heappop(self.in_patients)
            if patient is not self.updated_condition:
                del self._patient_list[patient]
                return patient
        raise ValueError("There are no awaiting patients.")

    def next_patient(self):
        """send next patient to examination room"""
        if not self.in_treatment:
            patient = self._next_patient()
            self.in_treatment.append(patient)
            return self.call_patient(patient)
        else:
            raise ValueError("-- Examination Room -- occupied !" 
               "\nCanceling next patient call.")

    def call_patient(self, patient):
        return "Calling ... {}".format(patient)

    def patients_in_queue(self):
        """return number and patient names in queue"""
        return "Patients in queue: {}\n{}".\
            format(self.numbers_of_patients(), self.in_patients)

    def check_out_patient(self):
        """remove patient from queue"""
        if self.in_treatment:
            self._out_patients.append(self.in_treatment.pop())
            return "Checking out: {}".format(self._out_patients[-1])
        return "No patients in Examination room."

    def checked_out_patients(self):
        """list of checked out patients"""
        return self._out_patients

    def is_examination_room_empty(self):
        """return if examination room is empty"""
        return self.in_treatment == []

