import csv
#from . import Index

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
#class Results(object):
#    """
#    Represents a set of simulation results in relation to a given index
#    This class understands and is tied to the current file format
#    """
#    def __init__(self, root='.'):
#        self.root = root
#        self.index = Index(root=root)
#        self.data = []
#        self.fields = []
#        reader = csv.DictReader(open(os.path.join(root, 'SimResults.csv'), 'r'), skipinitialspace=True)
#        for row in reader:
#        
#            """I need to do something here to handle any timeseries results"""
#            
#            resultID = row.pop('Id')
#            resultDateTime = row.pop('Date/Time')
#            jobID = row.pop('Job_Id')   #different header for JobID
#            job = self.index.jobs[jobID]
#            for k in row.keys():
#                field = OutputField(k)
#                if row[k] == '-':
#                    row[k] = 0.0
#                else:
#                    row[k] = float(row[k])
#                self.data.append({'job': job, 'field': field, 'value': row[k]})
#        for k in row.keys():
#            self.fields.append(OutputField(k))
#
#    def find(self, value=None, job=None, field=None):
#        """returns a list of results filtered by the given values"""
#        return [r for r in self.data if (((r['job']==job) | (job is None)) & ((r['value']==value) | (value is None) & (r['field'].name==field) | (field is None)))]
#
#    def datasets(self):
#        result = {}
#        for f in self.fields:
#            result[f] = [r['value'] for r in self.find(field=f.name)]
#        return result
#
#    def jobs(self):
#        return [r['job'] for r in self.find(field=self.fields[0].name)]

