import time

class VisualServoDryRun:
    def __init__(self):
        # Image settings
        self.image_width = 640
        self.cx = self.image_width / 2.0
        
        # Target settings
        self.target_depth = 1.0 # Stop 1 meter away
        
        # Tunable Proportional Gains
        self.k_w = 0.002  # Angular gain
        self.k_v = 0.5    # Linear gain
        
        # Safety limits
        self.max_w = 0.5
        self.max_v = 1.0

    def compute_velocity(self, target_x, current_depth):
        print(f"\n--- AI Detection: Object at X: {target_x}px, Depth: {current_depth}m ---")
        
        # 1. Angular Velocity Calculation (Yaw)
        error_x = target_x - self.cx
        raw_w = -self.k_w * error_x
        
        # Clamp angular velocity to safety limits
        cmd_w = max(min(raw_w, self.max_w), -self.max_w)
        
        # 2. Linear Velocity Calculation (Forward)
        error_z = current_depth - self.target_depth
        raw_v = self.k_v * error_z
        
        # Clamp linear velocity to safety limits
        cmd_v = max(min(raw_v, self.max_v), -self.max_v)
        
        # Print the thought process
        print(f"Error X: {error_x}px  -> Cmd Angular Z: {cmd_w:.3f} rad/s")
        print(f"Error Z: {error_z:.2f}m -> Cmd Linear X:  {cmd_v:.3f} m/s")

# Run the simulation
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
