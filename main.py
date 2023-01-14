from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

import datetime
import pandas


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    age_token = lambda age_to: (
            (age_to in range(5, 20)) and 'лет' or
            (age_to == 111) and 'лет' or
            (1 in (age_to, (last_dig := age_to % 10))) and 'год' or
            ({age_to, last_dig} & {2, 3, 4}) and 'года' or 'лет')
    foundation_year = 1920
    dif_years = datetime.date.today().year - foundation_year

    excel_data_df = pandas.read_excel('wine3.xlsx', sheet_name='Лист1')
    all_liquids = excel_data_df.fillna('').groupby(['Категория'], sort=False) \
        .apply(lambda x: x.to_dict(orient='records')).to_dict()

    rendered_page = template.render(
        count_of_years=dif_years,
        correct_russian_year=age_token(dif_years),
        all_liquids=all_liquids,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
