"""Cleanup the data obtained through scraping using orgcode.py."""
import json


FACULTIES = {
    "id" : {
        "01.01": "Kedokteran",
        "02.01": "Kedokteran Gigi",
        "03.01": "Matematika dan Ilmu Pengetahuan Alam",
        "04.01": "Teknik",
        "05.01": "Hukum",
        "06.01": "Ekonomi dan Bisnis",
        "07.01": "Ilmu Pengetahuan Budaya",
        "08.01": "Psikologi",
        "09.01": "Ilmu Sosial dan Ilmu Politik",
        "10.01": "Kesehatan Masyarakat",
        "12.01": "Ilmu Komputer",
        "13.01": "Ilmu Keperawatan",
        "14.01": "Pascasarjana",
        "15.01": "Pendidikan Vokasi",
        "17.01": "Farmasi",
        "18.01": "Ilmu Administrasi",
        "19.01": "Ilmu Lingkungan",
        "20.01": "Kajian Strategis dan Global"
    },
    "en": {
        "01.01": "Medicine",
        "02.01": "Dentistry",
        "03.01": "Mathematics and Natural Science",
        "04.01": "Engineering",
        "05.01": "Law",
        "06.01": "Economics and Business",
        "07.01": "Humanities",
        "08.01": "Psychology",
        "09.01": "Social and Political Sciences",
        "10.01": "Public Health",
        "12.01": "Computer Science",
        "13.01": "Nursing",
        "14.01": "Graduate School",
        "15.01": "Vocational Education",
        "17.01": "Pharmacy",
        "18.01": "Administration Science",
        "19.01": "Environmental Science",
        "20.01": "Strategic and Global Studies",
    }
}

def main():
    new_data = {"id": {}, "en": {}, "raw": {}}
    with open("org_code_dialog.json") as file:
        data = json.load(file)

    new_data["raw"] = data["raw"].copy()
    new_data["en"] = data["raw"].copy()

    for code in data["raw"]:
        faculty, study_program, educational_program = data["raw"][code].values()
        educational_program = educational_program.replace("Kls", "Kelas")
        new_data["id"][code] = {"faculty": FACULTIES["id"][code[-5:]]}
        new_data["en"][code] = {"faculty": FACULTIES["en"][code[-5:]]}

        each = {"study_program": study_program, "educational_program": educational_program}
        for key, value in each.items():
            start, stop = value.rfind("("), value.rfind(")")
            value_id = value[:start - 1] if start != -1 else value
            value_en = (value[start + 1:stop] if start != -1 else '') or value_id

            new_data["id"][code][key] = value_id
            new_data["en"][code][key] = value_en

    with open("org_code.json", "w") as file:
        print(json.dumps(new_data, indent=2), file=file)


if __name__ == '__main__':
    main()
