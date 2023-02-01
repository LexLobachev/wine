from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from dotenv import load_dotenv

import datetime
import pandas
import os


def set_age_token(age_to):
    literate_year = 'лет'
    last_dig = age_to % 10
    if age_to in range(5, 20) or age_to == 111:
        literate_year = 'лет'
    elif 1 in (age_to, last_dig):
        literate_year = 'год'
    elif {age_to, last_dig} & {2, 3, 4}:
        literate_year = 'года'
    return literate_year


def main():
    load_dotenv()
    file_name = os.environ.get("FILE_NAME")
    sheet_name = os.environ.get("SHEET_NAME")
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    foundation_year = 1920
    dif_years = datetime.date.today().year - foundation_year

    excel_data_df = pandas.read_excel(file_name, sheet_name=sheet_name)
    all_liquids = excel_data_df.fillna('').groupby(['Категория'], sort=False) \
        .apply(lambda x: x.to_dict(orient='records')).to_dict()

    rendered_page = template.render(
        count_of_years=dif_years,
        correct_russian_year=set_age_token(dif_years),
        all_liquids=all_liquids,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
