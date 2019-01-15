# kodoru

## Kode Organisasi UI

***Web scraper*** Python yang mengeruk data dari [SIAK-NG][siak-ng]
untuk mendapatkan deskripsi tentang kode organisasi yang ada di
Universitas Indonesia (UI).

Dikembangkan menggunakan Selenium dengan bantuan [Katalon Recorder][katalon].

Deskripsi kode organisasi dibangun dalam format JSON dengan bentuk
seperti berikut.

```json
"xx.xx.xx.xx": {
    "faculty": "Fakultas",
    "study_program": "Program Studi",
    "educational_program": "Program Pendidikan"
}
```

### Cara pakai

- Pastikan Anda sudah menginstal [`selenium`][selenium] untuk Python
  beserta [ChromeDriver][chromedriver].
- Atur *environment variable* `UI_USERNAME` dan `UI_PASSWORD` sesuai
  dengan nama pengguna dan kata sandi akun UI Anda, atau ubah
  `username` dan `password` yang ada di dalam [`orgcode.py`][orgcode].

- Jalankan perintah berikut di terminal atau *command prompt*.

```shell
$ python orgcode.py
```

- Tunggu hingga selesai dan hasil akan muncul berupa tiga berkas berikut.
    - `org_code_id.json`: Kode organisasi dalam bahasa Indonesia.
    - `org_code_en.json`: Kode organisasi dalam bahasa Inggris.
    - `org_code.json`: Gabungan kedua berkas di atas.

Jika Anda hanya tertarik pada data hasilnya, silakan lihat direktori
[`dump`][dump].

### Kontributor

- [laymonage][laymonage]

[siak-ng]: https://academic.ui.ac.id
[katalon]: https://chrome.google.com/webstore/detail/katalon-recorder-selenium/ljdobmomdgdljniojadhoplhkpialdid
[selenium]: https://pypi.org/project/selenium
[chromedriver]: http://chromedriver.chromium.org
[orgcode]: orgcode.py#L44
[dump]: dump/
[laymonage]: https://github.com/laymonage
