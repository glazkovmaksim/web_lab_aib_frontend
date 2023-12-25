from base import BaseXlsBlock
from datetime import datetime
from collections import defaultdict

class HeaderBlock(BaseXlsBlock):
    NAME = "Описание выгрузки"
    DATE = "Дата выгрузки"
    PERIOD = "Период за который сделана выгрузка"

    def write_header(self):
        header_format = self.workbook.add_format({'bold': True, 'bg_color': '#00FF00'})  # Green background color

        self.worksheet.write(self.row, self.col, self.NAME, header_format)
        self.row += 1
        self.worksheet.write(self.row, self.col, self.DATE, header_format)
        self.row += 1
        self.worksheet.write(self.row, self.col, self.PERIOD, header_format)
        self.row -= 1
        self.col += 1

    def write_data(self):
        date_now = datetime.now().strftime('%d.%m.%Y')
        self.worksheet.write(self.row, self.col, date_now)

        self.row += 1
        dates = [payment['created_at'] for payment in self.data['payments']]
        dates = [datetime.fromisoformat(date[:-1]) for date in dates]
        dates.sort()
        date_low_str = dates[0].strftime('%d.%m.%Y')
        date_upp_str = dates[-1].strftime('%d.%m.%Y')
        period = f'{date_low_str} - {date_upp_str}'
        self.worksheet.write(self.row, self.col, period)

        self.col = 0
        self.row += 2
class PayersBlock(BaseXlsBlock):
    NAME = "Отчёт по активным клиентам"

    def write_header(self):
        header_format = self.workbook.add_format({'bold': True, 'bg_color': '#00FF00'})  # Green background color

        self.row = 4
        self.col = 0
        self.worksheet.write(self.row, self.col, self.NAME, header_format)
    def write_data(self):
        self.row += 1
        self.col += 1
        clients_payments = []
        for client in self.data['clients']:
            for payment in self.data['payments']:
                if client['id'] == payment['client_id']:
                    clients_payments.append({
                        'fio': client['fio'],
                        'payment_amount': payment['amount'],
                        'payment_created_at': payment['created_at']
                    })

        clients_payments.sort(key=lambda x: datetime.fromisoformat(x['payment_created_at']), reverse=True)

        quarters = {}
        for client_payment in clients_payments:
            payment_date = datetime.fromisoformat(client_payment['payment_created_at'])
            q = f'Q{(payment_date.month % 4 + 1)} {payment_date.year}'
            quarters.setdefault(q, []).append({
                'fio': client_payment['fio'],
                'payment_amount': client_payment['payment_amount']
            })

        for q in quarters:
            self.worksheet.write(self.row, self.col, q)
            srt = sorted(quarters[q], key=lambda x: x['payment_amount'])[:10]
            for s in srt:
                self.row += 1
                self.worksheet.write(self.row, self.col, s['fio'])
            self.row -= 10
            self.col += 1
class CitiesBlock(BaseXlsBlock):
    NAME = "География клиентов"

    def write_header(self):
        header_format = self.workbook.add_format({'bold': True, 'bg_color': '#00FF00'})  # Green background color

        self.col = 0
        self.row = 19
        self.worksheet.write(self.row, self.col, self.NAME, header_format)
    def write_data(self):
        self.row += 1
        self.col += 1
        clients = self.data['clients']

        city_counts = {}
        for client in clients:
            city = client['city']
            city_counts[city] = city_counts.get(city, 0) + 1

        top_cities = sorted(city_counts.items(), key=lambda x: x[1], reverse=True)[:10]

        for i, (city, count) in enumerate(top_cities, start=1):
            self.worksheet.write(self.row + i - 1, self.col, f"{i}. {city}")
            self.worksheet.write(self.row + i - 1, self.col + 1, f"{count}")


class BankAccountBlock(BaseXlsBlock):
    NAME = "Анализ состояния счёта"
    def write_header(self):
        header_format = self.workbook.add_format({'bold': True, 'bg_color': '#00FF00'})  # Green background color

        self.col = 0
        self.row = 34
        self.worksheet.write(self.row, self.col, self.NAME, header_format)
    def write_data(self):
        self.col = 1
        self.row = 35
        clients = self.data['clients']
        payments = self.data['payments']

        account_balances = {}
        for payment in payments:
            client_id = payment['client_id']
            amount = payment['amount']
            account_balances[client_id] = account_balances.get(client_id, 0) + amount

        top_balances = sorted(account_balances.items(), key=lambda x: x[1], reverse=True)[:10]
        self.col = 1
        self.row = 35
        for i, (client_id, balance) in enumerate(top_balances, start=1):
            client_info = next(client for client in clients if client['id'] == client_id)
            fio = client_info['fio']
            self.worksheet.write(self.row + i - 1, self.col, f"{i}. {fio}")
            self.worksheet.write(self.row + i - 1, self.col + 1, f"{balance}")

        bottom_balances = sorted(account_balances.items(), key=lambda x: x[1])[:10]
        self.col = 3
        self.row = 35
        for i, (client_id, balance) in enumerate(bottom_balances, start=1):
            client_info = next(client for client in clients if client['id'] == client_id)
            fio = client_info['fio']
            self.worksheet.write(self.row + i - 1, self.col, f"{i}. {fio}")
            self.worksheet.write(self.row + i - 1, self.col + 1, f"{balance}")