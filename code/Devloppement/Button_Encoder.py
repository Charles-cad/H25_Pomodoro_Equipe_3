from machine import Pin
from micropython_rotary_encoder import RotaryEncoderRP2, RotaryEncoderEvent
import uasyncio as asyncio


# button class
class Button_Encoder:
        # Listeners
    def any_event_listener(self, event, clicks):
        print(f"ANY Event ID: {event} Clicks: {clicks}")


    def event_press(self):
        self.pressFlag = True
        print(f"Single Click")
    def press(self):
        return self.pressFlag
        
    def longPress(self):
        return self.longPressFlag


    def multy_click_listener(self, clicks):
        print(f"Multiply Clicks: {clicks}")


    def event_longPress(self):
        self.longPressFlag = True
        print(f"Held")


    def released_listener(self):
        print(f"Released")
        
    def treated(self):
        self.pressFlag = False
        self.longPressFlag = False
        
    def __init__(self, pin):
        self.pressFlag = False
        self.longPressFlag = False
        # Define the pin for the button
        self.encoder_pin_sw = Pin(pin, Pin.IN, Pin.PULL_UP)

        # Create the rotary encoder object
        self.encoder = RotaryEncoderRP2(
            pin_sw=self.encoder_pin_sw,
        )
                # subscribe to events
        self.encoder.on(RotaryEncoderEvent.ANY, self.any_event_listener)
        self.encoder.on(RotaryEncoderEvent.CLICK, self.event_press)
        self.encoder.on(RotaryEncoderEvent.MULTIPLE_CLICK, self.multy_click_listener)
        self.encoder.on(RotaryEncoderEvent.HELD, self.event_longPress)
        self.encoder.on(RotaryEncoderEvent.RELEASED, self.released_listener)
        
    
# Example usage:
if __name__ == "__main__":        
    async def main():
        ENCODER_SW_PIN = 14
        encoder = Button_Encoder(ENCODER_SW_PIN)
        
        # Start the event loop
        print("Using such a huge library to collect button events is overkill for me, but if you need to...")
        print(f"Connect you button to the next GPIO pin: SW {ENCODER_SW_PIN}")
        print("Then interact with it to test the firing of events.")
        asyncio.create_task(encoder.encoder.async_tick())
        
    # Run the asyncio event loop
    asyncio.run(main())
        

        
        
        
    
