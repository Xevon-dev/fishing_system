from .openrouter import query_openrouter
from .weather import get_forecast


ADVICE_RULES = """
- ранок або вечір: +2
- температура 12–22 °C: +2
- вітер не більше 15 км/год: +1
- без опадів і ймовірність дощу менше 40%: +1
- хмарність 50–85%: +1
- тиск 748–763 мм рт.ст.: +2
- якщо вдень було погано (темп > 22, тиск поза 748–763, вітер > 25, опади > 3)
  і зараз ранок або вечір: −2
"""

ADVICE_FORMAT = """
Напиши відповідь українською, у такому ж форматі, як у старих рекомендаціях:

1. Абзац про сьогоднішній день і час доби з емодзі: 🌅 ранок, ☀️ день, 🌇 вечір, 🌙 ніч.
2. "Погодні умови: ..." – температура, вітер, опади, вологість, тиск, хмарність.
   Якщо якась величина поза нормою – поясни чому це погано або добре для риби.
3. Вердикт: ✅ Варто йти - ... або ⚠️ Можна спробувати - ... або ❌ Я б не йшов - ...
   Порадь по снасті, приманці й найкращому часу ловлі – 2-4 речення.
4. ℹ️ Зверніть увагу: ці рекомендації базуються на загальних закономірностях поведінки риби
   та враховують особливості цієї водойми. Але власний досвід завжди важливіший –
   уважно стеж за змінами погоди і будь готовий швидко завершити рибалку,
   якщо умови погіршаться.

Пиши саме про сьогодні, без води, звертайся на "ти".
"""

def time_of_day(hour):
    if hour < 6:
        return "ніч"
    if hour < 10:
        return "ранок"
    if hour < 16:
        return "день"
    if hour < 21:
        return "вечір"
    return "ніч"


def score_conditions(weather):
    today = weather["forecast"]["forecastday"][0]
    day = today["day"]
    noon = today["hour"][12]
    time = time_of_day(int(weather["location"]["localtime"][11:13]))

    temp = round(day["avgtemp_c"])
    wind = round(day["maxwind_kph"])
    precip = day["totalprecip_mm"]
    pressure = round(noon["pressure_mb"] * 0.750062)
    cloud = noon["cloud"]
    chance_of_rain = day["daily_chance_of_rain"]

    score = 0
    if time in ("ранок", "вечір"):
        score += 2
    if 12 <= temp <= 22:
        score += 2
    if wind <= 15:
        score += 1
    if precip == 0 and chance_of_rain < 40:
        score += 1
    if 50 <= cloud <= 85:
        score += 1
    if 748 <= pressure <= 763:
        score += 2

    morning_was_bad = (
        temp > 22
        or pressure < 748
        or pressure > 763
        or wind > 25
        or precip > 3
    )
    if morning_was_bad and time in ("ранок", "вечір"):
        score -= 2

    if score >= 6:
        verdict = "✅ Варто йти"
    elif score >= 4:
        verdict = "⚠️ Можна спробувати"
    else:
        verdict = "❌ Я б не йшов"

    return {
        "score": score,
        "time": time,
        "verdict": verdict,
        "date": today["date"],
        "temp": temp,
        "min_temp": round(day["mintemp_c"]),
        "max_temp": round(day["maxtemp_c"]),
        "wind": wind,
        "precip": precip,
        "humidity": round(day["avghumidity"]),
        "pressure": pressure,
        "cloud": cloud,
        "chance_of_rain": chance_of_rain,
        "condition": day["condition"]["text"],
    }


def build_prompt(weather, water, score):

    water_text = f"{water.get('name') or 'Ця водойма'} ({water.get('type') or 'водойма'})"
    if water.get("area"):
        water_text += f", площа {water['area']} км²"
    if water.get("depth"):
        water_text += f", глибина {water['depth']}"
    if water.get("fish"):
        water_text += f", види риби: {water['fish']}"

    return f"""
Ти досвідчений рибальчий гід України. Напиши рекомендацію для рибалки на сьогодні.

Водойма: {water_text}

Погода на сьогодні ({score['date']}), зараз {weather['location']['localtime'][11:16]}:
{score['condition']}, середня температура {score['temp']} °C (від {score['min_temp']} до {score['max_temp']} °C),
вітер до {score['wind']} км/год, опади {score['precip']} мм,
ймовірність дощу {score['chance_of_rain']}%, вологість {score['humidity']}%,
тиск {score['pressure']} мм рт.ст., хмарність {score['cloud']}%.

Час доби зараз: {score['time']}
Оцінка умов на сьогодні: {score['score']} з 9 – {score['verdict']}

Критерії оцінки:
{ADVICE_RULES}
{ADVICE_FORMAT}
""".strip()


def get_advice(water):

    weather = get_forecast(water["lat"], water["lon"])

    score = score_conditions(weather)
    text = query_openrouter(build_prompt(weather, water, score))

    if text.startswith("Помилка:"):
        raise ValueError(text)

    return [part.strip() for part in text.split("\n\n") if part.strip()]