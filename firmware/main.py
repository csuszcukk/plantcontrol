from machine import Pin, I2C, ADC, PWM
import uasyncio as asyncio
import wifimanager
import dht
import urequests
import json

wlan = wifimanager.get_connection()

if wlan and wlan.isconnected():
    print("Sikeres netcsatlakozás! IP:", wlan.ifconfig()[0])

url = "https://api.thingspeak.com/update"
payload = {}
headers = {'Content-Type': 'application/json'}

async def read_dht_sensor():
    dht_sensor = dht.DHT22(Pin(7))
    while True:
        try:
            dht_sensor.measure()
            temperature = dht_sensor.temperature()
            humidity = dht_sensor.humidity()
            print("Temp.: {:.2f} °C, Humidity: {:.2f} %".format(temperature, humidity))
            payload['temperature'] = temperature
            payload['humidity'] = humidity
        except Exception as e:
            print("Error durring reading DHT22 sensor:", e)
        await asyncio.sleep(2)

async def read_Soil_moisture_sensor():
    soil_moisture_sensor = ADC(Pin(3))
    while True:
        try:
            soil_moisture_value = soil_moisture_sensor.read_u16()
            print("Soil Moisture Value:", soil_moisture_value)
            payload['soil_moisture'] = soil_moisture_value
        except Exception as e:
            print("Error during reading Soil Moisture sensor:", e)
        await asyncio.sleep(5)

async def read_Soil_temperature_sensor():
    soil_temp_sensor = ADC(Pin(6))
    while True:
        try:
            soil_temp_value = soil_temp_sensor.read_u16()
            print("Soil Temperature Value:", soil_temp_value)
            payload['soil_temperature'] = soil_temp_value
        except Exception as e:
            print("Error during reading Soil Temperature sensor:", e)
        await asyncio.sleep(5)

async def send_data():
    while True:
            try:
                response = urequests.post(url, data=json.dumps(payload), headers=headers)
                print("Data sent to ThingSpeak. Response:", response.text)
                response.close()
            except Exception as e:
                print("Error sending data to ThingSpeak:", e)
            await asyncio.sleep(10)

async def control_pump():
    pump = Pin(13, Pin.OUT)
    while True:
        if 'soil_moisture' in payload and payload['soil_moisture'] < 20000:
            pump.value(1)
            await asyncio.sleep(5)
            pump.value(0)
            print("Pump ON")
            await asyncio.sleep(900)  # Wait for 15 minutes before checking again
        await asyncio.sleep(5)

async def led_control():
    Light_sensor = ADC(Pin(2))
    Light_sensor.atten(ADC.ATTN_11DB)  # Set attenuation for full range (0-3.3V)
    raw_val = Light_sensor.read()
    LED = PWM(Pin(14), freq=1000)
    while True:
        target_duty = 65535 - int((raw_val / 4095) * 65535)
        target_duty = max(0, min(65535, target_duty))

        LED.duty_u16(target_duty)
        await asyncio.sleep_ms(50)
async def main():
    asyncio.create_task(read_dht_sensor())
    asyncio.create_task(read_Soil_moisture_sensor())
    asyncio.create_task(read_Soil_temperature_sensor())
    asyncio.create_task(send_data())
    asyncio.create_task(control_pump())
    asyncio.create_task(led_control())