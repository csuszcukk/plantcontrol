# PlantControl
make a smart pot for plants

<img width="1182" height="854" alt="image" src="https://github.com/user-attachments/assets/43174cda-7d5d-4d06-a59e-f9dee39e8c2f" />


## Features

* Automatic watering and light control
* Humidity and temperature monitoring
* Soil temperature and moisture monitoring
* Low water level alert
* Custom water container design
* Compatible with all plants and pots

## How to Build It

1. **PCB Fabrication:** Order the PCBs from any manufacturer (ordering a stencil is recommended).
2. **Heat Dissipation (Optional):** If you plan to use LEDs, mount them on an aluminum sheet using thermal conductive tape for proper heat dissipation.
3. **Components:** Order the necessary components listed in the Bill of Materials (BOM) — feel free to modify or skip non-essential parts.
4. **3D Printing:** Print the structural parts (PLA is recommended for the main board enclosure, and PETG for the water container).
5. **Assembly:** Solder all components onto the PCB.
6. **Preparation:** Connect the boot configuration pins and plug in the power source.
7. **Flashing Interface:** Connect your USB-to-UART bridge (make sure RX and TX lines are swapped).
8. **Firmware Installation (MicroPython):** Flash the ESP32 with the MicroPython firmware (see the official [MicroPython ESP32 Documentation](https://docs.micropython.org/en/latest/esp32/tutorial/intro.html)).
9. **Uploading Code:** Flash `main.py` onto the board (follow this [MicroPython Flashing Guide](https://georgefreedom.com/ignition-sequence-how-to-flash-micropython-onto-your-esp32/)).
10. **Cleanup:** Remove the boot mode jumpers and the UART adapter, then disconnect power.
11. **Wiring:** Connect all peripherals and modules to their respective header pins (labels are silkscreened on the PCB for guidance).
12. **Final Mounting:** Secure the sensors and the main board inside the enclosure (double-sided mounting tape works great).
13. **Power On:** Reconnect power to the board.
14. **Done!** Your plant controller is ready to go.

> **Pro Tip:** On first boot (or if it cannot connect to a saved network), the device will host a Wi-Fi Access Point. Connect to it to enter your local Wi-Fi SSID and password via the captive portal. Don't forget to enter your ThingSpeak API key in the configuration file to enable telemetry logging!


## How It Works

PlantControl is an automated, ESP32-C6-powered plant monitoring and maintenance system running on custom MicroPython firmware. It continuously monitors environmental conditions and manages irrigation and lighting using asynchronous event loops.

### Core Architecture

* **Sensor Data Acquisition:** The system periodically samples soil moisture, ambient light, and air temperature/humidity levels. 
* **Automated Logic & Safety:** If soil moisture drops below the predefined threshold, the MCU triggers a relay/MOSFET to activate the water pump. It includes safety timers to prevent over-watering or running the pump dry.
* **Local UI & Status:** A circular GC9A01 SPI display provides real-time readout of plant metrics and device status directly on the enclosure.
* **Power & Load Management:** High-side MOSFET switching ensures power is delivered efficiently to peripherals (pumps, LEDs) only when needed, minimizing idle power consumption.
* **Connectivity & Telemetry:** Integrated Wi-Fi connects to local infrastructure to stream telemetry to ThingSpeak. If network connection fails, it automatically spins up a Wi-Fi Access Point with a captive portal for re-configuration.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
