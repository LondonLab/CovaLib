import sys
import os
#import Paths
import matplotlib.pyplot as plt
from pprint import pprint
import subprocess as sp
import Bio.PDB as bp
sys.path.append(os.path.dirname(sys.argv[0]) + "/../")
from Code import PDBUtils




DOCKING_RUN_FILES = "Docking_run"
BASE_RMSD = '/home/rosaliel/chemfarm/Benchmark/Round_32/baseline'
BASE_SCORE = '/home/rosaliel/chemfarm/Benchmark/Round_32/scores'


class Analyzer(object):
    
    def __init__(self, path):  
        """
        path - location of the file where all results of running benchmark are
        """
        self.path = path 
        self.current_location = os.getcwd()
        self.rmsd = dict()
        self._get_rmsd_list()
        self._get_scores_list()
        self._get_running_time()
        #self._get_step()
                
    #############
    ## Data loading
    #############
    
    def _get_rmsd_list(self):
        """
        Creating a dictionary of all rmsd values calculated after docking.
        Writes to 'no_rmsd' receptors that failed the docking.
        """
        fout_no = open('no_rmsd','w')#no poses file
        fout_empty = open('rmsd_empty','w')#poses file was empty
        fout_minus = open('minus_1','w')
        for subdir in os.listdir(self.path):
            if subdir.startswith('.'):
                continue
            try:
                rmsd = open('{0}/{1}/{2}/rmsd.txt'.format(self.path, subdir, DOCKING_RUN_FILES),'r').read()
                if rmsd == '': #no rmsd calculated
                    fout_empty.write(subdir + '\n')
                elif '-1.0' in rmsd:
                    fout_minus.write(subdir + '\n')
                else:
                    self.rmsd[subdir] = float(rmsd.strip())
            except:
                fout_no.write(subdir + '\n') 
                                
    def _get_scores_list(self):
        """
        Creates a dictionary of all scores.
        output:
            self.scores
        """
        self.scores = dict()
        for subdir in os.listdir(self.path):
            if subdir.startswith('.'):
                continue
            try:
                score = open('{0}/{1}/{2}/extract_all.sort.uniq.txt'.format(self.path, subdir, DOCKING_RUN_FILES),'r').read().split()[-1]
                self.scores[subdir] = float(score.strip())
            except:
                pass                   
    
    def _get_running_time(self):
        """Sets self.running_time by summing all run times of successful runs"""
        time_sum = 0.0
        for subdir in os.listdir(self.path):
            if subdir.startswith('.'):
                continue
            try:
                line = open('{0}/{1}/{2}/out/OUTDOCK'.format(self.path, subdir, DOCKING_RUN_FILES),'r').readlines()[-1]
                if line.startswith('elapsed time'):
                    time = float(line.split()[-1])
                    time_sum = time_sum + time
            except:
                pass   
        self.running_time = time_sum
            
    def _get_step(self):
        """Deprecaterd"""
        try:
            self.step = float(open(self.path + '../doc').readlines()[-1].split()[-1])
        except:
            #self.step = "(i, i = 80, 280, 10)"
            print os.getcwd()
            self.step = open(self.path + '../doc').readlines()[-1].split()[-1]
    
    def _get_rotetable_bond(self):
        f = open('../benchmark_files/rot_bonds','r')
        d = dict()
        for line in f:
            d[line.split()[0]] = line.split()[1]
        return d
     
    #############
    ## create data files
    #############

    def create_base(self):
        """Creates a file containing all rmsd values"""
        fout = open('baseline','w')
        fout.write(reduce(lambda x, key: '{0}\n{1:<15}{2}'.format(x, key, str(self.rmsd[key])), self.rmsd, ''))
        pass

    def create_scores(self):
        """Creates a file containing the best docking score for every receptor"""
        fout = open('scores','w')
        fout.write(reduce(lambda x, key: '{0}\n{1:<15}{2}'.format(x, key, str(self.scores[key])), self.scores, ''))
        pass
            
    def create_running_time(self):
        open('running_time','w').write(str(self.running_time))
 
    #############
    ## Plotting
    #############
    
    def plot_hist_rmsd(self):
        num_bins =  round( max(self.rmsd.values()))
        plt.hist(self.rmsd.values(), num_bins, facecolor = '#22D8EC')
        plt.title("RMSD Histogram")
        plt.xlabel("Value")
        plt.ylabel("Frequency")
        plt.savefig('rmsd_hist')
        #plt.show()
        
    def plot_rmsd_size(self):
        counts = dict()
        for k in self.rmsd.keys():
            counts[k] = PDBUtils.count_heavy_atom( '{0}{1}/xtal-lig.pdb'.format(self.path, k))
        x = list()
        y = list()
        for k in counts.keys():
            x.append(counts[k])
            y.append(self.rmsd[k])
            
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.plot(x, y, linestyle = 'None', marker = r'$\circlearrowleft$')
        plt.title("Size - RMSD")
        plt.xlabel("heavy atom count")
        plt.ylabel("RMSD value")
        plt.savefig('Size_RMSD')
        #plt.show()
        
    def plot_rotbonds_rmsd(self):
        rotbonds = self._get_rotetable_bond()
        x = list()
        y = list()
        for k in self.rmsd.keys():
            x.append(rotbonds[k])
            y.append(self.rmsd[k])
            
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.plot(x, y, linestyle = 'None', marker = 'o', color = '#a328eb')
        plt.title("Size - RMSD")
        plt.xlabel("# rotetable bonds")
        plt.ylabel("RMSD value")
        plt.savefig('rot_rmsd')
        plt.show()
        
    def plot_diff(self):
        ## read baseline rmsds
        base_rmsd = self._read_baseline(BASE_RMSD)
        base_score = self._read_baseline(BASE_SCORE)
        x = []
        y = []
        diffs = []
        labels = []
        for k in self.rmsd.keys():
            try:
                #diffs.append(base_rmsd[k] - self.rmsd[k])  
                diffs.append(base_score[k] - self.scores[k]) 
                y.append(self.rmsd[k])
                x.append(base_rmsd[k]) 
                labels.append(k)
            except:
                pass
            
        ## rmsd's. different color if the scor difference between now and baseline is more than 1
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ind_diff_more = [i for i in range(len(diffs)) if abs(diffs[i])>=1]
        ind_diff_less = [i for i in range(len(diffs)) if i not in ind_diff_more]
        ax.plot(range(-1,18), range(-1,18), 'k-', label = 'y = x')
        ax.plot([x[i] for i in ind_diff_less], [y[i] for i in ind_diff_less] , linestyle = 'None', marker = 'o', color = '#a328eb',label = 'score diff < 1')#purple
        ax.plot([x[i] for i in ind_diff_more], [y[i] for i in ind_diff_more] , linestyle = 'None', marker = 'o', color = '#22D8EC', label =  'score diff > 1') #cyan
        
        
        ## names for data point that diviates from Y=X significantly 
        for i in range(len(x)):
            if abs(x[i]-y[i])>=1:
                plt.text(x[i], y[i], labels[i], fontsize = 8)
                
        ## legend
        ax.legend(loc = 'lower right', fontsize = 11)
        plt.text(13.5,2,'running time: {0:.2f}'.format(self.running_time), fontsize = 11)
        plt.text(13.5,3,'mean rmsd:  {0:.2f}'.format(self._calculate_rmsd_mean()), fontsize = 11)
        plt.title("rmsd comparisation")
        plt.ylabel("current rmsd")
        plt.xlabel("baseline rmsd")
        plt.savefig('comp_rmsd')
        plt.show()  
                
    #############
    ## Calculations
    #############

    def _read_baseline(self, path):
        """reads a baseline file (contains list of names and rmsd values) and returns it as a dictionary"""
        base_rmsd = dict()
        fin = open(path,'r')
        for line in fin:
            if line == '\s' or line == '' or line == '\n':
                continue
            k, v = line.split()
            base_rmsd[k.strip()] = float(v.strip())
        return base_rmsd
    
    def _read_scores(self,path):
        """reads a scores file (contains list of names and scores) and returns it as a dictionary"""
        scores = dict()
        fin = open(path,'r')
        for line in fin:
            k, v = line.split()
            scores[k.strip()] = float(v.strip())
        return scores        
    
    def _calculate_rmsd_mean(self):
        return reduce (lambda x,y: x+y, self.rmsd.values())/float(len(self.rmsd))    
      
    

 
               
def main(name, argv):
        if(len(argv) != 1):
            print_usage(name)
            return
        path = argv[0]
        ab = Analyze_Bechmark(path)
        ab.create_base()
        ab.plot_hist_rmsd()
        #ab.create_scores()
        #ab.create_running_time()
        ab.plot_diff()
        #ab.plot_rotbonds_rmsd()

def print_usage(name):
        print "Usage : " + name + " <Run_directory>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])

