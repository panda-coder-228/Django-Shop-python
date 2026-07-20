from .models import Warehouse, StockIssue, Stock, StockReceipt
from django.db import transaction
from django.db.models import F


class WarehouseService:

    @staticmethod
    def create(**data):
        return Warehouse.objects.create(**data)

    @staticmethod
    def update(warehouse, **data):
        for field, value in data.items():
            setattr(warehouse, field, value)
        warehouse.save()
        return warehouse

    @staticmethod
    def delete(warehouse):
    # """Мягкое удаление склада"""
        warehouse.is_delete = True  # нужно добавить поле в модель
        warehouse.is_active = False
        warehouse.save(update_fields=["is_delete", "is_active"])
        return  warehouse
    
    @staticmethod
    def hard_delete(warehouse):
    # """Полное удаление (использовать осторожно)"""
        warehouse.delete()

    @staticmethod
    def activate(warehouse):
    # """Активация склада"""
        if warehouse.is_active:
            return warehouse  # Уже активен
        warehouse.is_active = True
        warehouse.save(update_fields=["is_active"])
        return warehouse

    @staticmethod
    def deactivate(warehouse):
        # """Деактивация склада"""
        if not warehouse.is_active:
            return warehouse  # Уже неактивен
    
        # Проверка, есть ли товар на складе
        if Stock.objects.filter(warehouse=warehouse, quantity__gt=0).exists():
            raise ValueError("Нельзя деактивировать склад с товаром")
    
        warehouse.is_active = False
        warehouse.save(update_fields=["is_active"])
        return warehouse
    

class StockService:
    @staticmethod
    def get_or_create_stock(warehouse, product):
        """
        Получить или создать запись о товаре на складе
        
        Returns:
            tuple: (stock, created) - запись и флаг, была ли она создана
        """
        if not warehouse or not product:
            raise ValueError("Склад и товар обязательны")
        
        if not warehouse.is_active:
            raise ValueError(f"Склад '{warehouse.title}' неактивен")
        
        stock, created = Stock.objects.get_or_create(
            warehouse=warehouse,
            product=product,
            defaults={"quantity": 0},
        )
        
        # Логируем создание новой записи
        if created:
            import logging
            logger = logging.getLogger("warehouse")
            logger.info(
                f"Создана новая запись склада: "
                f"Склад={warehouse.title}, Товар={product.title}"
            )
        
        return stock, created



class StockReceiptService:

    @staticmethod
    @transaction.atomic
    def create(warehouse, product, quantity, supplier="", comment=""):
        """
        Создание прихода товара на склад
        """
        # Валидация
        if quantity <= 0:
            raise ValueError("Кількість повинна бути більше 0")
        
        if not warehouse:
            raise ValueError("Склад обязателен")
        
        if not product:
            raise ValueError("Товар обязателен")
        
        if not warehouse.is_active:
            raise ValueError("Склад неактивний")
        
        # Получаем или создаем запись СРАЗУ с блокировкой
        stock = Stock.objects.select_for_update().get_or_create(
            warehouse=warehouse,
            product=product,
            defaults={"quantity": 0},  # Правильно: начальное количество 0
        )[0]
        
        # Создаем документ прихода
        receipt = StockReceipt.objects.create(
            warehouse=warehouse,
            product=product,
            quantity=quantity,
            supplier=supplier,
            comment=comment,
        )
        
        # Обновляем количество с использованием F()
        stock.quantity = F("quantity") + quantity
        stock.save(update_fields=["quantity"])
        
        # Обновляем объект из базы
        stock.refresh_from_db()
        
        return receipt

class StockIssueService:

    @staticmethod
    @transaction.atomic
    def create(
        warehouse,
        product,
        quantity,
        reason,
        comment="",
    ):
        
        # 1. Проверка что количество больше 0
        if quantity <= 0:
            raise ValueError("Кількість повинна бути більше 0.")
        
        # 2. Проверка что причина указана
        if not reason or not reason.strip():
            raise ValueError("Причина списання обов'язкова.")
        
        # 3. Проверка что склад активен
        if not warehouse.is_active:
            raise ValueError("Склад неактивний.")
        
        # 4. Обработка случая когда товара нет на складе
        try:
            stock = Stock.objects.select_for_update().get(
                warehouse=warehouse,
                product=product,
            )
        except Stock.DoesNotExist:
            raise ValueError("Товар не знайдено на складі.")

        # 5. Проверка наличия товара
        if stock.quantity < quantity:
            raise ValueError(
                f"Недостатньо товару на складі. "
                f"На складі: {stock.quantity}, потрібно: {quantity}"
            )

        # 6. Создание расхода
        issue = StockIssue.objects.create(
            warehouse=warehouse,
            product=product,
            quantity=quantity,
            reason=reason,
            comment=comment,
        )

        # 7. Обновление количества
        stock.quantity = F("quantity") - quantity
        stock.save(update_fields=["quantity"])

        stock.refresh_from_db()

        return issue