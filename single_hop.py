import numpy as np
import matplotlib.pyplot as plt

# Simulation Parameters
bit_rate = 1e6  # 1 Mbps (Megabits per second)
packet_size = 1000  # Packet size in bits
propagation_delay = 0.001  # 1ms fixed delay (time for signal to travel)
num_packets = 1000  # Total packets to simulate
error_prob = 0.002  # Probability of a bit error (adjust this value)
error_threshold = 5  # Max errors per packet before it is considered lost
retransmission_delay = 0.002  # Additional delay if packet needs retransmission

# Lists to store results for plotting
delays = []
throughputs = []
errors_list = []

# Function to simulate packet transmission
def transmit_packet():
    """Simulates a single packet transmission and computes delays and errors."""
    transmission_delay = packet_size / bit_rate  # Time to transmit the packet
    errors = np.random.rand(packet_size) < error_prob  # Simulating bit errors
    num_errors = np.sum(errors)  # Total number of errors in the packet
    
    # Compute total delay (including retransmission if needed)
    total_delay = transmission_delay + propagation_delay
    if num_errors > error_threshold:
        total_delay += retransmission_delay  # Adding delay for retransmission
    
    # Compute throughput (only count if errors are within acceptable range)
    throughput = packet_size / total_delay if num_errors <= error_threshold else 0
    
    return total_delay, throughput, num_errors

# Run the simulation for multiple packets
for _ in range(num_packets):
    tx_delay, tx_throughput, tx_errors = transmit_packet()
    delays.append(tx_delay)
    throughputs.append(tx_throughput)
    errors_list.append(tx_errors)

# Plot Results
plt.figure(figsize=(12, 5))

# Plot Delay
plt.subplot(1, 2, 1)
plt.plot(range(num_packets), delays, label="Delay per Packet")
plt.xlabel("Packet #")
plt.ylabel("Delay (s)")
plt.title("Transmission Delay")
plt.legend()

# Plot Throughput
plt.subplot(1, 2, 2)
plt.plot(range(num_packets), throughputs, label="Throughput per Packet")
plt.xlabel("Packet #")
plt.ylabel("Throughput (bps)")
plt.title("Throughput Over Time")
plt.legend()

plt.show()

# Display Error Statistics
print(f"Average delay: {np.mean(delays):.6f} seconds")
print(f"Average throughput: {np.mean(throughputs):.2f} bps")
print(f"Packets with errors: {np.sum(np.array(errors_list) > 0)} / {num_packets}")
