# Business events

Actor: Unknown user
Action: Sign Up
Event: User.SignedUp
Data: Name, Email
CUDs: CreateNewWallet -> CreateNewUser

Actor: User
Action: CreateNewTask
Event: Task.Created
Data: Task ID, User ID (Assignee)
CUDs: CreateNewTask

Actor: User
Action: CompleteTask
Event: Task.Completed
Data: Task ID, Assignee ID
CUDs: UpdateMaxTaskPrice, UpdateTaskStatus

Actor: Task.Completed
Action: IncreaseUserBudget
Event: User.WalletUpdated
Data: Wallet ID
CUDs: UpdateUserWalletValue 

Actor: User.WalletUpdated
CUDs: UpdateUserWalletAuditLog, UpdateCompanyAccumulatedBudget

Actor: Admin, manager
Action: AssignTasks
Event: Task.AssigneeChanged
Data: Task ID, Assignee ID
CUDs: UpdateTaskAssignee

Actor: Task.AssigneeChanged
Action: DecreaseBudget
Event: User.WalletUpdated
Data: Wallet ID

Actor: Scheduler
Action: CompleteBillingCycle
Event: User.BillingCycleCompleted
Data: User
CUDs: UpdateNegativeBalanceStats

Policy: User wallet value > 0
Actor: User.BillingCycleCompleted
Action: PayUser
Event: User.PaymentSent, User.WalletUpdated
Data: Wallet ID, Wallet Value
CUDs: ResetUserWallet

Actor: User.BillingCycleCompleted
Action: SendReport
Event: User.ReportSent

# Domains 

Основные акторы, инициирующие цепочки: User, Scheduler
User - выполняет работу с задачами
Scheduler - инициирует выплаты в конце периода
Реагирующие акторы - эвенты, инициирующие работу с аккаунтингом

На основе контекстов можно выделить домены:

1. Task management - Взаимодействие с задачами, аналитика по статусам и работе пользователей
2. Accounting - Оплата и штрафы, отслеживание операций

# Services

## Task management domain

### Auth

Авторизация пользователя в системе. Выделяю так как security-sensitive данные являются драйвером изоляции сервиса

### Task manager

Принимает комманды по работе с задачами

### Task board

Выдает информацию о задачах, их статусах. Read-only для быстрого отображения на интерфейсе

NOTE: Возможно наоборот уменьшится responsiveness на запросы пользователя на интерфейсе

### Tasks analytics updater

Write-only

Получает данные необходимые для аналитики, записывает их в базу после фильтрации


### Tasks analytics reader

Read-only

Быстро выдает последнюю доступную аналитику

## Accounting domain


### Wallets manager

Write-only

Изменение баланса пользователей. Судя по эвентам будет иметь разную пропускную нагрузку с чтением, пока неясно в какую сторону. Раздельное масштабирование пока не выглядит плохой идеей.


### Wallets info

Read-only

Информация о балансе пользователей


### Accounting analytics reader

Делает query к Wallets info и собирает нужную статистику по балансам пользователей


### Payment service

Выполняет транзакции по кошелькам


### Reports sender

Отправляет пользователям отчеты о заработанных деньгах за период


