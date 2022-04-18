from time import sleep

from basic import models, helpers


class SalaActions:
    @staticmethod
    def sale_by_year():
        results = models.Sale.objects.by_year()
        counter = results.count()
        results = map(lambda item: f"{item['year']}, {item['month']}, {item['total']}\n", results)
        with open('sale_by_year.txt', 'a') as file:
            for index, row in enumerate(results):
                file.write(row)
                percentage = (index / counter) * 100
                helpers.send_channel_message('chat', {'message': round(percentage, 2)})
                sleep(0.1)
