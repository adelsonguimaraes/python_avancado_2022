from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from basic import models


@receiver(post_save, sender=models.State, dispatch_uid='create_file_state', weak=False)
def create_file_state(instance, **kwargs):
    with open('states.txt', 'a') as file:
        file.write(f'{instance.id}|{instance.name}')

# aqui vamos utilizar o pre_save, que é um gatilho que acontece antes da ação de salvar
@receiver(pre_save, sender=models.SaleItem, dispatch_uid='set_sale_price', weak=False)
def set_sale_price(instance, **kwargs):
    # setamos os preço do sale_price de sale_item com o valor de sale_price de produto
    instance.sale_price = instance.product.sale_price
    # como isso ocorre antes do save, não precisamos passar .save() pós na sequência ele irá salvar

