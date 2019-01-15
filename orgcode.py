"""Scrape SIAK-NG and Digital Catalog of UI to get description for organization codes."""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

import cleanup, json, os, time, unittest


class Monolithic(unittest.TestCase):
    def _steps(self):
        for name in dir(self):
            if name.startswith("step"):
                yield name, getattr(self, name)

    def test_steps(self):
        for name, step in self._steps():
            try:
                step()
            except Exception as e:
                self.fail("{} failed ({}: {})".format(step, type(e), e))


class OCScraper(Monolithic):
    data_siak_ng = {}
    data_dialog = {"id": {}, "en": {}, "raw": {}}

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument(
            "--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) "
            "AppleWebKit/602.1.50 (KHTML, like Gecko) "
            "CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1"
        ) # Desktop seems to be throttled by Dialog UI server.
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(30)
        self.base_url = "https://academic.ui.ac.id/"
        self.verificationErrors = []

    def step1_get_data_from_siak_ng(self):
        data = {}
        driver = self.driver
        driver.get(self.base_url + "main/Authentication/")
        driver.find_element_by_name("u").clear()
        driver.find_element_by_name("u").send_keys(os.getenv("UI_USERNAME", "username"))
        driver.find_element_by_name("p").clear()
        driver.find_element_by_name("p").send_keys(os.getenv("UI_PASSWORD", "password"))
        driver.find_element_by_tag_name("form").submit()
        driver.find_element_by_link_text("Jadwal").click()
        driver.find_element_by_link_text("Jadwal Kuliah Keseluruhan").click()

        faculty_dropdown = Select(
            driver.find_element_by_xpath(
                "(.//*[normalize-space(text()) and normalize-space(.)='Fakultas'])[1]"
                "/following::select[1]"
            )
        )

        faculties = [faculty.text for faculty in faculty_dropdown.options][1:]

        for faculty in faculties:
            faculty_dropdown = Select(
                driver.find_element_by_xpath(
                    "(.//*[normalize-space(text()) and normalize-space(.)='Fakultas'])[1]"
                    "/following::select[1]"
                )
            )
            faculty_dropdown.select_by_visible_text(faculty)

            program_dropdown = Select(
                driver.find_element_by_xpath(
                    "(.//*[normalize-space(text()) and normalize-space(.)='Program Studi'])[1]"
                    "/following::select[1]"
                )
            )

            for program in program_dropdown.options[1:]:
                organization_code, program_name = program.get_attribute('value'), program.text
                i = program_name.rfind(',')
                study_program, educational_program = program_name[:i], program_name[i + 2:]

                OCScraper.data_siak_ng[organization_code] = {
                    "faculty": faculty,
                    "study_program": study_program,
                    "educational_program": educational_program
                }
        driver.get(self.base_url + 'main/Authentication/Logout')

        with open("org_code_siak.json", "w") as output:
            print(json.dumps(OCScraper.data_siak_ng, indent=2), file=output)

    def step2_get_data_from_dialog(self):
        driver = self.driver
        self.base_url = "http://dialog.ui.ac.id/id/browse/detil/"
        for code in OCScraper.data_siak_ng:
            driver.get(self.base_url + code)
            table = driver.find_element_by_id("detil")
            trows = table.find_elements_by_tag_name("tr")
            faculty = trows[0].find_element_by_class_name("isi_katalog").text.strip()
            educational_program = trows[4].find_element_by_class_name("isi_katalog").text.strip()
            study_program = trows[5].find_element_by_class_name("isi_katalog").text.strip()
            if not faculty:
                faculty = OCScraper.data_siak_ng[code]["faculty"].upper().replace("DAN", "&")
            if study_program in '()':
                study_program = OCScraper.data_siak_ng[code]["study_program"]
            if educational_program in '()':
                educational_program = OCScraper.data_siak_ng[code]["educational_program"]
            result = {
                "faculty": faculty,
                "study_program": study_program,
                "educational_program": educational_program,
            }
            OCScraper.data_dialog['raw'][code] = result
        with open("org_code_dialog.json", "w") as output:
            print(json.dumps(OCScraper.data_dialog, indent=2), file=output)

    def tearDown(self):
        cleanup.main()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
