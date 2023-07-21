# Трекер заданий

Task-Tracker - это простое приложение для отслеживания времени выполнения задач. При помощи Task-Tracker вы можете легко отслеживать, сколько времени вы затрачиваете на различные задачи, и сохранять эту информацию для дальнейшего анализа.

### Установка и запуск

Для установки Task-Tracker выполните следующие шаги:

- Склонируйте репозиторий:

```bash
git clone https://github.com/romanpittchai/Task-Tracker.git
```

- Перейдите в директорию проекта:

```bash
cd Task-Tracker
```

- Установите зависимости:

```bash
pip install -r requirements.txt
```

- Запустите приложение:

```bash
python app.py
```

### Использование

После запуска приложения откроется главное окно Task-Tracker. Здесь вы можете:

    Начать отслеживать время задачи:
        Нажмите на кнопку "Open" для открытия окна отслеживания времени.
        Введите название задачи в поле ввода "Task Name".
        Нажмите кнопку "Run" для запуска таймера.
        Таймер начнет отсчет времени выполнения задачи.

    Поставить таймер на паузу:
        Во время выполнения задачи нажмите кнопку "Pause".
        Таймер остановится, и текущее время выполнения будет сохранено.
        Нажмите кнопку "Pause" снова, чтобы возобновить таймер.

    Остановить и сохранить время задачи:
        Введите дополнительные заметки о задаче, если необходимо.
        Когда задача выполнена, нажмите кнопку "Stop/Write DB".
        Это необходимо для остановки таймера и сохранения записи в базу данных.

### База данных

Task-Tracker использует SQLite базу данных для хранения информации о выполненных задачах. Файл базы данных `TaskTimerDB.db` будет автоматически создан при запуске приложения, если его еще нет.

### Зависимости

Task-Tracker использует следующие зависимости:

    Peewee - для работы с базой данных SQLite.
    GTK+3 - для графического интерфейса приложения.
    Остальные зависимости можно увидеть в файле requirements.txt

### Лицензия

Трекер заданий распространяется под лицензией MIT. 


# Task-Tracker

Task-Tracker is a simple application for tracking task completion time. With Task-Tracker, you can easily track how much time you spend on various tasks and save this information for further analysis.

### Installation and launch

Follow these steps to install Task-Tracker:

- Clone the repository:

```bash
git clone https://github.com/romanpittchai/Task-Tracker.git
```

- Change to the project directory:

```bash
cd Task Tracker
```

- Install dependencies:

```bash
pip install -r requirements.txt
```

- Run the application:

```bash
python app.py
```

### Usage

After launching the application, the main Task-Tracker window will open. Here you can:

     Start tracking task time:
         Click the "Open" button to open the time tracking window.
         Enter the name of the task in the "Task Name" input field.
         Press the "Run" button to start the timer.
         The timer will start counting down the task completion time.

     Pause the timer:
         While the task is running, press the "Pause" button.
         The timer will stop and the current execution time will be saved.
         Press the "Pause" button again to resume the timer.

     Stop and save task time:
         Enter additional notes about the task, if necessary.
         When the task is done, click the "Stop/Write DB" button.
         This is necessary to stop the timer and save the entry to the database.

### Database

Task-Tracker uses a SQLite database to store information about completed tasks. The database file `TaskTimerDB.db` will be automatically created on application startup if it does not already exist.

### Dependencies

Task-Tracker uses the following dependencies:

     Peewee - for working with a SQLite database.
     GTK+3 - for the graphical interface of the application.
     Other dependencies can be seen in the requirements.txt file

### License

Task-Tracker is distributed under the MIT license.