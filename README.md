<div align="center">

# HHResumeRaiser

**Локальный Python-скрипт для своевременного поднятия резюме на HH.ru**

![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-1.62%2B-2EAD33?logo=playwright&logoColor=white)
![Status](https://img.shields.io/badge/status-experimental-orange)

</div>

Скрипт использует локальный профиль Chromium, определяет время следующего
доступного поднятия резюме и повторно сверяется с системными часами после
гибернации или временного отключения компьютера. При нераспознанном состоянии
страницы срабатывает настраиваемый watchdog и страница загружается заново.

> Проект находится в экспериментальной стадии. Интерфейс HH.ru может меняться.

## Установка

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m playwright install chromium
```

## Учётные данные

Создайте локальный файл `hh-credentials.ini`:

```ini
[hh]
phone = +70000000000
password = replace-me
```

Файл исключён из Git. Вместо него можно использовать переменные окружения
`HH_PHONE` и `HH_PASSWORD` либо интерактивный ввод.

## Запуск

```powershell
.\.venv\Scripts\python.exe hh_resume_raiser.py --headless --credentials-file .\hh-credentials.ini
```

Полезные параметры:

- `--resume-title` — название резюме;
- `--once` — выполнить одну проверку;
- `--dry-run` — определить состояние без нажатия кнопки;
- `--poll-seconds` — период сверки системного времени;
- `--page-refresh-seconds` — watchdog зависшего или нераспознанного состояния страницы.

Все параметры доступны через `--help`.

## Проверка

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -q
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
```

Инструмент предназначен для личного использования владельцем резюме. Не
используйте его для массового сбора данных, обхода ограничений или иных
злоупотреблений платформой.
