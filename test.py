import bluepy as btle
import BB8_simple

bb8 = BB8_simple.BB8Controller()
bb8.go_forward()
bb8.go_back()
bb8.go_left()
bb8.go_right()
bb8.disconnect()
