import heapq
import generator
from event import Event

def heap_comp(a,b):
    return a.event_time < b.event_time

class MM1KSimulation:
    def __init__(self, simulation_time, utilization_queue, avg_packet_length, transmission_rate, max_queue_size):
        # Performance Metrics
        self.En = 0
        self.p_idle = 0
        self.p_loss = 0

        # Initial parameters
        self.simulation_time = simulation_time
        self.utilization_queue = utilization_queue
        self.avg_packet_length = avg_packet_length
        self.transmission_rate = transmission_rate
        self.max_queue_size = max_queue_size

        # Calculate Rates
        self.packet_rate = (self.utilization_queue * self.transmission_rate) / self.avg_packet_length
        self.observation_rate = self.packet_rate * 5

        # Events
        # self.arrival_events = []
        # self.depart_events = []
        self.events = []
        # self.dropped = 0
        # self.packets = 1


    def execute(self):
        self.generate_observations()
        self.generate_arrivals()
        # self.generate_packets()
        self.calculate_metrics()

    def calculate_metrics(self):
        queue_size = 0

        buffer = 0
        idle = 0
        loss = 0
        packets = 0

        arrival = 0
        depart = 0
        observation = 0
        depart_time = 0

        while self.events:
            event = heapq.heappop(self.events)
            if event.event_type == "ARRIVAL":
                packets += 1

                if queue_size < self.max_queue_size:
                    arrival += 1
                    queue_size += 1

                    arrival_time = event.event_time
                    service_time = self.generate_service()

                    if arrival_time > depart_time:
                        depart_time = arrival_time + service_time
                    else:
                        depart_time += service_time

                    depart_event = Event('DEPART', depart_time)
                    heapq.heappush(self.events, depart_event)
                else:
                    loss += 1
            elif event.event_type == "DEPART":
                depart += 1
                queue_size -= 1
            elif event.event_type == "OBSERVATION":
                observation += 1
                current_packets_buffer = arrival - depart
                if current_packets_buffer == 0:
                    idle += 1
                buffer += current_packets_buffer
            else:
                raise Exception('Unknown event type')

        # print("ARRIVALS: " + str(arrival))
        # print("DEPART: " + str(depart))
        # print("OBSERVATION: " + str(observation))
        # print("BUFFER: " + str(buffer))
        # print("LOSS: " + str(loss))
        # print("GENERATED: " + str(packets))
        # print("TOTAL: " + str(packets - loss))
        self.En = buffer/observation
        self.p_idle = idle/observation
        self.p_loss = loss/packets

        # buffer = 0
        # idle = 0
        # arrival = 0
        # depart = 0
        # observation = 0
        #
        # self.events.extend(self.arrival_events)
        # self.events.extend(self.depart_events)
        # self.events.sort(key=lambda e: e.event_time)
        #
        # for event in self.events:
        #     if event.event_type == 'ARRIVAL':
        #         arrival += 1
        #     elif event.event_type == 'DEPART':
        #         depart += 1
        #     elif event.event_type == 'OBSERVATION':
        #         observation += 1
        #         current_packets_buffer = arrival - depart
        #         if current_packets_buffer == 0:
        #             idle += 1
        #         buffer += current_packets_buffer
        #     else:
        #         raise Exception('Unknown event type')
        #
        # print("ARRIVALS: " + str(arrival))
        # print("DEPART: " + str(depart))
        # print("OBSERVATION: " + str(observation))
        # print("BUFFER: " + str(buffer))
        # print("LOSS: " + str(self.dropped))
        # print("GENERATED: " + str(self.packets))
        # print("TOTAL: " + str(self.packets - self.dropped))
        # self.En = buffer/observation
        # self.p_idle = idle/observation
        # self.p_loss = self.dropped/self.packets

    def generate_observations(self):
        observation_time = 0
        while observation_time < self.simulation_time:
            observation_time += self.generate_observer()
            observation_event = Event('OBSERVATION', observation_time)
            heapq.heappush(self.events, observation_event)
            # self.events.append(observation_event)

    def generate_arrivals(self):
        arrival_time = 0
        while arrival_time < self.simulation_time:
            arrival_time += self.generate_inter_arrival()
            arrival_event = Event('ARRIVAL', arrival_time)
            heapq.heappush(self.events, arrival_event)
            # self.events.append(arrival_event)

    # def generate_packets(self):
    #     queue_size = 1
    #     arrival_time = self.generate_inter_arrival()
    #     depart_time = arrival_time + self.generate_service()
    #     current_depart_time = depart_time
    #     depart_counter = 0
    #
    #     arrival_event = Event('ARRIVAL', arrival_time)
    #     self.arrival_events.append(arrival_event)
    #     depart_event = Event('DEPART', depart_time)
    #     self.depart_events.append(depart_event)
    #
    #     while arrival_time < self.simulation_time:
    #         arrival_time += self.generate_inter_arrival()
    #         service_time = self.generate_service()
    #
    #         queue_size += 1
    #         self.packets += 1
    #
    #         arrival_event = Event('ARRIVAL', arrival_time)
    #         self.arrival_events.append(arrival_event)
    #
    #         if arrival_time <= current_depart_time:
    #             if queue_size < self.max_queue_size:
    #                 depart_time += service_time
    #
    #                 depart_event = Event('DEPART', depart_time)
    #                 self.depart_events.append(depart_event)
    #             else:
    #                 self.arrival_events.pop()
    #                 self.dropped += 1
    #                 continue
    #         else:
    #             queue_size -= 1
    #             depart_counter += 1
    #
    #             if arrival_time <= depart_time:
    #                 depart_time += service_time
    #             else:
    #                 depart_time = arrival_time + service_time
    #
    #             depart_event = Event('DEPART', depart_time)
    #             self.depart_events.append(depart_event)
    #
    #             current_depart_time = self.depart_events[depart_counter].event_time

    def generate_observer(self):
        return generator.exponential_random(self.observation_rate)

    def generate_inter_arrival(self):
        return generator.exponential_random(self.packet_rate)

    def generate_service(self):
        return generator.exponential_random(1/self.avg_packet_length)/self.transmission_rate
