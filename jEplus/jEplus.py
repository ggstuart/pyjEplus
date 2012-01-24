import os, csv

class jEplus(object):
    """
    Represents a complete set of jEplus outputs
    """
    def __init__(self, root='.'):
        self.results = SimResults(os.path.join(root, 'SimResults.csv'))
        self.parameters = [Parameter(os.path.join(root, f)) for f in os.listdir(root) if 'IndexP' in f]
        self.index = SimJobIndex(os.path.join(root, 'SimJobIndex.csv'), self.parameters)
        
        
class SimResults(object):
    """
    Represents a set of simulation results
    This class understands and is tied to the current file format
    """
    def __init__(self, filename):
        reader = csv.DictReader(open(filename, 'r'), skipinitialspace=True)
        self.results = {}
        for row in reader:
            """I need to do something here to handle any timeseries results"""
            self.results[row['Job_Id']] = SimResult(**row)    #header for JobID isn't quite right

    def jobIDs(self):
        return [r.jobID for r in self.results]

    def fields(self):
        k = self.results.keys()[0]
        return [d['field'] for d in self.results[k].data]

    def field(self, field):
        """Value of a given field, across all simResults"""
        result = []
        for jobID in self.results.keys():
            for d in self.results[jobID].data:
                if d['field'].name == field: result.append(d['value'])
        return result
#        [d['value'] for jobID in self.results.keys() for d in self.results[jobID].data if self.results[jobID].data['field']==field]


class SimResult(object):
    def __init__(self, **kwargs):
        self.id = kwargs.pop('Id')
        self.DateTime = kwargs.pop('Date/Time')
        self.jobID = kwargs.pop('Job_Id')
        self.data = []
        for k in kwargs.keys():
            fld = OutputField(k)
            if kwargs[k] == '-':
                val = 0.0
            else:
                val = float(kwargs[k])
            self.data.append({'field': fld, 'value': val})

class OutputField(object):
    def __init__(self, colHead):
        data = colHead.split(' ')
        self.name, self.type = data[0].split(':')
        self.units = data[1].split('[')[1].split(']')[0]
        self.comment = data[1].split('(')[1].split(')')[0]

class Parameter(object):
    """
    Represents a parameter including all possible values it can take in the simulation run
    This class understands and is tied to the current file format
    """
    def __init__(self, filename):
        reader = csv.DictReader(open(filename, 'r'), skipinitialspace=True)
        self.values = []
        for row in reader:
            self.values.append(ParamValue(row['Index'], row['VALUE'], self))
        self.id = row['ID']
        self.name = row['NAME']
        self.type = row['Type']
        self.description = row['DISCRIPTION']   #spelling error in raw data file
        self.search_string = row['SEARCHSTRING']
        
        
class ParamValue(object):
    """Represents an actual value of a given parameter, maps value to an index"""
    def __init__(self, index, value, param):
        self.index = index
        self.value = value
        self.param = param
        

class SimJobIndex(object):
    """
    Represents an index of simulation jobs
    This class understands and is tied to the current file format
    """
    def __init__(self, filename, parameters):
        reader = csv.DictReader(open(filename, 'r'), skipinitialspace=True)
        self.jobs = {}
        for row in reader:
            #SimJobIndex file header is the parameter search_string
            jobID = row['JobID']
            WeatherFile = row['WeatherFile']
            ModelFile = row['ModelFile']
            values = [ParamValue(self, row[p.search_string], p) for p in parameters]
            self.jobs[jobID] = SimJob(jobID, WeatherFile, ModelFile, values)


class SimJob(object):
    """Represents a simulation job with associated weather file, model file and concrete parameter values"""
    def __init__(self, jobID, WeatherFile, ModelFile, values):
        self.jobid = jobID
        self.WeatherFile = WeatherFile
        self.ModelFile = ModelFile
        self.values = values
