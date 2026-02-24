import os
import time
r = "\033[91m"   
y = "\033[93m"   
g = "\033[92m"   
res = "\033[0m"  
min_size = 250
files_scanned = 0
logs_found = 0
suspicious_found = 0

print(f"{g}="*50)
print(f"🔍 DIR-SCANER v1.0: СИСТЕМА АУДИТА БЕЗОПАСНОСТИ")
print(f"="*50 + f"{res}")
try:
    fil = input("📂 Введите путь для сканирования: ")

    print(f"\n{y}[!] Начинаю сканирование: {os.path.abspath(fil)}{res}")

    print("-" * 50)

    if os.path.exists(fil):
        for root, dirs, files in os.walk(fil):
            for name in files:
                files_scanned += 1
                result = os.path.join(root, name)
                try:
                    is_log = name.lower().endswith(".log")
                    ves = os.path.getsize(result)
                    tim = time.ctime(os.path.getmtime(result))
                    icon = "📄"
                    color = ""               
                    if is_log:
                        logs_found += 1
                        if ves == 0:
                            icon = f"{r}💀 [КРИТИЧЕСКИ: ПУСТО]{res}"
                            color = r
                            suspicious_found += 1
                        elif ves < min_size:
                            icon = f"{y}⚠️ [ПОДОЗРИТЕЛЬНО: МАЛ]{res}"
                            color = y
                            suspicious_found += 1
                        else:
                            icon = f"{g}✅ [Чисто]{res}"
                            color = g                
                    print(f"{icon} {color}{name}{res}")
                    print(f"   ├─ Размер: {ves} байт")
                    print(f"   ├─ Изменен: {tim}")
                    print(f"   └─ Путь: {result}")
                    print("-" * 30)
                except PermissionError:
                    print(f"{r}🚫 [ОШИБКА ДОСТУПА]: {name}{res}")
                except FileNotFoundError:
                    print(f"{y}❓ [ИЗЧЕЗ]: {name}{res}")

        print(f"\n{g}" + "="*50)
        print("📊 ИТОГИ СКАНИРОВАНИЯ")
        print("="*50 + f"{res}")
        print(f"✅ Всего проверено файлов: {files_scanned}")
        print(f"📝 Найдено лог-файлов:     {logs_found}")
        print(f"{r if suspicious_found > 0 else g}🚨 Подозрительных логов:   {suspicious_found}{res}")
        print(f"{g}="*50 + f"{res}")
    else:
        print(f"{r}❌ ОШИБКА: Путь '{fil}' не найден.{res}")
except (KeyboardInterrupt,NameError):
    print(f"\n{y}[!]{res} Остановлено")
