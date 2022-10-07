import generator
from event import Event


class MM1Simulation:
    def __init__(self, simulation_time, utilization_queue, avg_packet_length, transmission_rate):
        # Performance Metrics
        self.En = 0  # Average number of packets in buffer
        self.p_idle = 0  # Proportion of time the server is idle

        # Initial parameters
        self.simulation_time = simulation_time  # T Simulation time
        self.utilization_queue = utilization_queue  # ρ Range of utilization of the queue
        self.avg_packet_length = avg_packet_length  # L Average length of packet in bits
        self.transmission_rate = transmission_rate  # C Transmission rate of the output link in bits/second

        # Calculate Rates
        self.packet_rate = (self.utilization_queue / self.avg_packet_length) * self.transmission_rate  # Average number of arrival packets
        self.observation_rate = self.packet_rate * 5  # Average number of observation events

        # Events
        self.events = []  # Array to hold all events

        # Properties
        self.buffer = 0  # Buffer/queue
        self.idle = 0  # Idle
        self.arrival = 0  # Number of arrival events
        self.depart = 0  # Number of depart events
        self.observation = 0  # Number of observation events

    def execute(self):
        # Generate Events
        self.generate_observations()
        self.generate_packets()

        # Sort events by time
        self.events.sort(key=lambda e: e.event_time)

        # Iterate through each event
        for event in self.events:
            if event.event_type == 'ARRIVAL':
                self.arrival += 1
            elif event.event_type == 'DEPART':
                self.depart += 1
            elif event.event_type == 'OBSERVATION':
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

    def generate_observations(self):
        observation_time = 0
        while observation_time < self.simulation_time:
            observation_time += self.generate_inter_observation()
            observation_event = Event('OBSERVATION', observation_time)
            self.events.append(observation_event)

    def generate_packets(self):
        arrival_time = 0
        depart_time = 0
        while arrival_time < self.simulation_time:
            arrival_time += self.generate_inter_arrival()
            service_time = self.generate_service()

            if arrival_time > depart_time:
                depart_time = arrival_time + service_time
            else:
                depart_time += service_time

            arrival_event = Event('ARRIVAL', arrival_time)
            depart_event = Event('DEPART', depart_time)
            self.events.append(arrival_event)
            self.events.append(depart_event)

    def generate_inter_observation(self):
        return generator.exponential_random(self.observation_rate)

    def generate_inter_arrival(self):
        return generator.exponential_random(self.packet_rate)

    def generate_service(self):
        return generator.exponential_random(1/self.avg_packet_length)/self.transmission_rate
