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
headers = {'Content-Type': 'application/json'}

# ThingSpeak kötelező api_key mezővel
payload = {
    "api_key": "IDE_IRAD_A_THINGSPEAK_WRITE_API_KEYEDET",
    "field1": 0.0,
    "field2": 0.0,
    "field3": 0.0,
    "field4": 0.0
}

async def read_dht_sensor():
    dht_sensor = dht.DHT22(Pin(7)) # Ha a rajz szerint van: Pin(3)
    while True:
        try:
            dht_sensor.measure()
            temperature = dht_sensor.temperature()
            humidity = dht_sensor.humidity()
            print("Temp.: {:.2f} °C, Humidity: {:.2f} %".format(temperature, humidity))
            payload['field1'] = temperature
            payload['field2'] = humidity
        except Exception as e:
            print("Error during reading DHT22 sensor:", e)
        await asyncio.sleep(2)

async def read_Soil_moisture_sensor():
    soil_moisture_sensor = ADC(Pin(3))
    soil_moisture_sensor.atten(ADC.ATTN_11DB) # 0-3.3V méréshatár!
    while True:
        try:
            soil_moisture_value = soil_moisture_sensor.read_u16()
            print("Soil Moisture Value:", soil_moisture_value)
            payload['field3'] = soil_moisture_value
        except Exception as e:
            print("Error during reading Soil Moisture sensor:", e)
        await asyncio.sleep(5)

async def read_Soil_temperature_sensor():
    soil_temp_sensor = ADC(Pin(6))
    soil_temp_sensor.atten(ADC.ATTN_11DB) # 0-3.3V méréshatár!
    while True:
        try:
            soil_temp_value = soil_temp_sensor.read_u16()
            print("Soil Temperature Value:", soil_temp_value)
            payload['field4'] = soil_temp_value
        except Exception as e:
            print("Error during reading Soil Temperature sensor:", e)
        await asyncio.sleep(5)

async def send_data():
    while True:
        try:
            # Csak akkor küldünk, ha van net
            if wlan and wlan.isconnected():
                response = urequests.post(url, data=json.dumps(payload), headers=headers)
                print("Data sent to ThingSpeak. Response:", response.text)
                response.close() # Nagyon fontos memóriaszivárgás ellen!
        except Exception as e:
            print("Error sending data to ThingSpeak:", e)
        
        # A ThingSpeak ingyenes limitje miatt MINIMUM 15-20 mp kell!
        await asyncio.sleep(20)

async def control_pump():
    pump = Pin(13, Pin.OUT, value=0) # Ha a rajz szerint van: Pin(8)
    while True:
        if 'field3' in payload and float(payload['field3']) < 20000:
            print("Pump ON")
            pump.value(1)
            await asyncio.sleep(5)
            pump.value(0)
            print("Pump OFF, waiting 15 mins...")
            await asyncio.sleep(900)  # 15 perc várakozás
        await asyncio.sleep(5)

async def led_control():
    Light_sensor = ADC(Pin(2))
    Light_sensor.atten(ADC.ATTN_11DB)
    LED = PWM(Pin(14), freq=1000) # Ha a rajz szerint van: Pin(15)
    
    while True:
        # A beolvasás bekerült a ciklusba!
        raw_val = Light_sensor.read()
        
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
    
    while True:
        await asyncio.sleep(1)

asyncio.run(main())