# MELK LED for Home Assistant

Минимальная кастомная интеграция для лент **MELK / ELK-BLEDOM**.

Поведение как у приложения **Elkotrol**:
`connect → login → write → disconnect` на каждую команду.

## Возможности
- Вкл / выкл
- RGB цвет
- Яркость
- Эффекты (jump / fade / blink)
- Голосовое управление через Алису (через light entity)

## Требования
- Home Assistant 2024.6+
- Рабочий Bluetooth adapter или **ESPHome Bluetooth Proxy** / Android BLE Proxy
- Лента с именем `MELK-*` / `ELK-*`

## Установка

### Вручную
```bash
cd /config/custom_components
git clone https://github.com/toragi/melk-led.git /tmp/melk-led
cp -r /tmp/melk-led/custom_components/melk_led .
rm -rf /tmp/melk-led
```

Перезапуск Home Assistant → **Настройки → Устройства и службы → Добавить интеграцию → MELK LED**

MAC пример: `BE:67:01:03:09:E0`

### HACS (после публикации)
HACS → Custom repositories → `https://github.com/toragi/melk-led` → Integration

## Важно
Пока в HA нет активного Bluetooth scanner/proxy (`0 scanners`), интеграция не сможет подключиться к ленте. Сначала подними ESP32 Bluetooth Proxy или Android BLE Proxy.

## Протокол
- Write UUID: `0000fff3-0000-1000-8000-00805f9b34fb`
- Login (MELK): `7E 07 83` + `7E 04 04`
- Power / Color / Effect — стандартные 9-байтные кадры `7E … EF`
