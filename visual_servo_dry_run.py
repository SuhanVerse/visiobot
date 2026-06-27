# visual_servo_dry_run.py

import time

class VisualServoDryRun:
    def __init__(self):

        self.image_width = 640
        self.cx = self.image_width / 2.0
        
        self.target_depth = 1.0 
        
        self.k_w = 0.002 
        self.k_v = 0.5 
        
        self.max_w = 0.5
        self.max_v = 1.0

    def compute_velocity(self, target_x, current_depth):
        print(f"\n--- Detection: Object at X: {target_x}px, Depth: {current_depth}m ---")
        
        error_x = target_x - self.cx
        raw_w = -self.k_w * error_x
        
        cmd_w = max(min(raw_w, self.max_w), -self.max_w)

        error_z = current_depth - self.target_depth
        raw_v = self.k_v * error_z
        
        cmd_v = max(min(raw_v, self.max_v), -self.max_v)

        print(f"Error X: {error_x}px  -> Cmd Angular Z: {cmd_w:.3f} rad/s")
        print(f"Error Z: {error_z:.2f}m -> Cmd Linear X:  {cmd_v:.3f} m/s")

if __name__ == '__main__':
    servo = VisualServoDryRun()
    
    # Scenario 1: Object is far to the right (x=600) and far away (3.0m)
    servo.compute_velocity(target_x=600, current_depth=3.0)
    time.sleep(1)
    
    # Scenario 2: Object is getting closer to center (x=400) and depth is closing (1.5m)
    servo.compute_velocity(target_x=400, current_depth=1.5)
    time.sleep(1)
    
    # Scenario 3: Object is perfectly centered (x=320) and at target distance (1.0m)
    servo.compute_velocity(target_x=320, current_depth=1.0)
