import pytest
from .emergency_room import EmergencyRoom as E


@pytest.fixture(scope="module")
def e_room():
    """class instance"""
    return E()


@pytest.fixture(scope="module")
def error():
    return "-- Examination Room -- occupied !\nCanceling next patient call."


@pytest.fixture(scope="module")
def fill_queue(e_room):
    """setup patients for ER class"""
    e_room.register_patient("Jean-Marie", 1)
    e_room.register_patient("Moi Tsai", 3)
    e_room.register_patient("Kourage TSai", 4)
    e_room.register_patient("Gérard François", 3)
    e_room.register_patient("Mie wer", 5)


@pytest.mark.parametrize("expected", [
    ("Patients in queue: 5\n" +
    "[[1, 0, 'Jean-Marie'], [3, 1, 'Moi Tsai'], "
    "[4, 2, 'Kourage TSai'], [3, 3, 'Gérard François'], "
    "[5, 4, 'Mie wer']]")
])
def test_patients_in_queue(e_room, expected):
    fill_queue(e_room)
    assert e_room.patients_in_queue() == expected


def test_next_patient(e_room):
    assert e_room.next_patient() == "Calling ... Jean-Marie"

@pytest.mark.parametrize("patient, priority, expected", [
    ("Gérard François", 2,
     "Patients in queue: 5\n" +
    "[[2, 5, 'Gérard François'], [3, 1, 'Moi Tsai'],"
    " [4, 2, 'Kourage TSai'],"
    " [5, 4, 'Mie wer'], [3, 3, '--changed--']]")
])
def test_update_patient(e_room, patient, priority, expected):
    e_room.register_patient(patient, priority)
    assert e_room.patients_in_queue() == expected


def test_examination_room_is_busy(e_room, error):
    with pytest.raises(ValueError, match=error):
        e_room.next_patient()


def test_examination_room_is_busy_1(e_room, ):
    assert e_room.is_examination_room_empty() == False


def test_checkout_patient(e_room):
    assert e_room.check_out_patient() == "Checking out: Jean-Marie"


def test_patients_in_queue_after_1_c_o(e_room):
    assert e_room.patients_in_queue() == "Patients in queue: 5\n" + \
               "[[2, 5, 'Gérard François'], [3, 1, 'Moi Tsai']," \
               " [4, 2, 'Kourage TSai']," \
               " [5, 4, 'Mie wer'], [3, 3, '--changed--']]"


def test_next_patient_2(e_room):
    assert e_room.next_patient() == "Calling ... Gérard François"


def test_patients_in_queue_after_update(e_room):
    assert e_room.patients_in_queue() == "Patients in queue: 4\n" + \
    "[[3, 1, 'Moi Tsai'], [3, 3, '--changed--'], " \
    "[4, 2, 'Kourage TSai'], [5, 4, 'Mie wer']]"


def test_checkout_patient_2(e_room):
    assert e_room.check_out_patient() == "Checking out: Gérard François"


def test_examination_room_is_busy_2(e_room, ):
    assert e_room.is_examination_room_empty() == True


def test_checked_out_2_patients(e_room):
    assert e_room.checked_out_patients() == ["Jean-Marie", "Gérard François"]


def test_all_checkouts(e_room):
    for _ in range(3):
        e_room.next_patient()
        e_room.check_out_patient()
    assert e_room.checked_out_patients() == ["Jean-Marie", "Gérard François",
                                             'Moi Tsai', "Kourage TSai", "Mie wer"]


def test_patients_in_queue_end(e_room):
    assert e_room.patients_in_queue() == "Patients in queue: 0\n[]"


def test_is_examination_room_empty_end(e_room):
    assert e_room.is_examination_room_empty() == True







