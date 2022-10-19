# Business events

Actor: Unknown user
Action: Register
Event: UserRegistered
Data: Name, Email
CUDs: UserCreated

Actor: User
Action: AddTask
Event: TaskAdded
Data: Task ID, User ID (Assignee)
CUDs: TaskCreated

Actor: User
Action: CompleteTask
Event: TaskCompleted
Data: Task ID, Assignee ID
CUDs: TaskUpdated 

Actor: TaskCompleted
Action: IncreaseUserBudget
Event: TaskCompleted
Data: Task ID, Assignee ID
CUDs: TaskUpdated

Actor: User.WalletUpdated
CUDs: UpdateUserWalletAuditLog, UpdateCompanyAccumulatedBudget

Actor: Admin, manager
Action: ShuffleAssignees
Event: AssigneeShuffled
Data: Task ID, Assignee ID
CUDs: TaskUpdated, AccountUpdated

Actor: Scheduler
Action: CompleteBillingCycle
Event: BillingCycleCompleted
Data: -

Policy: User wallet value > 0
Actor: BillingCycleCompleted
Action: PayUser
Event: UserGotPayed
Data: User ID
CUDs: AccountUpdated

Actor: BillingCycleCompleted
Action: SendReport
Event: ReportSent
Data: User ID

# Domains 

Основные акторы, инициирующие цепочки: User, Scheduler
User - выполняет работу с задачами
Scheduler - инициирует выплаты в конце периода
Реагирующие акторы - эвенты, инициирующие работу с аккаунтингом

На основе контекстов можно выделить домены:

1. Task management - Взаимодействие с задачами, аналитика по статусам и работе пользователей
2. Accounting - Оплата и штрафы, отслеживание операций

# Services

## Users domain

### Auth service

Авторизация пользователя в системе. Выделяю так как security-sensitive данные являются драйвером изоляции сервиса

## Task management domain


### Task manager service

Принимает комманды по работе с задачами

Выдает информацию о задачах, их статусах. Read-only для быстрого отображения на интерфейсе


### Tasks analytics service

Получает данные необходимые для аналитики, записывает их в базу после фильтрации

Быстро выдает последнюю доступную аналитику


## Accounting domain

### Accounting service

Изменение баланса пользователей. Судя по эвентам будет иметь разную пропускную нагрузку с чтением, пока неясно в какую сторону. Раздельное масштабирование пока не выглядит плохой идеей.

Информация о балансе пользователей

Выполняет транзакции по кошелькам

Отправляет пользователям отчеты о заработанных деньгах за период


## Analytics domain

### Analytics service

Делает query к Wallets info и собирает нужную статистику по балансам пользователей



