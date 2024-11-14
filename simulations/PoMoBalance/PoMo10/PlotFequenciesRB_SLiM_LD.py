import  numpy as np
import matplotlib.pyplot as plt
import os
import StationaryFrequencies as sf

if __name__ == '__main__':

    # Number of PoMo states
    N = 10
    # Entry in the dictionary for the simulated data
    type = {"bal_1": [], "bal_2": []}
    num = 2

    path = os.getcwd()
    iter = 1  # Iterator to import correct inference folder
    folder = "mix_100kb"
    keys = list(type.keys())
    for sel_type in keys:
        # Entry for inferred SFS
        type["{0}_inf".format(sel_type)] = []
        # Import simulated data
        path_to_data = os.path.join(path, 'data', folder, 'sequences_{0}.txt'.format(sel_type))
        poMoStates = np.genfromtxt(path_to_data)
        n_pop = len(poMoStates[:, 0])
        assert(n_pop == len(poMoStates[:, 0]))
        poMoStatesAll = poMoStates[:, 1:]
        n_nucl = len(poMoStatesAll[0, :])
        n_states = 4+6*(N-1)
        counts = np.zeros(n_states)
        for i in range(0, n_states):
            for j in range(n_pop):
                counts[i] += list(poMoStatesAll[j]).count(i)

        freq_sim = counts/(n_nucl*n_pop)

        # Import rates from inference

        print("Iteration", iter)
        path_to_log = os.path.join(path, "output{0}/".format(iter))
        logs = {}
        sel_log = [4]

        for log in sel_log:
            ex_log = np.genfromtxt(os.path.join(path_to_log, "test_pomo_balance_run_{0}.log".format(log)))
            logs[str(log)] = ex_log[1:]
        log_res = np.concatenate(list(logs.values()), axis=0)

        # Calculate mean rates
        sigma2 = np.mean(log_res[:, -1])
        phi2 = [1.0, 1.0 + sigma2, 1.0 + sigma2, 1.0]
        pi2 = [np.mean(log_res[:, -11]), np.mean(log_res[:, -10]), np.mean(log_res[:, -9]), np.mean(log_res[:, -8])]
        rho2 = [np.mean(log_res[:, -7]), np.mean(log_res[:, -6]), np.mean(log_res[:, -5]), np.mean(log_res[:, -4]),
                np.mean(log_res[:, -3]), np.mean(log_res[:, -2])]
        B2 = [np.mean(log_res[:, 4]), np.mean(log_res[:, 5]), np.mean(log_res[:, 6]), np.mean(log_res[:, 7]),
              np.mean(log_res[:, 8]), np.mean(log_res[:, 9])]
        #    B_val2 = round(N/2)
        beta2 = [np.mean(log_res[:, 10]), np.mean(log_res[:, 11]), np.mean(log_res[:, 12]), np.mean(log_res[:, 13]),
                 np.mean(log_res[:, 14]), np.mean(log_res[:, 15])]
        freq_inf = sf.frequency(N, pi2, rho2, phi2, beta2, B2, n_states)

        # Save parameters to file
        f = open(path_to_log + "params_SLiM_{0}_logs_{1}.txt".format(sel_type, sel_log), 'w')
        f.write("pi {0}, {1}, {2}, {3} \n".format(pi2[0], pi2[1], pi2[2], pi2[3]))
        f.write("rho {0}, {1}, {2}, {3}, {4}, {5} \n".format(rho2[0], rho2[1], rho2[2], rho2[3], rho2[4], rho2[5]))
        f.write("sigma {0} \n".format(sigma2))
        f.write(
            "beta {0}, {1}, {2}, {3}, {4}, {5} \n".format(beta2[0], beta2[1], beta2[2], beta2[3], beta2[4], beta2[5]))
        f.write("B {0}, {1}, {2}, {3}, {4}, {5} \n".format(B2[0], B2[1], B2[2], B2[3], B2[4], B2[5]))
        f.close()

        # Plot FREQUENCIES
        # Specify font:
        # vector of numbers of states
        x = np.arange(0, N+1)
        y_th = np.zeros((6, N + 1))
        y_sim = np.zeros((6, N+1))
        y_inf = np.zeros((6, N+1))
        comb = [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]
        for i in range(6):
            # From simulations
            y_sim[i, 0] = freq_sim[comb[i][0]]
            y_sim[i, 1:N] = np.flip(freq_sim[4 + (N-1)*i:4 + (N - 1)*(i+1)])
            y_sim[i, N] = freq_sim[comb[i][1]]
            #print("Sum data {0}{1}".format(comb[i][0], comb[i][1]), sum(y_sim[i, :]))
            y_inf[i, 0] = freq_inf[comb[i][0]]
            y_inf[i, 1:N] = np.flip(freq_inf[4 + (N-1)*i:4 + (N - 1)*(i+1)])
            y_inf[i, N] = freq_inf[comb[i][1]]
        type[sel_type].append(y_sim)
        type["{0}_inf".format(sel_type)].append(y_inf)
        iter += 1

    markers = ['*', 'd', 'X', 'o', 'h', '<', 'x', '1', 's', '+', 'P', '*', 'd', '.', 'o']
    colors = ['teal', 'orangered', 'forestgreen', 'purple', 'gold', 'magenta', 'cyan', 'coral', 'b']
    # Plot

    fig = plt.figure(figsize=(28, 18), facecolor='w', edgecolor='k')
    font = {'family': 'Times New Roman', 'weight': 'normal', 'size': 15}
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif', size=35)
    lab = ["AC", "AG", "AT", "CG", "CT", "GT"]
    for i in range(0, 6):
        fig.add_subplot(2, 3, i+1)
        plt.xlabel('n')
        plt.ylabel('SFS {0}'.format(lab[i]))
        plt.plot(type[keys[0]][0][i, :], linestyle="--", markerfacecolor='none', markeredgewidth=3, color=colors[0], marker=markers[0],
                  markersize=30,  alpha=0.6, label="Simulations_{0}".format(keys[0]))
        # plt.plot(type["{0}_inf".format(keys[0])][0][i, :], linestyle="--", markerfacecolor='none', markeredgewidth=3, color=colors[1], marker=markers[1],
        #           markersize=30,  alpha=0.6, label="Inference_{0}".format(keys[0]))
        # Finish this
        for j in range(len(keys)-1):
            plt.plot(type[keys[j+1]][0][i, :], linestyle="--", markerfacecolor='none', markeredgewidth=3,
                     color=colors[j+2], marker=markers[0],
                     markersize=30, alpha=0.6, label="Simulations_{0}".format(keys[j+1]))
            # plt.plot(type["{0}_inf".format(keys[j+1])][0][i, :], linestyle="--", markerfacecolor='none',
            #          markeredgewidth=3, color=colors[len(colors) - j - 1], marker=markers[1],
            #          markersize=30, alpha=0.6, label="Inference_{0}".format(keys[0]))
    plt.legend()
    plt.tight_layout()
    path_to_figures = path
    plt.savefig(path_to_figures + "/Stationary_frequencies_SLiM_Pomo{0}_test_{1}.pdf".format(N, folder))
    plt.show()