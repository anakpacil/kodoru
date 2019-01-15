"""Scrape SIAK-NG to get description for organization codes."""
from selenium import webdriver
from selenium.webdriver.support.ui import Select

import json, os, unittest


class Kodoru(unittest.TestCase):
    NAME = 'kodoru'
    STRINGS = {
        "id": {
            "fac": "Fakultas",
            "maj": "Program Studi"
        },
        "en": {
            "fac": "Faculty",
            "maj": "Major"
        }
    }

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(3)
        self.base_url = "https://academic.ui.ac.id/"
        self.verificationErrors = []

    def authenticate(self):
        driver = self.driver
        driver.get(self.base_url + "main/Authentication/")
        driver.find_element_by_name("u").send_keys(os.getenv("UI_USERNAME", "username"))
        driver.find_element_by_name("p").send_keys(os.getenv("UI_PASSWORD", "password"))
        driver.find_element_by_tag_name("form").submit()

    def scrape(self, language):
        driver = self.driver
        data = {}

        def select_dropdown(selector):
            return Select(
                driver.find_element_by_xpath(
                    "(.//*[normalize-space(text()) and normalize-space(.)='{}'])[1]"
                    "/following::select[1]".format(selector)
                )
            )

        driver.get(self.base_url + "/main/Schedule/IndexOthers")
        faculty_dropdown = select_dropdown(Kodoru.STRINGS[language]["fac"])

        faculties = [faculty.text for faculty in faculty_dropdown.options][1:]

        for faculty in faculties:
            faculty_dropdown = select_dropdown(Kodoru.STRINGS[language]["fac"])
            faculty_dropdown.select_by_visible_text(faculty)
            program_dropdown = select_dropdown(Kodoru.STRINGS[language]["maj"])

            for program in program_dropdown.options[1:]:
                organization_code, program_name = program.get_attribute('value'), program.text
                i = program_name.rfind(',')
                study_program, educational_program = program_name[:i], program_name[i + 2:]

                data[organization_code] = {
                    "faculty": faculty,
                    "study_program": study_program,
                    "educational_program": educational_program
                }

        return data

    def test_get_data_from_siak_ng(self):
        data = {lang: {} for lang in Kodoru.STRINGS}
        driver = self.driver
        self.authenticate()

        for lang in data:
            driver.get(self.base_url + 'main/System/Language?lang=' + lang)
            data[lang] = self.scrape(lang)

        driver.get(self.base_url + 'main/Authentication/Logout')

        write = {Kodoru.NAME + ".json": data}
        write.update({
            Kodoru.NAME + "_" + lang + ".json": data[lang] for lang in Kodoru.STRINGS
        })
        for file_name, dic in write.items():
            with open(file_name, "w") as output:
                print(json.dumps(dic, indent=2), file=output)

    def tearDown(self):
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
