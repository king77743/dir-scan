import os
import time

r = "\033[91m"   
y = "\033[93m"   
g = "\033[92m"   
b = "\033[94m"   
res = "\033[0m"  
bold = "\033[1m"
min_size = 250
files_scanned = 0
interesting_found = 0
empty_found = 0
nothing_files = []
tags = {
    '.log': f'{b}[ЛОГИ]{res}',
    '.env': f'{r}{bold}[СЕКРЕТЫ]{res}',
    '.conf': f'{y}[КОНФИГ]{res}',
    '.config': f'{y}[КОНФИГ]{res}',
    '.sql': f'{g}[БАЗА ДАННЫХ]{res}',
    '.bak': f'{y}[БЭКАП]{res}',
    '.sh': f'{b}[СКРИПТ АВТОМАТИЗАЦИИ]{res}',
    '.py': f'{b}[PYTHON]{res}',
    '.pcap': f'{y}[WIRESHARK ТРАФИК]{res}'
}
print(f"{g}="*60)
print(f"{bold}🔍 FILE-AUDIT v2.0: СИСТЕМА ГЛУБОКОГО АНАЛИЗА{res}")
print(f"{g}="*60 + f"{res}")
try:
    path_to_scan = input("📂 Введите путь для сканирования: ")
    if os.path.exists(path_to_scan):
        print(f"\n{y}[!] Запуск сканирования: {os.path.abspath(path_to_scan)}{res}")
        print("-" * 60)
        for root, dirs, files in os.walk(path_to_scan):
            for name in files:
                files_scanned += 1
                result = os.path.join(root, name)
                try:
                    ext = os.path.splitext(name)[1].lower()
                    ves = os.path.getsize(result)
                    tim = time.ctime(os.path.getmtime(result))
                    icon = "📄"
                    header = name                   
                    if ext in tags:
                        interesting_found += 1
                        icon = tags[ext]
                        header = f"{bold}{name}{res}"
                    status_line = f"{g}{ves} байт{res}"
                    if ves == 0:
                        empty_found += 1
                        nothing_files.append(result)
                        status_line = f"{r}КРИТИЧЕСКИ: ПУСТО (0 байт){res}"
                    elif ext == '.log' and ves < min_size:
                        status_line = f"{y}ПОДОЗРИТЕЛЬНО МАЛ ({ves} байт){res}"
                    print(f"{icon} {header}")
                    print(f"   ├─ Изменен: {tim}")
                    print(f"   ├─ Статус:  {status_line}")
                    print(f"   └─ Путь:    {result}")
                    print("-" * 40)
                except (PermissionError, FileNotFoundError) as e:
                    print(f"{r}🚫 [ОШИБКА ДОСТУПА]: {name}{res}")
        print(f"\n{g}" + "="*60)
        print(f"{bold}📊 ИТОГИ АУДИТА{res}")
        print(f"{g}" + "="*60 + f"{res}")
        print(f"✅ Проверено объектов:    {files_scanned}")
        print(f"📂 Найдено важных типов:  {interesting_found}")
        print(f"💀 Пустых файлов:         {r if empty_found > 0 else g}{empty_found}{res}")
        if nothing_files:
            print(f"\n{y}Список пустых объектов:{res}")
            for f in nothing_files:
                print(f"  {r}»{res} {f}")
        print(f"{g}="*60 + f"{res}")
    else:
        print(f"{r}❌ ОШИБКА: Путь '{path_to_scan}' не найден.{res}")
except KeyboardInterrupt:
    print(f"\n\n{r}[!] Сканирование прервано пользователем.{res}")