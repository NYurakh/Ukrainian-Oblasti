import turtle
import pandas as pd

#TODO: Виправив координати для більш коректного відображення

# --- Налаштування екрану ---
screen = turtle.Screen()
screen.title("Ukrainian Oblasti Game")
image = "Ukraine.gif"
# Перевірка, чи файл існує, перед додаванням форми
try:
    screen.addshape(image)
    turtle.shape(image)
except turtle.TurtleGraphicsError:
    print(f"Помилка: Не вдалося завантажити зображення '{image}'. Перевірте шлях.")
    # Можна або завершити програму, або продовжити без фонового зображення
    # exit() # Варіант завершення
    pass # Варіант продовження без фону

screen.setup(width=1200, height=800) # Налаштуйте за потребою

# --- Завантажуємо дані ---
try:
    data = pd.read_csv("Ukraine_Oblast_Centroids.csv")
except FileNotFoundError:
    print("Помилка: Файл 'Ukraine_Oblast_Centroids.csv' не знайдено!")
    exit() # Завершуємо програму, якщо дані відсутні

all_oblasts = data.Oblast.to_list()
guessed_oblasts = []

TARGET = len(all_oblasts)

while len(guessed_oblasts) < TARGET:
    corrects = len(guessed_oblasts)
    # Використовуємо українську мову для запиту
    ans_raw = screen.textinput(
        title=f"{corrects}/{TARGET} Вгадано",
        prompt="Введіть назву області або міста (Київ/Севастополь)\n(або 'Вихід' для завершення):"
    )

    # Обробка натискання кнопки "Cancel"
    if ans_raw is None:
        continue # Пропустити цю ітерацію

    ans = ans_raw.strip().title() # Стандартизуємо ввід

    if ans == "Вихід": # Використовуємо українське слово
        missing = [o for o in all_oblasts if o not in guessed_oblasts]
        pd.DataFrame(missing, columns=["Області для вивчення"])\
          .to_csv("oblasts_to_learn.csv", index=False, encoding='utf-8-sig') # Додаємо кодування
        print("Невгадані області збережено у файл 'oblasts_to_learn.csv'.")
        break

    # --- Логіка пошуку з пріоритетом точного збігу ---
    best_match_full_name = None
    match_type = 0 # 0 = Немає збігу, 1 = Збіг за 'core' назвою, 2 = Точний збіг

    for full in all_oblasts:
        # Пропускаємо області, які вже вгадані
        if full in guessed_oblasts:
            continue

        # Визначаємо "core" назву
        core_name = full
        # Шукаємо " Oblast" в кінці, щоб уникнути випадкових збігів
        if full.endswith(" Oblast"):
            core_name = full.replace(" Oblast", "").strip()
        # Можна додати інші специфічні закінчення, якщо вони є у ваших даних
        # elif full.endswith(" Region"):
        #    core_name = full.replace(" Region", "").strip()

        # 1. Перевірка на ТОЧНИЙ збіг (найвищий пріоритет)
        if ans == full:
            best_match_full_name = full
            match_type = 2
            # Знайшли точний збіг - кращого варіанту бути не може.
            # Негайно виходимо з циклу пошуку.
            break

        # 2. Перевірка на збіг за 'core' назвою (нижчий пріоритет)
        elif ans == core_name:
            # Якщо знайдено збіг за 'core' назвою, зберігаємо його,
            # АЛЕ ТІЛЬКИ ЯКЩО досі не було знайдено ТОЧНОГО збігу.
            # НЕ виходимо з циклу 'for', бо далі може бути точний збіг.
            if match_type < 2: # Оновлюємо, тільки якщо поточний найкращий - не точний
                best_match_full_name = full
                match_type = 1
            # Не ставимо 'break' тут!

    # --- Обробка результату пошуку ---
    if best_match_full_name: # Якщо знайдено будь-який збіг (точний або core)
        guessed_oblasts.append(best_match_full_name)

        # Малюємо напис
        turtle_pen = turtle.Turtle()
        turtle_pen.hideturtle()
        turtle_pen.penup()
        # Важливо: Використовуємо знайдену НАЙКРАЩУ відповідність ('best_match_full_name')
        row = data[data.Oblast == best_match_full_name]
        if not row.empty:
            # Безпечне отримання координат за допомогою .iloc[0]
            x = float(row.x.iloc[0])
            y = float(row.y.iloc[0])
            turtle_pen.goto(x, y)
            turtle_pen.write(best_match_full_name, align="center", font=("Arial", 8, "normal"))
        else:
            # Цього не мало б статись, якщо all_oblasts створено з data
            print(f"Помилка: Не знайдено координати для {best_match_full_name}")
    else:
        # Якщо не знайдено жодної відповідності (ні точної, ні core)
        # Можна додати повідомлення (наприклад, за допомогою print або turtle)
        # print(f"'{ans}' - не знайдено або вже вгадано.")
        continue # Переходимо до наступного запиту в циклі while

# --- Завершення гри ---
if len(guessed_oblasts) == TARGET:
    print("Вітаємо! Ви вгадали всі області!")
else:
    # Це повідомлення з'явиться, якщо гра завершилась через 'Вихід'
    print("Гру завершено.")

# Можна залишити вікно відкритим до кліку
# screen.exitonclick()