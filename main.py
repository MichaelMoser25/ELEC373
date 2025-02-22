import numpy as np
import matplotlib.pyplot as plt
from collections import deque

class QueueSimulator:
    def __init__(self, arrival_rate, service_rate):
        self.lambda_ = arrival_rate  # Arrival rate
        self.mu = service_rate      # Service rate = 0.75
        self.queue = deque()        # Queue for packets
        self.current_time = 0
        self.server_busy = False
        self.service_finish_time = 0
        
        # Statistics
        self.total_queue_length = 0
        self.total_packets = 0
        self.total_delay = 0
        
    def generate_geometric(self, p):
        """Generate geometric distribution with parameter p"""
        return np.random.geometric(p)
    
    def simulate(self, time_slots):
        """Run simulation for specified number of time slots"""
        for t in range(time_slots):
            self.current_time = t
            
            # Check for packet arrival
            if self.generate_geometric(self.lambda_) == 1:
                self.total_packets += 1
                if self.server_busy:
                    self.queue.append(t)
                else:
                    self.server_busy = True
                    service_time = self.generate_geometric(self.mu)
                    self.service_finish_time = t + service_time
            
            # Check if service is complete
            if self.server_busy and t >= self.service_finish_time:
                if len(self.queue) > 0:
                    arrival_time = self.queue.popleft()
                    self.total_delay += t - arrival_time
                    service_time = self.generate_geometric(self.mu)
                    self.service_finish_time = t + service_time
                else:
                    self.server_busy = False
            
            # Record queue length
            self.total_queue_length += len(self.queue)
            
    def get_average_delay(self):
        """Calculate average queueing delay using Little's Law"""
        if self.total_packets == 0:
            return 0
        avg_queue_length = self.total_queue_length / self.current_time
        return avg_queue_length / self.lambda_

def theoretical_delay(lambda_, mu):
    """Calculate theoretical queueing delay"""
    if lambda_ >= mu:
        return float('inf')
    return (lambda_ * (1 - lambda_)) / (mu * (mu - lambda_))

# Run simulations
arrival_rates = [0.2, 0.4, 0.5, 0.6, 0.65, 0.7, 0.72, 0.74, 0.745]
service_rate = 0.75
time_slots = 1000000

empirical_delays = []
theoretical_delays = []

for lambda_ in arrival_rates:
    # Run simulation
    simulator = QueueSimulator(lambda_, service_rate)
    simulator.simulate(time_slots)
    empirical_delays.append(simulator.get_average_delay())
    
    # Calculate theoretical delay
    theoretical_delays.append(theoretical_delay(lambda_, service_rate))

# Plot results
plt.figure(figsize=(10, 6))
plt.plot(arrival_rates, empirical_delays, 'bo-', label='Simulation')
plt.plot(arrival_rates, theoretical_delays, 'r--', label='Theoretical')
plt.xlabel('Arrival Rate (λ)')
plt.ylabel('Expected Queueing Delay')
plt.title('Queueing Delay vs Arrival Rate')
plt.legend()
plt.grid(True)
plt.show()

# Print numerical results
print("\nNumerical Results:")
print("λ\tEmpirical\tTheoretical")
for i in range(len(arrival_rates)):
    print(f"{arrival_rates[i]:.3f}\t{empirical_delays[i]:.3f}\t\t{theoretical_delays[i]:.3f}")
