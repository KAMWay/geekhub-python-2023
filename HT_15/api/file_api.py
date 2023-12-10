import csv
import logging
import os

HTTP_TIMEOUT = 15
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'


class FileApi:
    def _save_to_csv(self, data: list[dict], *, dirname, filename, is_append: bool = False):
        do_str = "appended" if is_append else "written"

        try:
            if dirname:
                self._create_dir(dirname)
            file = os.path.join(dirname, filename) if dirname else filename

            fieldnames = [str(i) for i in data[0].keys()]
            with open(file, "a" if is_append else "w", newline='', encoding='UTF-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)

                if not is_append:
                    writer.writeheader()

                [writer.writerow(i) for i in data]

            logging.info(f'successful {do_str} to {filename}')
            print(f'successful {do_str} to {filename}')
        except Exception:
            logging.error(f'invalid {do_str} to {filename}')

    def _create_dir(self, dir_name):
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

    def _remove_file(self, dir_name: str, file_name: str):
        file = os.path.join(dir_name, file_name) if dir_name else file_name
        if os.path.isfile(file):
            os.remove(file)

