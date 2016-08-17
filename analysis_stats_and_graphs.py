import numpy as np
from collections import OrderedDict
from module.save_db_dic import Database
from pylab import plt
from os import path, mkdir


class Analyst(object):

    def __init__(self, result_folder):

        self.result_folder = result_folder

        self.db = Database(folder_path=result_folder, database_name="results")
        self.n = len(self.db.read_column(column_name='ID'))
        self.parameters = self.db.get_column_list()

        self.parameters_to_test = ['alpha', 'tau', 'epsilon', 'q_information']

        print("Parameters:", self.parameters)
        print()

    def compute_min_max(self):

        for i in self.parameters_to_test:
            self.get_n_money_state_according_to_parameter(i)

        print("*"*10)
        print("And under the hypothesis that a0 = a1 = a2?")
        print("*" * 10)
        print()
        self.stats_about_economies_with_equal_fd()
        for i in self.parameters_to_test:
            self.get_n_money_state_according_to_parameter_and_equal_fd(i)

    def get_n_money_state_according_to_parameter(self, parameter):

        assert parameter in self.parameters, 'You ask for a parameter that is not in the list...'

        parameter_values = np.unique(self.db.read_column(column_name='{}'.format(parameter)))
        print("Possible values for {}:".format(parameter), parameter_values)
        print("Possible values for {}:".format(parameter), "min", np.min(parameter_values),
              "max", np.max(parameter_values))

        values_with_money = \
            [i[0] for i in self.db.read(query="SELECT `{}` FROM `data` WHERE m_sum > 0".format(parameter))]
        print("Values with money for {}:".format(parameter), "min", np.min(values_with_money),
              "max", np.max(values_with_money))
        print()

    def stats_about_economies_with_equal_fd(self):

        print("n sample:", self.n)
        print("n with equal fundamental structure:",
              len(self.db.read(query="SELECT `ID` FROM `data` WHERE a0 = a1 AND a1 = a2")))
        print("n with equal fundamental structure and more than one moneraty state:",
              len(self.db.read(query="SELECT `ID` FROM `data` WHERE m_sum > 0 AND a0 = a1 AND a1 = a2")))
        print()

    def get_n_money_state_according_to_parameter_and_equal_fd(self, parameter):

        assert parameter in self.parameters, 'You ask for a parameter that is not in the list...'

        parameter_values = np.unique(self.db.read_column(column_name='{}'.format(parameter)))
        print("Possible values for {}:".format(parameter), parameter_values)
        print("Possible values for {}:".format(parameter), "min", np.min(parameter_values),
              "max", np.max(parameter_values))

        values_with_money = \
            [i[0] for i in self.db.read
             (query="SELECT `{}` FROM `data` WHERE m_sum > 0 AND a0 = a1 AND a1 = a2".format(parameter))]
        print("Values with money for {}:".format(parameter), "min", np.min(values_with_money),
              "max", np.max(values_with_money))
        print()

    def represent_var_according_to_parameter(self, var):

        assert var in self.parameters, ""

        results = {}

        for parameter in self.parameters_to_test:

            parameter_values = np.unique(self.db.read_column(column_name='{}'.format(parameter)))
            print("Possible values for {}:".format(parameter), parameter_values)
            print("Possible values for {}:".format(parameter), "min", np.min(parameter_values),
                  "max", np.max(parameter_values))

            average_m_sum = OrderedDict()

            for v in parameter_values:

                m_sum = \
                    [i[0] for i in self.db.read
                     (query="SELECT `{}` FROM `data` WHERE {} = {}".format(var, parameter, v))]
                average_m_sum[v] = np.mean(m_sum)

            print("Average '{}' for {}".format(var, parameter), average_m_sum)

            results[parameter] = average_m_sum

            print()

        return results

    def select_best_economy(self):

        m_sum = \
            [i[0] for i in self.db.read
             (query="SELECT `m_sum` FROM `data`")]
        max_m_sum = np.max(m_sum)

        idx_max_m_sum = self.db.read(query="SELECT `idx` FROM `data` WHERE `m_sum` = {}".format(max_m_sum))[0][0]
        print("Economy idx with the greatest number of monetary state:", idx_max_m_sum)

        # economy_suffix = "{}_idx{}".format(self.session_suffix, idx_max_m_sum)
        #
        # print("Parameters", import_parameters(economy_suffix))

    def plot_var_against_parameter(self, var, results, figure_folder):

        if not path.exists(figure_folder):
            mkdir(figure_folder)

        for parameter in results.keys():

            x = [i for i in results[parameter].keys()]
            y = [i for i in results[parameter].values()]

            fig_title = "{} against {}".format(var, parameter)

            plt.plot(x, y, linewidth=2)
            plt.title(fig_title)

            if not path.exists("../figures"):
                mkdir("../figures")

            plt.savefig("{}/{}.pdf".format(figure_folder, fig_title))
            plt.close()


def main():

    result_folder = "../results"
    figure_folder = "../global_analysis"

    a = Analyst(result_folder=result_folder)
    # a.compute_min_max()
    results = a.represent_var_according_to_parameter('m_sum')
    a.plot_var_against_parameter('m_sum', results, figure_folder)
    # a.represent_var_according_to_parameter('interruptions')
    # a.select_best_economy()

if __name__ == "__main__":

    main()
