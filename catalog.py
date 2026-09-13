# Stable source paths and localized navigation labels. Every public guide is assigned once.
GROUPS = [
 ('start','Getting started','Начало работы',[
 ('installation','Install the panel','Установка панели'),('sections/getting-started','First setup','Первый запуск'),('sections/home','Dashboard','Главная панели')]),
 ('network','Servers & network','Серверы и сеть',[
 ('node-installation','Install a node','Установка ноды'),('sections/nodes','Manage servers','Управление серверами'),('sections/hosts','Hosts','Хосты'),('sections/squads-int','Internal squads','Внутренние сквады'),('sections/squads-ext','External squads','Внешние сквады'),('sections/nodes-metrics','Server health','Состояние серверов'),('sections/nodes-stats','Traffic history','История трафика'),('sections/node-plugins','Filters & protection','Фильтры и защита')]),
 ('config','Profiles & configurations','Профили и конфиги',[
 ('profiles','Profiles and templates','Профили и шаблоны'),('sections/profiles','Inbounds and profiles','Инбаунды и профили'),('sections/config','Xray editor','Редактор Xray'),('selfsteal','Selfsteal website','Сайт Selfsteal')]),
 ('subscriptions','Subscriptions','Подписки',[
 ('subscription-installation','Install the service','Установка сервиса'),('sections/sub-settings','Subscription settings','Настройки подписки'),('sections/subpage','Connection page','Страница подключения'),('sections/templates','DNS and routing','DNS и маршрутизация'),('sections/response-rules','Response formats','Форматы ответа'),('sections/happ-routing','Happ routing','Маршрутизация Happ')]),
 ('customers','Customers & Mini App','Клиенты и Mini App',[
 ('cabinet-installation','Install the customer site','Установка кабинета'),('sections/cabinet','Website & Mini App','Кабинет и Mini App'),('branding','Branding & languages','Брендинг и языки'),('sections/users','Customer records','Карточки клиентов'),('sections/support','Customer support','Поддержка клиентов'),('addons','Device & traffic add-ons','Докупка устройств и трафика')]),
 ('telegram','Telegram','Telegram',[
 ('sections/bot','Set up the bot','Настройка бота'),('sections/broadcasts','Broadcasts','Рассылки'),('team-notifications','Team notifications','Уведомления команды')]),
 ('billing','Plans & payments','Тарифы и оплаты',[
 ('sections/tariffs','Plans','Тарифы'),('payment-gateways','Payment integrations','Платёжные интеграции'),('sections/providers','Payment settings','Настройка оплат'),('sections/payments','Payments & refunds','Оплаты и возвраты'),('sections/promos','Promo codes','Промокоды'),('sections/partners','Referrals','Реферальная программа'),('sections/infra-billing','Hosting costs','Расходы на серверы')]),
 ('team','Team & administration','Команда и управление',[
 ('sections/team','Owner and teammates','Владелец и сотрудники'),('sections/admin-profile','Administrator profile','Профиль администратора'),('sections/settings','Panel settings','Настройки панели'),('sections/audit','Audit log','Журнал действий')]),
 ('operations','Updates & diagnostics','Обновления и диагностика',[
 ('backup-restore','Backup & restore','Резервные копии'),('troubleshooting','Troubleshooting','Решение проблем'),('sections/hwid-inspector','Customer devices','Устройства клиентов'),('sections/srh-inspector','Subscription requests','Запросы подписок'),('sections/sessions','Traffic sessions','Сессии трафика'),('sections/torrent-reports','Blocking events','События блокировки'),('sections/http-stats','Domain statistics','Статистика доменов')]),
 ('development','Development','Разработка',[
 ('releases','Builds & releases','Сборки и релизы'),('development','Architecture & development','Архитектура и разработка')]),
]
