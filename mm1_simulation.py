import generator
from event import Event


class MM1Simulation:
    def __init__(self, simulation_time, utilization_queue, avg_packet_length, transmission_rate):
        # Performance Metrics
        self.En = 0
        self.p_idle = 0

        # Initial parameters
        self.simulation_time = simulation_time
        self.utilization_queue = utilization_queue
        self.avg_packet_length = avg_packet_length
        self.transmission_rate = transmission_rate

        # Calculate Rates
        self.packet_rate = (self.utilization_queue / self.avg_packet_length) * self.transmission_rate
        self.observation_rate = self.packet_rate * 5

        # Events
        self.events = []

        # Properties
        self.buffer = 0
        self.idle = 0
        self.arrival = 0
        self.depart = 0
        self.observation = 0

    def execute(self):
        self.generate_observations()
        self.generate_packets()
        self.calculate_metrics()

    def calculate_metrics(self):
        self.events.sort(key=lambda e: e.event_time)

        for event in self.events:
            if event.event_type == 'ARRIVAL':
                self.arrival += 1
            elif event.event_type == 'DEPART':
                self.depart += 1
            elif event.event_type == 'OBSERVATION':
                self.observation += 1
                current_packets_buffer = self.arrival - self.depart
                if current_packets_buffer == 0:
                    self.idle += 1
                self.buffer += current_packets_buffer
            else:
                raise Exception('Unknown event type')

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
