import utime
from machine import Pin, PWM, ADC, I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

I2C_ADDR     = 39
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

pel_pwm = PWM(Pin(6))
pel_pwm.freq(1000)

for_pwm = PWM(Pin(8))
for_pwm.freq(1000)

coo_pwm = PWM(Pin(11))
coo_pwm.freq(1000)
coo_pwm.duty_u16(30000)

conversion_factor_sensor = 5 / 65535
conversion_factor = 3.3 / 65535

def read_temp(): #Medición interna de temperatura
    sensor_temp = machine.ADC(26) # Tomo una medición
    reading = sensor_temp.read_u16()
    temperature = ((reading * conversion_factor_sensor) - 0.25) / 0.01
    formatted_temperature = "{:.1f}".format(temperature)
    string_temperature = str("Temperatura:" + formatted_temperature)
    utime.sleep(0.1)
    return string_temperature

def read_temp2(): #Medición caliente de temperatura
    sensor_temp2 = machine.ADC(27)
    reading2 = sensor_temp2.read_u16() 
    temperature2 = ((reading2 * conversion_factor) - 0.25) / 0.01
    formatted_temperature2 = "{:.2f}".format(temperature2)
    string_temperature2 = str("Temp2:" + formatted_temperature2)
    utime.sleep(0.1)
    return string_temperature2

def read_setpoint(): #Valor de setpoint
    sense_setpoint = machine.ADC(28)
    reading3 = sense_setpoint.read_u16() 
    setpoint = (reading3 * conversion_factor * 30) / 3.3
    formatted_setpoint = "{:.1f}".format(setpoint)
    string_setpoint = str("Setpoint:" + formatted_setpoint)
    utime.sleep(0.1)
    return string_setpoint

while True:

    sensor_temp = machine.ADC(26)
    reading = sensor_temp.read_u16()
    temperature = ((reading * conversion_factor_sensor) - 0.25) / 0.01
    
    sensor_temp2 = machine.ADC(27)
    reading2 = sensor_temp2.read_u16() 
    temperature2 = ((reading2 * conversion_factor_sensor) - 0.25) / 0.01
    
    sense_setpoint = machine.ADC(28)
    reading3 = sense_setpoint.read_u16() 
    setpoint = (reading3 * conversion_factor) * 30 / 3.3

    print(temperature, temperature2, setpoint)
    utime.sleep_ms(500)
    
    error = temperature - setpoint
    kp = error * 10000
    kp = int(kp)
    Potencia = 1

    temperature = read_temp()
    lcd.move_to(0, 0)
    lcd.putstr(temperature)
    
    setpoint = read_setpoint()
    lcd.move_to(0, 1)
    lcd.putstr(setpoint)
    utime.sleep_ms(500)
    

        
    if (error > 0):
        Potencia = Potencia * kp
        pel_pwm.duty_u16(Potencia)
                
    elif (error <= 0):
        Potencia = 0
        pel_pwm.duty_u16(0)
    
    if (Potencia >=65535):
        Potencia = 65535
    
    if (temperature2 >= 30):
        for_pwm.duty_u16(60000)
        
    else:
        for_pwm.duty_u16(0)
        
