import click
from collections.abc import Mapping
import csv
import functools
import os
from writer import write_results

def strip_path(filename):
    return os.path.basename(os.path.normpath(filename))


def summarise_results(results):
    summary_results = {}

    for r in results:
        if 'id' in summary_results.keys():
            assert(r['id'] == summary_results['id'])
        else:
            summary_results['id'] = r['id']
        
        e_dict = summary_results.get(r['executable'], {})

        e_dict[r['num_par']] = r['runtime']

        summary_results[r['executable']] = e_dict
    
    return summary_results


def flatten_results(results):
    flat_results = {}
    
    for k in results.keys():
        if isinstance(results[k], Mapping):
            d = results[k]
            for k2 in d.keys():
                fullkey = "%s_%s" % (k, k2)
                flat_results[fullkey] = d[k2]
        else:
            flat_results[k] = results[k]
    return flat_results


@click.command()
@click.option('--basedir', default=None, help='Directory to find executables')
@click.option('--identifier', required=True, help='Identify this submission')
@click.option('--leaderboard-path', required=True, help='Location of leaderboard')
@click.option('--iresults', default="iresults.csv", help='Filename for intermediate results')
@click.option('--sresults', default="sresults.csv", help='Filename for summarised results')
def run(basedir, identifier, leaderboard_path, iresults, sresults):
    iresults = os.path.join(basedir, iresults)
    sresults = os.path.join(leaderboard_path, sresults)

    existing_results = None
    if os.path.exists(iresults):
        with open(iresults, 'r') as ifile:
            reader = csv.DictReader(ifile)
            existing_results = list(reader)
    else:
        print("Input file does not exist")
        return
    
    existing_results = [{'id': x['id'],
                         'executable': strip_path(x['executable']),
                         'num_par': int(x['num_par']),
                         'runtime': float(x['runtime'])} for x in existing_results]
    
    results = summarise_results(existing_results)
    results = flatten_results(results)
    write_results(results, lambda x: x['id'] == str(identifier), sresults)


if __name__=="__main__":
    run()