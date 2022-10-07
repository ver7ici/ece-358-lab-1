import matplotlib.pyplot as plt
import generator
from mm1_simulation import MM1Simulation
from mm1k_simulation import MM1KSimulation

MBPS = 1000000


def question_1():
    rate = 75
    size = 1000
    data = [generator.exponential_random(rate) for i in range(size)]
    mean = sum(data)/len(data)
    variance = sum([(xi - mean)**2 for xi in data])/(len(data) - 1)
    expected_mean = 1 / rate
    expected_variance = (1 / rate) ** 2
    mean_percentage_error = ((mean - expected_mean)/expected_mean) * 100
    variance_percentage_error = ((variance - expected_variance) / expected_variance) * 100
    print(f"Calculated Mean = {mean}")
    print(f"Calculated Variance = {variance}")
    print(f"Exponential Distribution Mean = {expected_mean}")
    print(f"Exponential Distribution Variance = {expected_variance}")
    print(f"Mean Percentage Error = {mean_percentage_error}")
    print(f"Variance Percentage Error = {variance_percentage_error}")


def question_3():
    simulation_time = 1000
    avg_packet_length = 2000
    transmission_rate = 1 * MBPS
    utilization_queues = [0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95]

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
    plt.savefig('graphs/question3-en-graph.png', bbox_inches='tight')
    plt.close()

    # Pidle Graph
    plt.plot(utilization_queues, p_idles, linestyle='--', marker='o')
    plt.title("Proportion of Time Server is Idle vs Traffic Intensity")
    plt.ylabel('Proportion of Time Server is Idle (P_idle)')
    plt.xlabel('Traffic Intensity (ρ)')
    plt.savefig('graphs/question3-p_idle-graph.png', bbox_inches='tight')
    plt.close()


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


def question_6():
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
            simulation = MM1KSimulation(simulation_time, utilization_queue, avg_packet_length, transmission_rate, max_queue_size)
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
        print("Running Question 1 \n")
        question_1()
    elif question == "3":
        print("Running Question 3 \n")
        question_3()
    elif question == "4":
        print("Running Question 4 \n")
        question_4()
    elif question == "6":
        print("Running Question 6 \n")
        question_6()
    else:
        print("Undefined question!")

    # args = sys.argv[1:]
    # if not args:
    #     print("Please define the question you want to run.")
    #     return
    #
    # if args[0] == "1":
    #     print("Running Question 1 \n")
    #     question_1()
    # elif args[0] == "3":
    #     print("Running Question 3 \n")
    #     question_3()
    # elif args[0] == "4":
    #     print("Running Question 4 \n")
    #     question_4()
    # elif args[0] == "6":
    #     print("Running Question 6 \n")
    #     question_6()
    # else:
    #     print("Not question")

    # question_1()
    # question_3()
    # question_4()
    # question_6()


if __name__ == '__main__':
    main()
