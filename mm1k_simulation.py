import heapq
import generator
from event import Event

class MM1KSimulation:
    def __init__(self, simulation_time, utilization_queue, avg_packet_length, transmission_rate, max_queue_size):
        # Performance Metrics
        self.En = 0  # Average number of packets in buffer
        self.p_idle = 0  # Proportion of time the server is idle
        self.p_loss = 0  # Packet loss probability

        # Initial parameters
        self.simulation_time = simulation_time  # T Simulation time
        self.utilization_queue = utilization_queue  # ρ Range of utilization of the queue
        self.avg_packet_length = avg_packet_length  # L Average length of packet in bits
        self.transmission_rate = transmission_rate   # C Transmission rate of the output link in bits/second
        self.max_queue_size = max_queue_size  # K Max queue size

        # Calculate Rates
        self.packet_rate = (self.utilization_queue * self.transmission_rate) / self.avg_packet_length  # Average number of arrival packets
        self.observation_rate = self.packet_rate * 5  # Average number of observation events

        # Events
        self.events = []  # Array to hold all events

        # Properties
        self.buffer = 0  # Buffer/queue
        self.idle = 0  # Idle
        self.loss = 0  # Loss
        self.packets = 0  # Number of generated arrival packets
        self.arrival = 0  # Number of arrival events
        self.depart = 0  # Number of depart events
        self.observation = 0  # Number of observation events

    def execute(self):
        # Generate Events
        self.generate_observations()
        self.generate_arrivals()

        # Initialize queue size & departure time
        queue_size = 0
        depart_time = 0

        # Iterate through each event
        while self.events:
            # Pop event from min-heap
            event = heapq.heappop(self.events)

            if event.event_type == "ARRIVAL":
                # Increment generated arrival packet
                self.packets += 1

                if queue_size < self.max_queue_size:
                    self.arrival += 1
                    queue_size += 1  # Increase queue size if arrival event

                    arrival_time = event.event_time
                    service_time = self.generate_service()

                    if arrival_time > depart_time:
                        depart_time = arrival_time + service_time
                    else:
                        depart_time += service_time

                    depart_event = Event('DEPART', depart_time)
                    heapq.heappush(self.events, depart_event)
                else:
                    # If queue size is greater than or equal to max queue size, 
                    # drop arrival packet and don't generate a departure event
                    self.loss += 1
            elif event.event_type == "DEPART":
                self.depart += 1
                queue_size -= 1  # Decrease queue size if departure event
            elif event.event_type == "OBSERVATION":
                self.observation += 1
                current_packets_buffer = self.arrival - self.depart

                # Buffer is idle when there are no arrivals
                if current_packets_buffer == 0:
                    self.idle += 1

                # Sum of packets in buffer
                self.buffer += current_packets_buffer
            else:
                raise Exception('Unknown event type')

        # Calculate metrics
        self.En = self.buffer/self.observation
        self.p_idle = self.idle/self.observation
        self.p_loss = self.loss/self.packets

    def generate_observations(self):
        observation_time = 0
        while observation_time < self.simulation_time:
            observation_time += self.generate_inter_observation()
            observation_event = Event('OBSERVATION', observation_time)
            heapq.heappush(self.events, observation_event)

    def generate_arrivals(self):
        arrival_time = 0
        while arrival_time < self.simulation_time:
            arrival_time += self.generate_inter_arrival()
            arrival_event = Event('ARRIVAL', arrival_time)
            heapq.heappush(self.events, arrival_event)

    def generate_inter_observation(self):
        return generator.exponential_random(self.observation_rate)

    def generate_inter_arrival(self):
        return generator.exponential_random(self.packet_rate)

    def generate_service(self):
        return generator.exponential_random(1/self.avg_packet_length)/self.transmission_rate
