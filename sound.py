import threading
import time
class Sound(object):
    def __init__(self,type,site,power,decay_type,decay_time,sport_type,sport_speed):
        self.type = type
        self.site = site
        self.power = power
        self.decay_type = decay_type
        self.decay_time = decay_time
        self.sport_type = sport_type
        self.sport_speed = sport_speed
        decay_thread = threading.Thread(target=self.decay)
        sport_thread = threading.Thread(target=self.sport)
        decay_thread.start()
        sport_thread.start()

    def decay(self):
        if self.decay_type == 'a':
            time.sleep(self.decay_time)  # Wait for decay_time to elapse.
            self.decayed_power = 0  # Set the power to 0 after decay_time.
            print(f"Decayed power: {self.decayed_power}")
        elif self.decay_type == 'b':
            decay_rate = self.power / self.decay_time
            num_steps = self.decay_time * 10  # 每秒分成十个时间片
            time_step = 1.0 / 10
            for i in range(num_steps):
                time.sleep(time_step)
                decay_amount = decay_rate * i
                self.decayed_power = max(0, self.decayed_power - decay_amount)
                print(f"Decayed power: {self.decayed_power}")

    def sport(self):
        print("sport")
        #TODO:根据传入参数实现运动功能





