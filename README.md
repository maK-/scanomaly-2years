# scanomaly
Automated web fuzzing for anomalies (use python 3.6+)

## Description
The goal of this tool is to be a flexible request fuzzer. Generating lists of requests to make via the different modules. I'll hopefully continuously add new modules as I get more ideas.
Each element of a request is configurable, the method types, user agents, headers, parameters. You can provide a single URL or list of urls to scan. 

The options with * below are compulsory. By default it used 2 threads

`-u` provide a URL or `-ul` provide a file with a list of URLs *

`-scan` Runs a scan only if modules have been selected

`-t` is the number of threads to scan with

`-a` set a user agent for all requests

`-al` select a random user agent and use for all requests

`-d` POST data to pass

`-c` Cookies to use

`-db` store in a database

`-sc` store the full response body

## Modules
To use all modules and view their info use `-m all -mi`
If you want to store the responses for the folowing modules, add `-db [databasename]`

`-m archives dirb parameth` Load specified modules

`-mx dirb-files` exclude a module by name

Some modules require arguments, it's important not to use these at the same time.

For example dirb-files takes an argument of filetypes `-dl html php asp` etc. If this is loaded at the same time as the vhost module it will interpret html as a passed domain and php as a list to be read.

#### baseline
This module will be used as a means of establishing baselines, this can be useful when later assessing the responses for anomalies.

` ./scanomaly.py -u http://127.0.0.1 -m baseline -scan -t 10`

#### dirb
This module scans a directory for common directories and filenames. An example use is the following:

` ./scanomaly.py -u http://127.0.0.1/ -m dirb -scan -t 10`

#### parameth
This module is used to brute force parameters and is based on (mak-/parameth)

` ./scanomaly.py -u http://127.0.0.1/ -m parameth -scan -t 10`

#### repo
This module scans a directory for common config, meta-info and code repo files.

` ./scanomaly.py -u http://127.0.0.1/ -m repo -scan -t 10`

#### archives
This module scans a directory for common archive files and generates additional archive names from the provided URL

` ./scanomaly.py -u http://127.0.0.1/ -m archives -scan -t 10`

#### dirb-files
This modules scans a directory for common file names using a specified file extension (default: html)

You can specify the filetype or file extension to use with `-dl [filetype] [filetype]...`

` ./scanomaly.py -u http://127.0.0.1/ -m dirb-files -dl php -scan -t 10`

### dirb-custom
This module scans a directory for a provided file list

You can specify a file list to use by using `-dl [wordlist]`

` ./scanomaly.py -u http://127.0.0.1/ -m dirb-custom -dl [wordlist] -scan -t 10`

#### vhost
This scans a server for common dev virtual hosts or for a provided list of domains

You can provide a single domain to scan for using `-dl blah.com`

It is also possible to use `-dl blah.com [list of sub/domains]`

` ./scanomaly.py -u http://127.0.0.1/ -m vhost -dl localhost -scan -t 10`
