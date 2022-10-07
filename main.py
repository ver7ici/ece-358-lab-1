import os
import csv
import matplotlib.pyplot as plt
import generator
from mm1_simulation import MM1Simulation
from mm1k_simulation import MM1KSimulation

MBPS = 1000000
GRAPH_FOLDER = 'graphs'
DATA_FOLDER = 'data'


# Question 1 - Generate 1000 Exponential Random Variables
def question_1():
    # Create directory to save the data in csv
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

    rate = 75  # λ = 75
    size = 1000  # 1000 data points
    runs = 5  # Iteration to run
    runs_data = []  # Array of results

    # Calculate & display the expected mean & variance from λ
    expected_mean = 1 / rate
    expected_variance = (1 / rate) ** 2
    print(f"Exponential Distribution Mean = {expected_mean}")
    print(f"Exponential Distribution Variance = {expected_variance}")
    print("")

    # Iterate for runs
    for i in range(1, runs+1):
        data = [generator.exponential_random(rate) for i in range(size)]

        # Calculate & display mean & variance from generated data
        mean = sum(data) / len(data)
        variance = sum([(xi - mean) ** 2 for xi in data]) / (len(data) - 1)
        print(f"Run: {i}")
        print(f"Calculated Mean: {mean}")
        print(f"Calculated Variance: {variance}")
        print("")

        # Store the runs in array
        runs_data.append([i, mean, variance])

    # Display average of results
    calculated_mean = 0
    calculated_variance = 0
    for run_data in runs_data:
        calculated_mean += run_data[1]
        calculated_variance += run_data[2]
    print(f"Average Calculated Mean: {calculated_mean/len(runs_data)}")
    print(f"Average Calculated Variance: {calculated_variance/len(runs_data)}")
    print("")

    # Write to CSV file
    print("Writing to CSV...")
    header = ['Run', 'Mean', 'Variance']
    with open(f"{DATA_FOLDER}/question1-exponential-random-data.csv", 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(runs_data)
    print("Done!")


# Question 3 - M/M/1 Queue Simulation
def question_3():
    # Create directory to save the graphs
    if not os.path.exists(GRAPH_FOLDER):
        os.makedirs(GRAPH_FOLDER)

    # Create directory to save the data in csv
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

    # Initialize parameters
    simulation_time = 1000  # T Simulation time
    avg_packet_length = 2000  # L Average length of packet in bits
    transmission_rate = 1 * MBPS  # C Transmission rate of the output link in bits/second
    utilization_queues = [0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95]  # ρ Range of utilization of the queue

    avg_packets = []
    p_idles = []

    for utilization_queue in utilization_queues:
        simulation = MM1Simulation(simulation_time, utilization_queue, avg_packet_length, transmission_rate)
        print(f"Simulation Execute - Traffic Intensity (ρ): {utilization_queue}")
        simulation.execute()
        print(f"En: {simulation.En}")
        avg_packets.append(simulation.En)
        print(f"P_idle: {simulation.p_idle}")
        p_idles.append(simulation.p_idle)
        print("")

    # En Graph
    plt.plot(utilization_queues, avg_packets, linestyle='--', marker='o')
    plt.title("Average Number of Packets vs Traffic Intensity")
    plt.ylabel('Average Number of Packets (En)')
    plt.xlabel('Traffic Intensity (ρ)')
    plt.savefig(f"{GRAPH_FOLDER}/question3-en-graph.png", bbox_inches='tight')
    plt.close()

    # Pidle Graph
    plt.plot(utilization_queues, p_idles, linestyle='--', marker='o')
    plt.title("Proportion of Time Server is Idle vs Traffic Intensity")
    plt.ylabel('Proportion of Time Server is Idle (P_idle)')
    plt.xlabel('Traffic Intensity (ρ)')
    plt.savefig(f"{GRAPH_FOLDER}/question3-p_idle-graph.png", bbox_inches='tight')
    plt.close()


# Question 4 - M/M/1 Queue Simulation for ρ = 1.2
def question_4():
    utilization_queue = 1.2
    simulation_time = 1000
    avg_packet_length = 2000
    transmission_rate = 1 * MBPS

    simulation = MM1Simulation(simulation_time, utilization_queue, avg_packet_length, transmission_rate)
    print(f"Simulation Execute - Traffic Intensity: {utilization_queue}")
    simulation.execute()
    print(f"En: {simulation.En}")
    print(f"P_idle: {simulation.p_idle}")


# Question 6 - M/M/1/K Queue Simulation
def question_6():
    if not os.path.exists(GRAPH_FOLDER):
        os.makedirs(GRAPH_FOLDER)

    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

    simulation_time = 1000
    avg_packet_length = 2000
    transmission_rate = 1 * MBPS
    utilization_queues = [0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5]
    # utilization_queues = [0.5, 0.6]
    max_queue_sizes = [10, 25, 50]
    # max_queue_sizes = [10]

    avg_packets = []
    p_losses = []

    for max_queue_size in max_queue_sizes:
        avg_packets_k = []
        p_losses_k = []
        for utilization_queue in utilization_queues:
            simulation = MM1KSimulation(simulation_time, utilization_queue, avg_packet_length, transmission_rate,
                                        max_queue_size)
            print(f"Simulation Execute at Traffic Intensity: {utilization_queue}, Max Queue Size: {max_queue_size}")
            simulation.execute()
            print(f"En: {simulation.En}")
            avg_packets_k.append(simulation.En)
            print(f"Pidle: {simulation.p_idle}")
            print(f"Ploss: {simulation.p_loss}")
            p_losses_k.append(simulation.p_loss)
            print("")

        avg_packets.append(avg_packets_k)
        p_losses.append(p_losses_k)

    # En Graph
    for avg_packet in avg_packets:
        plt.plot(utilization_queues, avg_packet, linestyle='--', marker='o')
    plt.title("Average Number of Packets vs Traffic Intensity")
    plt.ylabel('Average Number of Packets (En)')
    plt.xlabel('Traffic Intensity (ρ)')
    plt.legend(['k = 10', 'k = 25', 'k = 50'], loc='upper left')
    plt.savefig('graphs/question6-en-graph.png', bbox_inches='tight')
    plt.close()

    # En Graph
    for p_loss in p_losses:
        plt.plot(utilization_queues, p_loss, linestyle='--', marker='o')
    plt.title("Average Number of Packets vs Traffic Intensity")
    plt.ylabel('Average Number of Packets (En)')
    plt.xlabel('Traffic Intensity (ρ)')
    plt.legend(['k = 10', 'k = 25', 'k = 50'], loc='upper left')
    plt.savefig('graphs/question6-p_loss-graph.png', bbox_inches='tight')
    plt.close()


def main():
    question = input("Enter question: ")

    if question == "1":
        print("Running Question 1... \n")
        question_1()
    elif question == "3":
        print("Running Question 3... \n")
        question_3()
    elif question == "4":
        print("Running Question 4... \n")
        question_4()
    elif question == "6":
        print("Running Question 6... \n")
        question_6()
    else:
        print("Undefined question!")


if __name__ == '__main__':
    main()
