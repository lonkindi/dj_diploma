# Дипломный проект по курсу «Django: создание функциональных веб-приложений»

Сайт интернет-магазина.
Позволяет владельцу создать электронную витрину, наполнять её различными товарами, разделёнными по категориям.
Просматривать и редактировать заказы и отзывы посетителей магазина.
Создавать, редактировать и удалять пользователей магазина.
Пользователи магазина могут "складывать" товары в корзину и делать заказы (для этого требуется авторизация).
Могут оставлять отзывы о товарах.


## Инструкция по установке и первому запуску

* Создать приложение django `django-admin startproject <имя проекта>`
* Скопировать файлы в рабочую директорию проекта.
* В директории проекта запустить миграции для создания базы данных `manage.py migrate`
* Заполнить базу данных тестовыми данными из файла `manage.py loaddata fixtures.json`


Вход в административный интерфейс проекта можно осуществить под учётной записью администратора
* логин: admin@mail.ru (или просто admin)
* пароль: admin

### **Не забудьте сменить пароль администратора!**
    
